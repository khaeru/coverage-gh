import click

from . import read_data


@click.command()
def cli():
    read_data()


if __name__ == "__main__":
    cli()
