import os
from pathlib import Path

import pandas


def get_bd_names(bds_path: str, ip: str):
    parent_dir = Path(bds_path).parent

    tmp_csv_path = os.path.join(parent_dir, f"{ip}.csv")

    pandas.read_excel(bds_path, usecols=["Inventory ID", "Owner"]).to_csv(
        tmp_csv_path, index=False
    )
    data_frame = pandas.read_csv(tmp_csv_path)

    data_frame.replace(r"\d+\.\d+\.\d+\.\d+ [–-] ", "", regex=True, inplace=True)
    data_frame.to_csv(tmp_csv_path, index=False, header=False)

    with open(tmp_csv_path, "r") as csv:
        bds = csv.read()

    os.remove(tmp_csv_path)

    return f"=============\n{ip}\n=============\n\n{bds}\n"


def get_bd_authors_from_matrix(csv_path: str, ips: list):
    with open(csv_path, 'r') as file:
        lines = file.readlines()

    while "SO (Windows / Linux)" not  in lines[0]:
        lines.pop(0)

    with open(csv_path, 'w') as file:
        file.writelines(lines)

    data_frame = pandas.read_csv(csv_path, usecols=["IP nueva", "Responsable Docto"])

    content = ""
    replace = [
        "Angel Eduardo Juarez Castellon",
        "Cesar Augusto Machorro Perea",
        "Mareli Natali Rojas Castillo",
        "Carlos Farid Nogales Lopez",
        "Jose Ramon Huerta Coronado"
    ]
    r_counter = 0
    for ip in ips:
        if "," in ip:
            ip = ip.replace(",", ".")

        result = data_frame[data_frame["IP nueva"] == ip]
        if not result.empty:

            if "Laura Fernández" in f"{result.iloc[0]['Responsable Docto']}":
                content += f"{ip:<13}: Cesar Augusto Machorro Perea"
            elif "Fernando Armas Tellez" in f"{result.iloc[0]['Responsable Docto']}":
                content += f"{ip:<13}: {replace[r_counter % len(replace)]}"
                r_counter += 1
            elif "nan" in f"{result.iloc[0]['Responsable Docto']}":
                content += f"{ip:<13}: N/A"
            else:
                content += f"{ip:<13}: {result.iloc[0]['Responsable Docto']}"

        else:
            content += f"{ip:<13}: ,No existe en la matriz"

        if len(result) > 1:
            content += "**, Repetido"
        content += "\n"

    return content
