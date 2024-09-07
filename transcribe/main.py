import os
import typer
from typing_extensions import Annotated
from rich.console import Console

app = typer.Typer()
err_console = Console(stderr=True)


# TODO: Detect directory of given IP
# TODO: Convert all files from utf-16 to utf-8
# TODO: Create outfile
# TODO: Append systeminfo file processed to outfile
# TODO: Append discos file processed to outfile
# TODO: Append puertos file processed to outfile
# TODO: Append programas file processed to outfile
# TODO: Add 'Etapa' argument to command
@app.command()
def windows(ip_dir: Annotated[str, typer.Argument()]):
    pass


# TODO: Everything
@app.command()
def linux(ip_dir: Annotated[str, typer.Argument()]):
    pass


if __name__ == "__main__":
    app()
