@echo off
title Linkify - Tornado Server
cd ../
goto :INPUT

rem Request user input
:INPUT
    set ENVIRONMENT=dev
    set /P ENVIRONMENT=Environment (dev [Default], test, prod):
    goto :RUN

rem Start HTTP/HTTPS server
:RUN
    echo Activating environment.
    CALL "env/Scripts/activate.bat"

    echo Starting tornado server
    python manage.py --tornado --env %ENVIRONMENT% %*

    echo "Press any key to restart."
    pause
    goto :RUN