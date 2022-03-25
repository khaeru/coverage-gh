from datetime import datetime, timezone
from itertools import groupby
from pathlib import Path
from typing import Dict, List, Tuple

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
        return f"Added lines #L{start_line}-{end_line} not covered by tests"


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


def read_data() -> Tuple[List[Dict], Numbers]:
    """Read data from coverage's storage location & create annotations."""
    # TODO make location configurable
    cov = coverage.Coverage()
    cov.load()

    annotations = []
    total = Numbers()

    # Iterate over files
    for fr, analysis in get_analysis_to_report(cov, morfs=None):
        # Generate annotations for the current file
        for missing_range in get_missing_range(analysis.missing):
            annotation = create_single_annotation(missing_range, fr.relative_filename())
            annotations.append(annotation)
            if len(annotations) >= MAX_ANNOTATIONS:
                print("Reached maximum {MAX_ANNOTATIONS}; stopping")

        total += analysis.numbers

    return annotations, total


class GitHubAPIClient:
    """Minimal client to prepare and make a POST request to GitHub's Checks API."""

    def __init__(self, **options):
        # Arguments for requests.post()
        self._request = dict(
            url=f"{options.pop('api_url')}/repos/{options.pop('repo')}/check-runs",
            headers=dict(
                Accept="application/vnd.github.v3+json",
                Authorization=f"token {options.pop('token')}",
            ),
        )

        # SHA for the HEAD of the pull request branch; used by get_payload()
        self._sha = options.pop("sha")

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
            name="pytest-coverage",
            head_sha=self._sha,
            status="completed",
            conclusion=self.get_conclusion(),
            completed_at=datetime.now(timezone.utc).isoformat(),
            output=dict(
                title="Coverage Result",
                summary=self.render_summary(),
                text="Coverage results",
                annotations=self.annotations,
            ),
        )

    def post(self):
        self.annotations, self.total = read_data()
        payload = self.get_payload()

        if self._options["verbose"] or self._options["dry_run"]:
            print(self._request)
            print(payload)

        if self._options["event_name"] != "pull_request":
            print(
                "Will not make a request for GITHUB_EVENT_NAME=="
                + self._options["event_name"]
            )
            return

        if not self._options["dry_run"]:
            requests.post(**self._request, json=payload).raise_for_status()
