@echo off&setlocal

:: Go to http://localhost:8000/_build/html/ to see docs

echo Starting local doc server...
cmd /k "python -m SimpleHTTPServer"
