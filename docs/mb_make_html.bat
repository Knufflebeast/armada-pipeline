@echo off&setlocal

:: Run this script before mb_start_server

set _DOC_DIR=%~dp0

:: Get project root dir
for %%i in ("%_DOC_DIR%\..") do set "_ROOT_DIR=%%~fi"
echo %_ROOT_DIR%
:: Get venv activate path
set _VENV_DIR=%_ROOT_DIR%\venv\Scripts

:: Activate the venv and execute the launcher script
cmd /k "cd /d %_VENV_DIR% & activate & cd /d %_DOC_DIR% & make html" 
