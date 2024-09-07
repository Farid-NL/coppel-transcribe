# Server info extractor

Extrae la información de los servidores en un archivo de texto único para su fácil traspaso.

![License](https://img.shields.io/badge/License-WTFPL-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<!-- TOC -->
* [Server info extractor](#server-info-extractor)
  * [Uso](#uso)
  * [Roadmap](#roadmap)
    * [General](#general)
    * [Windows](#windows)
    * [Linux](#linux)
<!-- TOC -->

## Uso

TBD

## Roadmap

### General

- [ ] Recibe `IP`, `Tipo` y `Etapa`
- [ ] Recibe un csv con 2 columnas `IP`, `Tipo` y `Etapa`
  
  | IP           | Tipo    | Etapa |
  |--------------|---------|-------|
  | 10.30.1.124  | Windows | 1     |
  | 10.20.100.25 | Linux   | Full  |
  
  ```text
  IP,Tipo,Etapa
  10.30.1.124,Windows,1
  10.20.100.25,Linux,Full
  ```

- Genera txt con todas las ips a buscar y su información correspondiente
- Buenas prácticas
  - [ ] Documentación
  - [ ] Type hinting
  - [ ] Estructura del proyecto para scripts

### Windows

- **Manejo de archivos `zip`**
  - [ ] Extracción de único zip
  - [ ] Extracción a carpeta con el mismo nombre del archivo
  - [ ] Extracción de multiples zip
  - [ ] Revisar que los archivos txt correspondan al nombre del zip


- **Manejo de archivos `txt`**
  - [ ] Extraer info de `systeminfo_X.X.X.X.txt`
    - Host Name
    - OS Name + OS Version
    - Processor
      - Nombre + #
    - Total Physical Memory
  - [ ] Extraer info de `discos_X.X.X.X.txt`
    - Eliminar líneas vacías
    - Eliminar espacios finales
  - [ ] Extraer info de `puertos_X.X.X.X.txt`
    - Convertir a CSV temporalmente
    - Conservar solo la columna _Local Address_
    - Eliminar IP (`X.X.X.X`) y `:`
    - Eliminar duplicados
  - [ ] Extraer info de `programas_instalados_X.X.X.X.txt`
    - Convertir a CSV temporalmente
    - Conservar solo las columnas _Name_ y _Version_
    - Conservar entradas hasta encontrar `Security Intelligence Updat...`

### Linux