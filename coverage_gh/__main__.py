from pathlib import Path

import click

from . import GitHubAPIClient


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
def cli(**options):
    GitHubAPIClient(**options).post()


if __name__ == "__main__":
    cli()
