"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Acme Bleach."""


if __name__ == "__main__":
    main(prog_name="acme-bleach")  # pragma: no cover
