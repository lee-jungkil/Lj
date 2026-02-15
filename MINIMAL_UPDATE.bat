@echo off
cd /d "%~dp0"
echo Stopping Python...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul
echo Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo Downloading main.py...
curl -s -L "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py" -o "src\main.py"
echo Downloading VERSION.txt...
curl -s -L "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt" -o "VERSION.txt"
echo.
echo Done! Version:
type VERSION.txt
echo.
echo Start: python -B -u -m src.main --mode paper
pause
