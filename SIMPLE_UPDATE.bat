@echo off
cd /d "%~dp0"

echo Stopping Python...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 > nul

echo Clearing cache...
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

echo Downloading...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py' -OutFile 'src\main.py' -UseBasicParsing" 2>nul
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt' -OutFile 'VERSION.txt' -UseBasicParsing" 2>nul

echo.
echo Done! Version:
type VERSION.txt
echo.
echo Start: python -B -u -m src.main --mode paper
echo.

pause
