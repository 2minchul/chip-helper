@echo off
pushd %~dp0

echo making venv ...
py -3 -m venv venv
venv\Scripts\pip install -r requirements.txt
echo finish!
pause