@echo off

echo NumPad - Windows Build Script
echo ================================

echo Creating conda environment...
call conda env create -f environment.yml

echo Activating environment...
call conda activate numpad

echo Running build script...
call python build.py

echo Deactivating environment...
call conda deactivate