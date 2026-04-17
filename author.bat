@echo off
cd /d "%~dp0"
start http://localhost:5000
python authoring/server.py
pause
