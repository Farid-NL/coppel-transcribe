import os
import zipfile

import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from transcribe import utils

app = typer.Typer()
err_console = Console(stderr=True)


# TODO: Add 'Etapa' argument to command
@app.command()
def windows(ip_zip: Annotated[str, typer.Argument()]):
    full_path = os.path.abspath(ip_zip)

    if not full_path.endswith(".zip"):
        err_console.print("The chosen path is not a zip file.")
        raise typer.Exit(code=1)

    parent_dir = os.path.dirname(full_path)
    ip = os.path.splitext(os.path.basename(full_path))[0]
    target_dir = os.path.join(parent_dir, ip)

    with zipfile.ZipFile(full_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)

    if not utils.convert_files_to_utf8(target_dir):
        err_console.print("Something went wrong when converting files to UTF-8.")
        raise typer.Exit(code=1)

    # Files to be processed
    systeminfo_txt = os.path.join(target_dir, f"systeminfo_{ip}.txt")
    discos_txt = os.path.join(target_dir, f"discos_{ip}.txt")
    puertos_txt = os.path.join(target_dir, f"puertos_{ip}.txt")
    programas_txt = os.path.join(target_dir, f"programas_instalados__{ip}.txt")

    output_file = os.path.join(target_dir, f"{ip}.txt")

    content = utils.get_summary(
        systeminfo_txt,
        discos_txt,
        ip,
    )

    content += utils.get_ports(
        puertos_txt,
    )

    content += utils.get_programs(programas_txt)

    with open(output_file, "w") as file:
        file.write(content)


# TODO: Everything
@app.command()
def linux(ip_dir: Annotated[str, typer.Argument()]):
    pass


if __name__ == "__main__":
    app()
