# Revisión total (Versión y Listos para migrar)

## Tabla de contenidos

  * [Consideraciones](#consideraciones)
    * [Revisión del sistema operativo](#revisión-del-sistema-operativo)
    * [Revisión de migración](#revisión-de-migración)
      * [Condición 1: Puertos y procesos asociados](#condición-2-puertos-y-procesos-asociados)
      * [Condición 2: Aplicaciones y/o base de datos](#condición-3-aplicaciones-yo-base-de-datos)

## Consideraciones

### Revisión del sistema operativo

- Considerar solo RHEL
- Versiones deben ser `^8.0`

_Ejemplo:_

| S.O                                  | Validez |
|--------------------------------------|---------|
| Red Hat Enterprise Linux release 8.9 | ✅       |
| Red Hat Enterprise Linux release 9.2 | ❌       |
| Red Hat Enterprise Linux release 7.8 | ❌       |

### Revisión de migración

Se deben de cumplir 3 condiciones para que el check sea marcado

#### Condición 1: Sistema operativo

Ver [tabla de S.O](#revisión-de-migración) arriba.

#### Condición 2: Puertos y procesos asociados

> Revisar en la hoja `Puerto por Aplicaciones`

| Pauta                                            | Validez |
|--------------------------------------------------|---------|
| Se encuentra alguno de los servicios permitidos* | ✅       |
| Se encuentra alguno de los servicios prohibidos* | ❌       |


- _* Servicios permitidos: `nessus`, `ha-proxy`, `sensor`, `sshd`_.
- _* Servicios prohibidos: `xinetd`, `httpd`_.

#### Condición 3: Aplicaciones y/o base de datos

> Revisar en las siguientes hojas:
> - `Resumen` o `Paquetes Instalados`
> - `Puerto por Aplicaciones`
> - `BD`

No debe tener base de datos y/o aplicaciones

| Pauta                                                             | Validez |
|-------------------------------------------------------------------|---------|
| Hay base de datos en la hoja _'BD'_                               | ❌       |
| Tiene algún gestor de base de datos **con** puerto(s) asociado(s) | ❌       |
| Tiene algún aplicativo **con** puerto(s) asociado(s)              | ❌       |
| Tiene algún gestor de base de datos **sin** puerto(s) asociado(s) | ✅       |
| Tiene algún aplicativo **sin** puerto(s) asociado(s)              | ✅       |

_Ejemplos_

- **_Uno:_** No se pone el check
    - **Condición 1:** ✅ _(Se encuentra el proceso `sshd`)_
    - **Condición 2:** ❌ _(Se lista `PostreSQL` con puerto(s) asociado(s): `5432, postmaster`)_
    - **Condición 2:** ✅ _(Se lista `Python` sin puerto(s) asociado(s))_
    - **Condición 2:** ✅ _(No hay contenido en la hoja 'BD')_

    ```text
    # Hoja `Resumen`
    Características
    PostreSQL   8.1.23
    Python	    2.7, 3.6

    # Hoja `Puerto por Aplicaciones`
    5012  trace-agent
    22    sshd
    5432  postmaster
    32505 ClMgrS

    # Hoja `BD`
    # Vacía
    ```

- **_Dos:_** Si se pone el check
    - **Condición 1:** ✅ _(Se encuentra el proceso `sshd`)_
    - **Condición 2:** ✅ _(Se lista `PostreSQL` pero no tiene un puerto asociado)_
    - **Condición 2:** ✅ _(Se lista `Python` sin puerto(s) asociado(s))_
    - **Condición 2:** ✅ _(No hay contenido en la hoja 'BD')_

    ```text
    # Hoja `Resumen`
    Características
    PostreSQL   8.1.23
    Python	    2.7, 3.6

    # Puerto por Aplicaciones
    5012  trace-agent
    22    sshd
    32505 ClMgrS

    # Hoja `BD`
    # Vacía
    ```

- **_Tres:_** No se pone el check
    - **Condición 1:** ✅ _(Se encuentra el proceso `sshd`)_
    - **Condición 2:** ✅ _(Se lista `PostreSQL` pero no tiene un puerto asociado)_
    - **Condición 2:** ❌ _(Hay contenido en la hoja 'BD')_

    ```text
    # Hoja `Resumen`
    Características
    PostreSQL   8.1.23

    # Puerto por Aplicaciones
    5012  trace-agent
    22    sshd

    # Hoja `BD`
    ARVAACTUAL               MARIO ROMERO FUENTES
    CARTERA	                 MARIO ROMERO FUENTES
    INTERNET                 MARIO ROMERO FUENTES
    INTRANET_ADMINISTRACION  MARIO ROMERO FUENTES
    NOMINAINVERSA	         MARIO ROMERO FUENTES
    SORTEO                   MARIO ROMERO FUENTES
    TELECOM                  MARIO ROMERO FUENTES
    ```


