import os
import re
import zipfile
from pathlib import Path
from shutil import rmtree
from typing import List

import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from transcribe import lnx_utils, win_utils

app = typer.Typer()
multiple_app = typer.Typer()
app.add_typer(multiple_app, name="multiple")

err_console = Console(stderr=True)


# TODO: Add 'Etapa' argument to command
@app.command()
def windows(ip_zip: Annotated[str, typer.Argument()]):
    full_path = os.path.abspath(ip_zip)

    # Validation: Check if it's a zip file
    if not full_path.endswith(".zip"):
        err_console.print("The file is not a zip file.")
        raise typer.Exit(code=1)

    # Validation: Check if the zip file exists
    if not os.path.exists(full_path):
        err_console.print(f"The file '{full_path}' does not exist.")
        err_console.print("File skipped")
        return

    ip = os.path.splitext(os.path.basename(full_path))[0]

    # Directory path where the zip file is going to be extracted
    target_dir = os.path.join(os.path.dirname(full_path), ip)

    # Zip extraction
    with zipfile.ZipFile(full_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)

    # Convert UTF-16 files to UTF-18
    if not win_utils.convert_files_to_utf8(target_dir):
        err_console.print("Something went wrong when converting files to UTF-8.")
        raise typer.Exit(code=1)

    # Validation: Check if extracted files match the IP
    files = os.listdir(target_dir)
    for file in files:
        if not ip in file:
            err_console.print(f":cross_mark: [bold red]{ip}[/bold red]\t[italic](The file '{file}' does not match the IP)[/italic]")
            rmtree(target_dir)
            return

    # Files to be processed
    systeminfo_txt = os.path.join(target_dir, f"systeminfo_{ip}.txt")
    discos_txt = os.path.join(target_dir, f"discos_{ip}.txt")
    puertos_txt = os.path.join(target_dir, f"puertos_{ip}.txt")
    programas_txt = os.path.join(target_dir, f"programas_instalados__{ip}.txt")

    output_file = os.path.join(target_dir, f"{ip}.txt")

    content = win_utils.get_summary(systeminfo_txt, discos_txt, ip)
    content += win_utils.get_ports(puertos_txt)
    content += win_utils.get_programs(programas_txt)

    with open(output_file, "w") as file:
        file.write(content)

    print(f":white_check_mark: [bold green]{ip}[/bold green]")


# TODO: Check other formats and its variants
@app.command()
def linux(ip_file: Annotated[str, typer.Argument()]):
    full_path = os.path.abspath(ip_file)
    parent_dir = os.path.dirname(full_path)

    ip = os.path.splitext(os.path.basename(full_path))[0]

    # Validation: Check if file exists
    if not os.path.exists(full_path):
        err_console.print(
            f":cross_mark: [bold red]{ip}[/bold red]\t[italic](The file does not exists)[/italic]"
        )
        return

    # Validation: Check if file has format 1 (README.md)
    regex_format_1 = r"ok: \[\d+\.\d+\.\d+\.\d+]"  # r"ok: \[\d+\.\d+\.\d+\.\d+] => {"
    with open(full_path, "r") as file:
        first_line = file.readline()
    if not re.search(regex_format_1, first_line):
        err_console.print(
            f":cross_mark: [bold red]{ip}[/bold red]\t[italic](The file does not match [bold default]format 1[/bold default]"
        )
        return

    # Create output directory
    output_dir = os.path.join(parent_dir, ip)
    Path(output_dir).mkdir(0o775, True, True)
    output_file = os.path.join(output_dir, f"{ip}.txt")

    # Write content to output file
    content = lnx_utils.get_info_format_1(full_path, ip)
    with open(output_file, "w") as file:
        file.write(content)

    print(f":white_check_mark: [bold green]{ip}[/bold green]")


@multiple_app.command("windows")
def multiple_windows(
    base_dir: Annotated[str, typer.Argument()],
    ips: Annotated[List[str], typer.Argument()],
):
    full_path = os.path.abspath(base_dir)

    if not os.path.isdir(full_path):
        err_console.print("The chosen path is not a directory")
        raise typer.Exit(code=1)

    for ip in ips:
        windows(os.path.join(full_path, f"{ip}.zip"))


if __name__ == "__main__":
    app()
