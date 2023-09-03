import pathlib
import runpy
import site
import typing

import click

import acme.bleach.codec  # noqa: F401


PTH_CONTENTS = """\
# Provides the bleach codec to scripts
import acme.bleach.codec
"""


@click.group
def main() -> None:
    """Remove unsightly visible characters from your source code.

    Replaces the unsightly visible characters in Python source code with strings
    of spaces and tabs.
    """
    pass


@main.command()
@click.argument("infile", type=click.File("r"))
@click.option(
    "-o", "--outfile", type=click.File("wb"), help="Write to this file.", default="-"
)
def bleach(infile: typing.TextIO, outfile: typing.BinaryIO) -> None:
    """Bleach a file by replacing unsightly visible characters.

    Writes to standard output by default.

    INFILE: Input file to bleach.
    """
    bleached = infile.read().encode("bleach")

    outfile.write(b"# coding=bleach\n")
    outfile.write(bleached)


@main.command()
@click.argument("infile", type=click.File("rb"))
@click.option(
    "-o", "--outfile", type=click.File("w"), help="Write to this file.", default="-"
)
def unbleach(infile: typing.TextIO, outfile: typing.BinaryIO) -> None:
    """Unbleach a bleached file, restoring those visible characters.

    Writes to standard output by default.

    INFILE: Input file to unbleach.
    """
    unbleached = infile.read().decode("bleach")  # type: ignore
    outfile.write(unbleached)


@main.command()
@click.option("-m", "--module", type=str, help="Run library module as script")
@click.argument(
    "filename", type=click.Path(exists=True, dir_okay=False), required=False
)
def run(filename: str, module: str | None) -> None:
    """Run a bleached (or unbleached) script.

    Wrapper around "python script.py" or "python -mscript" that understands
    "# coding=bleach" comments. If the "install" command has been run, this
    wrapper is not necessary.

    FILENAME: Script to run.
    """

    if module:
        runpy.run_module(module)
    else:
        runpy.run_path(filename)


def _try_write_pth_to(directory: str) -> None:
    """Try and write pth file, propagating IOErrors."""
    path = pathlib.Path(directory, "bleach.pth")
    with path.open("w") as pth_out:
        pth_out.write(PTH_CONTENTS)
    print(f"Wrote {path}.")


@main.command()
@click.option("-u/-s", "--user/--system")
def install(user: bool | None) -> None:
    """Install the bleach codec to be used natively.

    This command will install a bleach.pth file into your Python installation's
    site-packages folder, enabling you to run bleached files with
    "# coding=bleach" without having to use "bleach run".
    """
    # Can't write to the user site if it doesn't exit.
    if user and not site.ENABLE_USER_SITE:
        raise click.ClickException(
            "Option --user was used to force use of user-site packages, "
            "but the user site is disabled."
        )

    # Prefer the user site over the system-wide site if not explicitly set.
    if user or (user is None and site.ENABLE_USER_SITE):
        try:
            _try_write_pth_to(site.getusersitepackages())
        except OSError as e:
            raise click.ClickException(
                f"Could not write to user site-packages. {e}"
            ) from e

    # Write to any system package if possible.
    else:
        for site_package in site.getsitepackages():
            try:
                _try_write_pth_to(site_package)
                return
            except OSError:
                pass

        raise click.ClickException(
            "Insufficient permissions to write to any of " f"{site.getsitepackages()}."
        )


if __name__ == "__main__":
    main()
