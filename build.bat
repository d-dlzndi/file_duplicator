@echo off
@chcp 65001 1> NUL 2> NUL

cd /d %~dp0

uv sync
uv run hatch build --hooks-only

@REM uv run pyinstaller --noconfirm --noconsole --onedir --clean --name "File Duplicator" --add-data "app_icon.ico;." --icon="app_icon.ico" main.py

uv run pyinstaller  --noconfirm  --noconsole  --onedir  --clean  --name "File-Duplicator-LocalBuild"  --add-data "app_icon.ico;."  --icon="app_icon.ico"  main.py