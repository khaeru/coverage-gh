import json
import operator
from datetime import datetime, timezone
from functools import reduce
from itertools import groupby
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
import coverage
import requests
from coverage.report import get_analysis_to_report
from coverage.results import Numbers
from jinja2 import Environment, FileSystemLoader

MAX_ANNOTATIONS = 50


def _get_annotation_message(start_line, end_line):
    if end_line == start_line:
        return f"Added line #L{start_line} not covered by tests"
    else:
        return f"Added lines #L{start_line}–{end_line} not covered by tests"


def _get_head_sha(info: Dict) -> Optional[str]:
    """Parse the SHA of the head commit from the GitHub event payload `info`."""
    for key in ("pull_request.head.sha", "after"):
        try:
            return reduce(operator.getitem, key.split("."), info)
        except KeyError:
            pass

    print(f"Unable to get SHA of head of PR branch from event payload: {info}")

    return None


def get_missing_range(range_list):
    for a, b in groupby(enumerate(range_list), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield (b[0][1], b[-1][1])


def create_single_annotation(error: Tuple[int, int], file_path: str) -> Dict:
    return dict(
        path=file_path,
        start_line=error[0],
        end_line=error[1],
        annotation_level="warning",
        message=_get_annotation_message(*error),
    )


def read_data(data_file=None) -> Tuple[List[Dict], Numbers]:
    """Read data from coverage's storage location & create annotations."""
    cov = coverage.Coverage(data_file)
    cov.load()

    annotations = []
    total = Numbers()

    # Iterate over files
    for fr, analysis in get_analysis_to_report(cov, morfs=None):
        # Generate annotations for the current file
        for missing_range in get_missing_range(analysis.missing):
            annotation = create_single_annotation(missing_range, fr.relative_filename())
            annotations.append(annotation)
            if len(annotations) >= MAX_ANNOTATIONS:  # pragma: no cover
                print("Reached maximum {MAX_ANNOTATIONS}; stopping")

        total += analysis.numbers

    return annotations, total


class GitHubAPIClient:
    """Minimal client to prepare and make a POST request to GitHub's Checks API."""

    annotations = []

    def __init__(self, **options):
        # Arguments for requests.post()
        self._request = dict(
            url=f"{options.pop('api_url')}/repos/{options.pop('repo')}/check-runs",
            headers=dict(
                Accept="application/vnd.github.v3+json",
                Authorization=f"token {options.pop('token')}",
            ),
        )

        # Location of the data file
        self._data_file = options.pop("data_file")

        # Read GitHub event info
        with open(options.pop("event_path")) as f:
            self._event = json.load(f)

        # Look up SHA for the HEAD of the pull request branch; used by get_payload()
        self._head_sha = _get_head_sha(self._event)

        # Store remaining options
        self._options = options

    def render_summary(self):
        env = Environment(loader=FileSystemLoader(Path(__file__).parent))
        template = env.get_template("summary.md.template")
        return template.render(
            annotations=self.annotations,
            total=self.total,
            missing_coverage_file_count=-1,
            missing_ranges_count=-1,
        )

    def get_conclusion(self):
        return "success" if len(self.annotations) == 0 else "failure"

    def get_payload(self):
        return dict(
            name="coverage",
            head_sha=self._head_sha,
            status="completed",
            conclusion=self.get_conclusion(),
            completed_at=datetime.now(timezone.utc).isoformat(),
            output=dict(
                title="Code coverage",
                summary=self.render_summary(),
                text=self.render_summary(),
                annotations=self.annotations,
            ),
        )

    def post(self):
        self.annotations, self.total = read_data(self._data_file)
        payload = self.get_payload()

        if self._options["verbose"] or self._options["dry_run"]:
            print("Request arguments:", self._request)
            print("Payload:", payload)

        if self._options["event_name"] != "pull_request":
            print(
                "Will not make a request for GITHUB_EVENT_NAME=="
                + self._options["event_name"]
            )
            return

        if not self._options["dry_run"]:
            requests.post(  # pragma: no cover
                **self._request, json=payload
            ).raise_for_status()


# Use click.option() to read values from GitHub's environment variables, else defaults
# (non-functional), while allowing user overrides
@click.command()
@click.option(
    "--api-url",
    envvar="GITHUB_API_URL",
    metavar="GITHUB_API_URL",
    default="https://example.com/api/v999",
)
@click.option(
    "--repo",
    envvar="GITHUB_REPOSITORY",
    metavar="GITHUB_REPOSITORY",
    default="user/repo",
)
@click.option(
    "--token", envvar="GITHUB_TOKEN", metavar="GITHUB_TOKEN", default="abc1234567890def"
)
@click.option("--verbose", is_flag=True, help="Display verbose output.")
@click.option("--dry-run", is_flag=True, help="Only show what would be done.")
@click.option(
    "--event-name", envvar="GITHUB_EVENT_NAME", default="MISSING", hidden=True
)
@click.option(
    "--event-path",
    envvar="GITHUB_EVENT_PATH",
    default=Path(__file__).parent.joinpath("tests", "event.json"),
    hidden=True,
)
@click.argument("data_file", nargs=-1)
def cli(**options):
    options["data_file"] = options["data_file"] or Path.cwd().joinpath(".coverage")
    GitHubAPIClient(**options).post()
