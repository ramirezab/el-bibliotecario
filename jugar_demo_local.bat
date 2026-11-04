@echo off
rem Abre la demo jugable en tu navegador desde esta carpeta (sin GitHub Pages).
cd /d "%~dp0"
start "" "http://localhost:8765/demo/index.html"
python -m http.server 8765
