# auto_link 

**auto_link** is a fast, multi-threaded CLI tool built with Python to analyze hyperlinks inside HTML files or entire directory trees, detect broken or inaccessible links (HTTP errors, timeouts, SSL issues), and clean or repair them automatically without damaging the document's structure.

---

##  Installation & Requirements

### Prerequisites
Requires **Python 3.8+**. Install dependencies:

```bash
pip install -r requirements.txt
```

### Linux / macOS
Run the automated installer:
```bash
chmod +x install.sh
./install.sh
```
*(Runs as standard user to install in `~/.local/bin`, or with `sudo ./install.sh` for system-wide `/usr/local/bin`).*

### Windows
You can run it directly with:
```powershell
python auto_link.py document.html
```
Or use the convenience launcher `auto_link.bat`:
```cmd
auto_link document.html
```

####  About `auto_link.bat` (Safety & Transparency)
On Windows, `.bat` batch files can sometimes look unfamiliar or suspicious. **`auto_link.bat` is 100% safe, transparent, and open-source:**
* **What does it do?** It simply forwards arguments to Python: `python "%~dp0auto_link.py" %*`. This lets you run `auto_link` like a native command without typing `python auto_link.py` every time.
* **No administrator rights needed:** It never requests or requires elevated administrator privileges.
* **No system changes:** It does not modify Windows system files, PATH, or the registry.
* **Fully auditable:** You can open `auto_link.bat` in Notepad at any time to verify its single command line.

---

##  Usage & Examples

### 1. Check a single file
```bash
auto_link index.html
```

### 2. Scan an entire directory
Scan all `.html` files in a folder:
```bash
auto_link ./my_website/
```
Scan subdirectories recursively:
```bash
auto_link ./my_website/ -r
```

### 3. Faster checking (concurrency)
Check with 20 parallel threads (default is 10):
```bash
auto_link document.html -w 20
```

### 4. Non-interactive / CI-CD mode
Automatically unwrap broken links (remove `<a>` tag, keep text) and overwrite in place (with automatic `.bak` backup):
```bash
auto_link index.html --in-place --unwrap
```

### 5. Self-update to the latest version
Fetch and install the latest version directly from GitHub:
```bash
auto_link --update
```

---

##  CLI Options & Flags

| Flag | Description |
|---|---|
| `target` | Path to an HTML file or a directory containing HTML files |
| `-r, --recursive` | Recursively scan subdirectories for HTML files |
| `-w, --workers <N>` | Number of parallel checking threads (default: `10`) |
| `-t, --timeout <S>` | Request timeout in seconds (default: `8`) |
| `-o, --output <PATH>`| Custom output file or directory path |
| `-i, --in-place` | Overwrite original file in-place (creates `.bak` backup) |
| `--unwrap` | Automatically unwrap broken links (non-interactive) |
| `--decompose` | Automatically remove broken link tags completely |
| `--check-local` | Verify if referenced local files exist on disk |
| `--update` | Check GitHub for updates and self-update |
| `-v, --version` | Display version number |

---

##  Key Features

* **Multi-threaded Performance:** Concurrent checks with connection pooling (`requests.Session`) and thread-safe caching to skip duplicate URLs.
* **Directory Support:** Check single files or entire folders recursively.
* **Smart Detection:** Fast `HEAD` requests with automatic fallback to `GET (stream)`. Catches HTTP 4xx/5xx, timeouts, DNS/connection issues, and SSL errors.
* **Non-destructive Cleaning (`unwrap`):** Preserves original text content so sentences remain natural.
* **Interactive URL Replacement:** Option to supply a replacement URL on the fly.
* **Self-updating:** Easily stay on the latest version using `auto_link --update`.

---

##  Repository Structure

* [`auto_link.py`](auto_link.py): Main multi-threaded CLI script.
* [`install.sh`](install.sh): Linux/macOS installer for `auto_link`.
* [`auto_link.bat`](auto_link.bat): Windows command runner.
* [`requirements.txt`](requirements.txt): Python dependencies.

---

## ¿Te ha sido útil auto_link? / Was auto_link useful to you?

Tu opinión es muy importante para seguir mejorando la herramienta:

|  **Sí, me ha sido útil / Yes, it worked great!** | 🔧 **No, algo falló / No, something could be better** |
|:---:|:---:|
| **¡Gracias por usar la aplicación!**<br>Si te sirvió, apoya el proyecto dándole una estrella ⭐ en GitHub:<br><br>[⭐ Dar estrella al repositorio](https://github.com/tokaiteio1993-1988/auto_link) | **Por favor, ve a la sección de Issues**<br>Reporta el fallo o propón mejoras en el repositorio:<br><br>[ Ver Issues en GitHub](https://github.com/tokaiteio1993-1988/auto_link/issues) &nbsp;•&nbsp; [ Abrir nuevo Issue](https://github.com/tokaiteio1993-1988/auto_link/issues/new) |

> Enlace oficial del repositorio: [https://github.com/tokaiteio1993-1988/auto_link](https://github.com/tokaiteio1993-1988/auto_link)

