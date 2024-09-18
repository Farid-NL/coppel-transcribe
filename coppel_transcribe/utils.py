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
