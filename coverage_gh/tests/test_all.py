from pathlib import Path
from shutil import copyfile

import pytest
from click.testing import CliRunner
from coverage.results import Numbers

from .. import (
    GitHubAPIClient,
    _get_annotation_message,
    cli,
    create_single_annotation,
    get_missing_range,
)


@pytest.fixture
def coveragedata(tmp_path):
    """Fixture which is a path to a coverage data file.

    TODO this uses an actual file committed to the repo; instead, use the
    coverage.CoverageData class to create such a file programmatically.
    """
    path = tmp_path.joinpath(".coverage")

    copyfile(Path(__file__).with_name("example.coverage"), path)

    yield path


def test_create_single_annotation():
    assert dict(
        annotation_level="warning",
        end_line=321,
        message="Added lines #L123–321 not covered by tests",
        path="foo/bar/baz.py",
        start_line=123,
    ) == create_single_annotation((123, 321), "foo/bar/baz.py")


def test_get_annotation_message():
    assert "Added line #L123 not covered by tests" == _get_annotation_message(123, 123)
    assert "Added lines #L123–321 not covered by tests" == _get_annotation_message(
        123, 321
    )


def test_get_missing_range():
    assert [(1, 2), (4, 7), (9, 9), (12, 13)] == list(
        get_missing_range([1, 2, 4, 5, 6, 7, 9, 12, 13])
    )


class TestGitHubAPIClient:
    @pytest.fixture
    def client(self, coveragedata):
        return GitHubAPIClient(
            data_file=coveragedata,
            api_url="api_url",
            repo="repo",
            token="token",
            event_name="pull_request",
            event_path=Path(__file__).with_name("event.json"),
            dry_run=True,
            verbose=False,
        )

    def test_get_conclusions(self, client):
        assert "success" == client.get_conclusion()

    def test_get_payload(self, client):
        client.total = Numbers()
        client.get_payload()

    def test_post(self, client):
        client.post()

        client._options["event_name"] = "foo"
        client.post()


def test_cli():
    runner = CliRunner()
    runner.invoke(cli, ["--dry-run"])
