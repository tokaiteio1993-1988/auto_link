#!/usr/bin/env python3
"""
auto_link_personal - Versión turbo con insultos sanos, multihilo y soporte para carpetas.
"""

import argparse
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Colores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"


class LinkCheckerPersonal:
    def __init__(self, timeout=8):
        self.timeout = timeout
        self.cache = {}
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def check_url(self, url):
        with self.lock:
            if url in self.cache:
                return self.cache[url]

        try:
            r = self.session.head(url, allow_redirects=True, timeout=self.timeout)
            if r.status_code in (400, 403, 404, 405) or r.status_code >= 500:
                r = self.session.get(url, allow_redirects=True, timeout=self.timeout, stream=True)
                r.close()

            is_ok = r.status_code < 400
            res = (is_ok, f"HTTP {r.status_code}")
        except requests.exceptions.Timeout:
            res = (False, f"Tiempo de espera agotado ({self.timeout}s)")
        except requests.exceptions.SSLError:
            res = (False, "Fallo de certificado SSL")
        except requests.exceptions.ConnectionError:
            res = (False, "Murió la conexión o no existe el dominio")
        except Exception as e:
            res = (False, f"Fallo desconocido ({type(e).__name__})")

        with self.lock:
            self.cache[url] = res
        return res


def buscar_archivos_html(ruta, recursivo=False):
    if os.path.isfile(ruta):
        if not ruta.lower().endswith((".html", ".htm")):
            print(f"{RED}error, e dado error porque eres tonto y me has pasado un archivo que no es un html cabezon.{RESET}")
            return []
        return [os.path.abspath(ruta)]

    if os.path.isdir(ruta):
        encontrados = []
        if recursivo:
            for raiz, _, archivos in os.walk(ruta):
                for f in archivos:
                    if f.lower().endswith((".html", ".htm")):
                        encontrados.append(os.path.abspath(os.path.join(raiz, f)))
        else:
            for item in os.listdir(ruta):
                completo = os.path.join(ruta, item)
                if os.path.isfile(completo) and item.lower().endswith((".html", ".htm")):
                    encontrados.append(os.path.abspath(completo))
        encontrados.sort()
        return encontrados

    print(f"{RED}no lo encuentro cabeza almendra ¿existe? ¿es la ruta? ¿está mal escrito?: '{ruta}'{RESET}")
    return []


def procesar_archivo(html_file, checker, workers=10):
    print(f"\n{BOLD}{CYAN}------------------------------------------------------------{RESET}")
    print(f"{BOLD}Mirando el archivo: {WHITE}{html_file}{RESET}")
    print(f"{BOLD}{CYAN}------------------------------------------------------------{RESET}")

    try:
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"{RED}ni leerlo puedo: {e}{RESET}")
        return

    enlaces_candidatos = []
    skipped_count = 0

    for link in soup.find_all("a", href=True):
        url = link["href"].strip()
        if not url or url.startswith("#"):
            continue

        parsed = urlparse(url)
        if parsed.scheme in ("javascript", "mailto", "tel", "sms"):
            continue

        if parsed.scheme not in ("http", "https"):
            skipped_count += 1
            continue

        enlaces_candidatos.append((link, url))

    total = len(enlaces_candidatos)
    print(f"Total de enlaces a revisar: {WHITE}{total}{RESET}")
    if skipped_count:
        print(f"[i] Enlaces locales ignorados: {skipped_count}")

    if total == 0:
        print(f"{GREEN}[+] Ni un solo enlace web para revisar.{RESET}")
        return

    print(f"\n{BLUE}[+] Comprobando {total} enlaces a toda mecha ({workers} hilos en paralelo)...{RESET}\n")

    broken_links = []
    lock_print = threading.Lock()
    hechos = 0

    def comprobar_tarea(item):
        link_tag, url = item
        is_ok, motivo = checker.check_url(url)
        return link_tag, url, is_ok, motivo

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(comprobar_tarea, item) for item in enlaces_candidatos]
        for f in as_completed(futures):
            link_tag, url, is_ok, motivo = f.result()
            with lock_print:
                hechos += 1
                progreso = f"[{hechos}/{total}]"
                if is_ok:
                    print(f"{progreso} {WHITE}{url}{RESET} -> {GREEN}:) OK ({motivo}){RESET}")
                else:
                    print(f"{progreso} {WHITE}{url}{RESET} -> {RED}:( ROTO ({motivo}){RESET}")
                    broken_links.append((link_tag, url, motivo))

    print(f"\n[+] Enlaces rotos encontrados: {len(broken_links)}")

    if broken_links:
        print("\n¿Qué hacemos con los rotos?")
        print(" 1. Desenlazar (quitar enlace pero NO borrar el texto) [Recomendado]")
        print(" 2. Borrar etiqueta y texto del enlace a lo bruto")
        print(" n. No tocar nada")

        choice = input("\nElige (1/2/n): ").strip().lower()

        if choice in ("1", "s", "si", "sí", ""):
            for tag, _, _ in broken_links:
                tag.unwrap()
        elif choice in ("2", "borrar", "eliminar", "decompose"):
            for tag, _, _ in broken_links:
                tag.decompose()
        else:
            print("[+] No se eliminó nada, cobarde.")
            return

        directorio = os.path.dirname(html_file)
        nombre_base = "cleaned_" + os.path.basename(html_file)
        output_file = os.path.join(directorio, nombre_base) if directorio else nombre_base

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(soup))

        print(f"{GREEN}[+] Archivo guardado: {output_file}{RESET}")
    else:
        print(f"{GREEN}[+] No hay enlaces rotos, milagro.{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="auto_link versión personal (con insultos y a toda mecha)."
    )
    parser.add_argument("ruta", nargs="?", default=None, help="Archivo HTML o carpeta con HTMLs")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Buscar en subcarpetas")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Hilos concurrentes (por defecto: 10)")
    parser.add_argument("-t", "--timeout", type=int, default=8, help="Timeout en segundos (por defecto: 8)")

    args = parser.parse_args()

    if not args.ruta:
        print(f"{RED}cabeza almendra, pasa un archivo o carpeta. Ej: auto_link_personal index.html{RESET}")
        sys.exit(1)

    archivos = buscar_archivos_html(args.ruta, recursivo=args.recursivo)
    if not archivos:
        sys.exit(1)

    checker = LinkCheckerPersonal(timeout=args.timeout)

    for arch in archivos:
        procesar_archivo(arch, checker, workers=args.workers)

    print(f"\n{BOLD}{GREEN}[✓] Terminado todo, máquina.{RESET}\n")


if __name__ == "__main__":
    main()
