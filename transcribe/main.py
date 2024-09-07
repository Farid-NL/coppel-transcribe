import os

import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from . import utils

app = typer.Typer()
err_console = Console(stderr=True)


# TODO: Create outfile
# TODO: Append systeminfo file processed to outfile
# TODO: Append discos file processed to outfile
# TODO: Append puertos file processed to outfile
# TODO: Append programas file processed to outfile
# TODO: Add 'Etapa' argument to command
@app.command()
def windows(ip_dir: Annotated[str, typer.Argument()]):
    full_path = os.path.abspath(ip_dir)

    if not os.path.isdir(full_path):
        err_console.print("The chosen path is not a directory.")
        raise typer.Exit(code=1)

    utils.convert_files_to_utf8(full_path)


# TODO: Everything
@app.command()
def linux(ip_dir: Annotated[str, typer.Argument()]):
    pass


if __name__ == "__main__":
    app()
