#!/usr/bin/env bash
# ============================================================
# auto_link installation script for Linux / macOS
# ============================================================

set -e

echo "=== Installing auto_link ==="
echo ""

SOURCE_FILE="auto_link.py"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "[-] Error: $SOURCE_FILE not found in the current directory."
    exit 1
fi

# Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "[-] Error: python3 is not installed or not in PATH."
    exit 1
fi

# Optional dependency installation
if [ -f "requirements.txt" ]; then
    echo "[+] Installing required Python packages..."
    python3 -m pip install -r requirements.txt --quiet || true
fi

# Determine target directory
if [ "$EUID" -eq 0 ]; then
    TARGET_DIR="/usr/local/bin"
else
    TARGET_DIR="$HOME/.local/bin"
    mkdir -p "$TARGET_DIR"
fi

TARGET_BIN="$TARGET_DIR/auto_link"

echo "[+] Copying $SOURCE_FILE to $TARGET_BIN..."
cp "$SOURCE_FILE" "$TARGET_BIN"
chmod +x "$TARGET_BIN"

echo ""
echo "[✓] Installation successful!"
echo "You can now run auto_link anywhere:"
echo "    auto_link <file.html|folder> [options]"
echo "    auto_link --help"
echo "    auto_link --update"
echo ""

if [ "$EUID" -ne 0 ]; then
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "Notice: ~/.local/bin is not currently in your PATH."
        echo "Add it by placing this in your ~/.bashrc or ~/.zshrc:"
        echo '    export PATH="$HOME/.local/bin:$PATH"'
    fi
fi

