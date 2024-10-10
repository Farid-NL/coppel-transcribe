import os
import re
from pathlib import Path

import pandas

POSTGRESQL_PORTS = [5432]
MYSQ_PORTS = [3306]
APPNAME_WITH_PORTS = ["java", "python"]


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
    with open(csv_path, "r") as file:
        lines = file.readlines()

    while "SO (Windows / Linux)" not in lines[0]:
        lines.pop(0)

    with open(csv_path, "w") as file:
        file.writelines(lines)

    data_frame = pandas.read_csv(csv_path, usecols=["IP nueva", "Responsable Docto"])

    content = ""
    replace = [
        "Angel Eduardo Juarez Castellon",
        "Cesar Augusto Machorro Perea",
        "Mareli Natali Rojas Castillo",
        "Carlos Farid Nogales Lopez",
        "Jose Ramon Huerta Coronado",
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


def is_port_apps_empty(excel_file: str):
    full_path = os.path.abspath(excel_file)

    data_frame = pandas.read_excel(full_path, sheet_name="Puerto por Aplicaciones")

    data_frame.columns = data_frame.iloc[9]
    data_frame.drop(data_frame.index[:10], inplace=True)

    if data_frame["Aplicación que viven en el servidor "].isnull().values.any():
        return True
    else:
        return False


def revision_listos_8(excel_file: str):
    def adjust_df(dataframe, header_row: int, content_row: int):
        dataframe.columns = dataframe.iloc[header_row]  # Use row 9 as column headers
        dataframe.drop(
            dataframe.index[:content_row],  # Use only the data from row 10 onwards.
            inplace=True,
        )

    full_path = os.path.abspath(excel_file)

    so_checkbox = False
    ready_checkbox = False

    df_resumen = pandas.read_excel(full_path, sheet_name="Resumen")
    df_puertos = pandas.read_excel(full_path, sheet_name="Puerto por Aplicaciones")
    df_bds = pandas.read_excel(full_path, sheet_name="BD ")

    # S.O check box (docs/revision-total-version-listos.md)
    so = df_resumen.iloc[8, 2]
    so_version = float(re.search(r"\d+(?:\.?\d+)?", so).group(0))
    if 8 <= so_version < 9:
        so_checkbox = True
        print(f"SO Check\nVersión: {so_version} - ✅")
    else:
        print(f"SO Check\nVersión: {so_version} - ❌")

    # Migration check box (docs/revision-total-version-listos.md)
    allowed = [
        "nessus-agen",
        "haproxy",
        "rte-sensor",
        "sshd",
    ]

    forbidden = [
        "xinetd",
        "httpd",
    ]

    print("\nMigración Check")

    # Condition 1
    if not so_checkbox:
        print(f"SO versión: {so_version} - ❌")
        return so_checkbox, ready_checkbox

    # Condition 2 - Forbidden
    adjust_df(df_puertos, header_row=9, content_row=10)
    if (
        True
        in df_puertos["Aplicación que viven en el servidor "].isin(forbidden).values
    ):
        print(f"Puerto por Aplicaciones (Web): {forbidden} - ❌")
        return so_checkbox, ready_checkbox

    # Condition 3 - Worksheet 'BD'
    adjust_df(df_bds, header_row=8, content_row=9)
    if df_bds["Base de datos"].values.any():
        print("Hoja BD: No está vacía - ❌")
        return so_checkbox, ready_checkbox

    # Condition 3 - Ports associated with some DBMS
    if (
        df_puertos["Puerto"].isin(POSTGRESQL_PORTS).any()
        or df_puertos["Puerto"].isin(MYSQ_PORTS).any()
    ):
        print("Puerto por Aplicaciones (BD): ❌")
        return so_checkbox, ready_checkbox

    # Condition 3 - Ports associated with some application
    if (
        df_puertos["Aplicación que viven en el servidor "]
        .isin(APPNAME_WITH_PORTS)
        .any()
    ):
        print(f"Puerto por Aplicaciones: {APPNAME_WITH_PORTS} - ❌")
        return so_checkbox, ready_checkbox

    # Condition 2 - Allowed
    if True in df_puertos["Aplicación que viven en el servidor "].isin(allowed).values:
        ready_checkbox = True

    print("Todo bien: ✅")
    return so_checkbox, ready_checkbox
