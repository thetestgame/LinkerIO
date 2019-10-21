@echo off
title Linkify - Create Environment
cd ../

rem Create and switch to Python environment
echo Creating environment.
virtualenv env
CALL "env/Scripts/activate.bat"

rem Install dependencies
echo Installing dependencies
pip install -r requirements.txt

rem Inform user of completion and wait
echo Environment created.
pause