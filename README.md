# auto_link

**auto_link** es una aplicación de terminal desarrollada en Python que permite comprobar si las URL contenidas en un archivo HTML son válidas y conducen a sitios web accesibles.

## Instalación y ejecución

Para ejecutar la aplicación como un programa independiente desde la terminal, primero hay que darle permisos de ejecución:

```bash
chmod +x auto_link.py
```

Si se desea ejecutar el programa desde cualquier directorio mediante el comando `auto_link`, es necesario mover el archivo a la ruta `/usr/local/bin/` y asegurarse de que tenga los permisos adecuados.

También se puede ejecutar directamente con Python desde el directorio en el que se encuentre el archivo:

```bash
python3 auto_link.py archivo.html
```

Una vez instalado correctamente, se podrá utilizar de la siguiente manera:

```bash
auto_link archivo.html
```

## Requisitos

La aplicación necesita Python 3 y las siguientes dependencias:

```bash
pip install requests beautifulsoup4
```

## Funciones principales

- **Detección de enlaces rotos:** identifica enlaces que devuelven errores HTTP 4xx o 5xx.
- **Filtrado de enlaces:** ignora enlaces internos del documento y enlaces JavaScript que no corresponden a URL web convencionales.
- **Eliminación de enlaces rotos:** permite al usuario eliminar los enlaces detectados como rotos si así lo desea.
- **Generación de HTML limpio:** crea una versión del archivo HTML sin los enlaces rotos que se hayan eliminado.

## Comando de uso

La aplicación recibe como argumento la ruta del archivo HTML que se desea analizar:

```bash
python3 auto_link.py archivo.html
```

Si se ha instalado correctamente en `/usr/local/bin/`, también se puede ejecutar mediante:

```bash
auto_link archivo.html
```

**Objetivo del proyecto:** automatizar la comprobación de enlaces en archivos HTML, facilitar la detección de URL inaccesibles y permitir la limpieza del documento de forma sencilla desde la terminal.
