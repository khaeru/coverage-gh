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
    "--pr-head-sha", envvar="PR_HEAD_SHA", metavar="PR_HEAD_SHA", default="a1b2c3d4"
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
def cli(**options):
    GitHubAPIClient(**options).post()


if __name__ == "__main__":
    cli()
