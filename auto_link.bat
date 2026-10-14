@echo off
:: ==============================================================================
:: auto_link - Safe Windows Command Launcher
:: ==============================================================================
:: This is a safe launcher script for Windows.
:: Purpose: Allows running 'auto_link <file.html>' directly in CMD/PowerShell
:: without having to manually type 'python auto_link.py'.
::
:: Safety & Security:
:: - 100% transparent: only forwards arguments to the local auto_link.py script.
:: - Requires NO administrator or elevated privileges.
:: - Does NOT touch system settings, registry, or download unauthorized binaries.
:: ==============================================================================

python "%~dp0auto_link.py" %*
