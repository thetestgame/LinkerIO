@echo off
title Linkify - Update Serverless
cd ../
goto :INPUT

rem Request user input
:INPUT
    set ENVIRONMENT=dev
    set /P ENVIRONMENT=Environment (dev [Default], test, prod):
    goto :DEPLOY

rem Deploy to environment
:DEPLOY
    echo Activating environment.
    CALL "env/Scripts/activate.bat"

    echo Deploying update...
    zappa update %ENVIRONMENT%

    echo Done!
    pause