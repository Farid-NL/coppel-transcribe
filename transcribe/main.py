import os

import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from transcribe import utils

app = typer.Typer()
err_console = Console(stderr=True)


# TODO: Append programas file processed to outfile
# TODO: Add 'Etapa' argument to command
@app.command()
def windows(
    ip_directory: Annotated[str, typer.Argument()],
    convert: Annotated[bool, typer.Option()] = True,
):
    full_path = os.path.abspath(ip_directory)

    if not os.path.isdir(full_path):
        err_console.print("The chosen path is not a directory.")
        raise typer.Exit(code=1)

    if convert:
        if not utils.convert_files_to_utf8(full_path):
            err_console.print("Something went wrong when converting files to UTF-8.")
            raise typer.Exit(code=1)

    ip = os.path.basename(full_path)

    # Files to be processed
    systeminfo_txt = os.path.join(full_path, f"systeminfo_{ip}.txt")
    discos_txt = os.path.join(full_path, f"discos_{ip}.txt")
    puertos_txt = os.path.join(full_path, f"puertos_{ip}.txt")
    programas_txt = os.path.join(full_path, f"programas_instalados__{ip}.txt")

    content = utils.get_summary(
        systeminfo_txt,
        discos_txt,
        ip,
    )

    content += utils.get_ports(
        puertos_txt,
    )

    content += utils.get_programs(programas_txt)

    with open(os.path.join(full_path, f"{ip}.txt"), "w") as file:
        file.write(content)


# TODO: Everything
@app.command()
def linux(ip_dir: Annotated[str, typer.Argument()]):
    pass


if __name__ == "__main__":
    app()
