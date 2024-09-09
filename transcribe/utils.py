import os
import re
from pathlib import Path
import pandas


def convert_files_to_utf8(directory_path: str) -> bool:
    """
    Convert UTF-16 encoded files to UTF-8 encoded files.
    :param directory_path: Directory where UTF-16 encoded files are located.
    :return: `True` if all files were UTF-8 encoded successfully, `False` otherwise.
    """

    def utf16_to_utf8(file_path: str):
        with open(file_path, "rb") as source:
            data = source.read().decode("utf-16").encode("utf-8")

        with open(file_path, "wb") as dest:
            dest.write(data)

    full_path = os.path.abspath(directory_path)
    files = os.listdir(full_path)

    for file in files:
        try:
            utf16_to_utf8(os.path.join(full_path, file))
        except UnicodeDecodeError:
            return False

    return True


def get_summary(info_path: str, disk_path: str, ip: str) -> str:
    """
    Return the server's information for the summary tab of the Gsheet
    :param info_path: Path of `systeminfo_X.X.X.X.txt`
    :param disk_path: Path of `discos_X.X.X.X.txt`
    :param ip: IP address of the server
    :return: Summary to be appended to the output file
    """

    def clean_line(data: list[str], row: int, regex: str = r"[\w\d_ ()]+:\s+"):
        """
        Remove regex match from given read lines
        :param data: Read lines
        :param row: Specific line number (0 index)
        :param regex: Regular expression to match
        :return: Cleaned line
        """
        return re.sub(regex, "", data[row].strip())

    with open(info_path, "r") as file:
        info = file.readlines()

    info_host = clean_line(info, 1)
    info_os = clean_line(info, 2) + " " + clean_line(info, 3)
    num_cpu = re.search(r"\d+", info[15].strip()).group(0)
    info_cpu = clean_line(info, 16, r"\[\d+]: ") + " x" + num_cpu
    info_ram = clean_line(info, 15 + int(num_cpu) + 8)

    with open(disk_path, "r+") as file:
        info_disk = file.read().strip()

    return f"""\
┌───────┐
│Resumen│
└───────┘
─ Servidor ─
{info_host}
{ip}

{info_os}

─ Características ─
{info_ram}
{info_cpu}
{info_disk}
"""


def get_ports(ports_path: str):
    parent_dir = Path(ports_path).parent
    file_name = Path(ports_path).stem

    # Tmp files
    tmp_txt_path = os.path.join(parent_dir, f"{file_name}.tmp")
    tmp_csv_path = os.path.join(parent_dir, f"{file_name}.csv")

    # Remove the 3 first lines of the original file and stores the rest in a tmp file
    with open(ports_path, "r") as ports_file, open(tmp_txt_path, "w") as tmp_txt_file:
        ports_data = ports_file.readlines()
        tmp_txt_file.writelines(ports_data[3:])

    # Create a tmp csv file
    pandas.read_fwf(tmp_txt_path).to_csv(tmp_csv_path, index=False)
    csv_data = pandas.read_csv(tmp_csv_path, usecols=["Local Address"])

    # Store just the port numbers and remove duplicates
    csv_data.replace(r".+:", "", regex=True, inplace=True)
    csv_data.drop_duplicates(inplace=True)

    # Create a string with all the ports data
    ports = "\n".join(csv_data["Local Address"])

    # Clean tmp files
    os.remove(tmp_txt_path)
    os.remove(tmp_csv_path)

    return f"""
┌───────┐
│Puertos│
└───────┘
{ports}
"""
