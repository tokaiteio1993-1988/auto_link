#!/usr/bin/env bash
# ============================================================
# Instalador de auto_link (Versión Personal)
# ============================================================

set -e

echo "=== Instalando auto_link (Versión Personal con insultos sanos) ==="
echo ""

SOURCE_FILE="auto_link_personal.py"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: No encuentro $SOURCE_FILE en este directorio, cabeza de chorlito."
    exit 1
fi

# Determinar directorio de instalación
if [ "$EUID" -eq 0 ]; then
    TARGET_DIR="/usr/local/bin"
else
    TARGET_DIR="$HOME/.local/bin"
    mkdir -p "$TARGET_DIR"
fi

TARGET_BIN="$TARGET_DIR/auto_link"

echo "[+] Copiando tu versión personal a $TARGET_BIN..."
cp "$SOURCE_FILE" "$TARGET_BIN"
chmod +x "$TARGET_BIN"

echo ""
echo "[✓] ¡Listo! Tu versión personal ya está instalada como 'auto_link'."
echo "Ahora puedes usar directamente:"
echo "    auto_link archivo.html"
echo ""

# Aviso sobre PATH si se instaló en ~/.local/bin
if [ "$EUID" -ne 0 ]; then
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "Aviso: ~/.local/bin no está en tu PATH. Pon esto en tu ~/.bashrc o ~/.zshrc:"
        echo '    export PATH="$HOME/.local/bin:$PATH"'
    fi
fi
