from pathlib import Path

import pytest

from .. import GitHubAPIClient


def test_nothing():
    pass


class TestGitHubAPIClient:
    @pytest.fixture
    def client(self):
        return GitHubAPIClient(
            api_url="api_url",
            repo="repo",
            token="token",
            event_path=Path(__file__).with_name("event.json"),
            dry_run=True,
        )

    def test_get_conclusions(self, client):
        assert "success" == client.get_conclusion()
