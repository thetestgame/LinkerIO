@echo off
title Linkify - Dev Server
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

    echo Starting development server
    python manage.py --env %ENVIRONMENT% %*
    
    echo "Press any key to restart."
    pause
    goto :RUN