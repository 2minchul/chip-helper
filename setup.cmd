@echo off
pushd %~dp0

echo making venv ...
py -3 -m venv venv
venv\Scripts\pip install -U -r requirements.txt -i http://ftp.daumkakao.com/pypi/simple --trusted-host ftp.daumkakao.com
echo finish!
pause