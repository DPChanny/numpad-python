@echo off

echo NumPad - Windows Build Script
echo ================================

cd /d "%~dp0.."

echo Creating conda environment...
call conda env create -f environment.yml

echo Activating environment...
call conda activate numpad

echo Running build script...
call python scripts\build.py

echo Deactivating environment...
call conda deactivate

echo.
echo Build completed! Check the dist\ directory for the executable.
pause