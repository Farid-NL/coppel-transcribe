import re


# TODO: Replace `last_lines` section with proper path handling
def get_info_format_1(file: str, ip: str) -> str:
    with open(file, "r") as file:
        data = file.readlines()

    info = dict.fromkeys(
        [
            "dns",
            "host",
            "ip",
            "os",
            "tipo",
            "ram",
            "cpu",
            "disk",
            "ports",
        ]
    )

    software = dict()

    def clean_line(row: str) -> str:
        return row.strip().replace(",", "").replace('"', "")

    last_i = 0
    last_lines = ""
    for i in range(len(data)):
        # Summary
        if "DNS" in data[i]:
            dns_list = ""
            while "___" not in data[i]:
                dns = re.search(r"\d+\.\d+\.\d+\.\d+", data[i])
                if dns:
                    dns_list += f"{dns.group()}\n"
                i += 1
            info["dns"] = dns_list

        if "hostname" in data[i]:
            info["host"] = clean_line(data[i + 1])

        if "Ambiente" in data[i]:
            info["ip"] = f"{ip} - Productivo" if "Productivo" in data[i + 1] else ip

        if "operativo" in data[i]:
            info["os"] = clean_line(data[i + 1])

        if "Base de Datos SI/NO" in data[i]:
            if "SI" in data[i + 1]:
                info["tipo"] = "Base de datos"
            elif "NO" in data[i + 1]:
                info["tipo"] = "Aplicativo"

        if "RAM" in data[i]:
            info["ram"] = re.search(r"\d+ kB", data[i + 1]).group()

        if "Numero de procesadores" in data[i]:
            info["cpu"] = f"x{clean_line(data[i + 1])}"

        if "DISCOS" in data[i]:
            sizes = ""
            while "___" not in data[i]:
                size = re.search(r"\d+(?:\.\d+)?[G|T]", data[i])
                if size and (
                    "disco root" in data[i - 1] or "disco root" in data[i - 2]
                ):
                    sizes += f"/      {size.group()}\n"
                elif size and "(sysx)" in data[i - 3]:
                    sizes += f"/sysx  {size.group()}"
                i += 1
            info["disk"] = sizes

        if "SQL SERVER" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+ Distrib .+-MariaDB", data[i + 1])
            if software_ver:
                software["MySQL"] = software_ver.group()

        if "Version de Java" in data[i]:
            while "___" not in data[i]:
                software_ver = re.search(r"(?:\d+\.)+\d+_?\d+", data[i])
                if software_ver:
                    software["Java"] = software_ver.group()
                    break
                i += 1

        if "Version de apache" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["Apache"] = software_ver.group()

        if "Version Tomcat" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["Tomcat"] = software_ver.group()

        if "Version de XINETD" in data[i]:
            while "___" not in data[i]:
                software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
                if software_ver:
                    software["xinetd"] = software_ver.group()
                    break
                i += 1

        if "Version SAMBA" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["Samba"] = software_ver.group()

        if "Version de python" in data[i]:
            python_ver = ""
            while "___" not in data[i]:
                software_ver = re.search(r"\d+(?:\.\d+\w?)?", data[i])
                if software_ver:
                    python_ver += f"{software_ver.group()}, "
                i += 1
            if python_ver:
                software["Python"] = f"{python_ver.strip(", ")}"

        if "Version de nginx" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["Nginx"] = software_ver.group()

        if "NODEJS version" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["NodeJS"] = software_ver.group()

        if "Version PHP" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["PHP"] = software_ver.group()

        if "Version de Mongo" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["PHP"] = software_ver.group()

        if "Version Postgres" in data[i]:
            while "___" not in data[i]:
                software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
                if software_ver:
                    software["PostgreSQL"] = software_ver.group()
                    break
                i += 1

        if "Version de REDIS" in data[i]:
            software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
            if software_ver:
                software["Redis"] = software_ver.group()

        if "Version Docker" in data[i]:
            while "___" not in data[i]:
                software_ver = re.search(r"(?:\d+\.)+\d+", data[i + 1])
                if software_ver:
                    software["Docker"] = software_ver.group()
                    break
                i += 1

        # Puertos
        if "Resumen puertos" in data[i]:
            ports = ""
            while "___" not in data[i]:
                port = re.search(r"\d+ \w+(?:-?\w+)*", data[i])
                if port:
                    port = port.group().replace(" ", ",")
                    ports += f"{port}\n"
                i += 1
            info["ports"] = ports.strip()
            last_i = i

    # Programs and its versions separated by commas
    all_software = ""
    for key, value in software.items():
        all_software += f"{key};{value}\n"
    all_software = all_software.strip()

    # The rest
    for line in data[last_i:]:
        last_lines += line

    return f"""\
┌───────┐
│Resumen│
└───────┘
─ Servidor ─
{info["dns"]}
{info["host"]}
{info["ip"]}

{info["os"]}
{info["tipo"]}

─ Características ─
{info["ram"]}
{info["cpu"]}
{info["disk"]}

─ Versiones de programas ({len(software)}) ─
{all_software}

┌───────┐
│Puertos│
└───────┘
{info["ports"]}

┌────────┐
│Usuarios│
└────────┘
...

┌─────┐
│Rutas│
└─────┘
{last_lines}
"""
