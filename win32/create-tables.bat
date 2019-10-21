@echo off
title Linkify - Create Dynamodb Tables
cd ../

rem Upload Assets
:main 
    echo Activating environment.
    CALL "env/Scripts/activate.bat"

    echo Creating tables.
    python manage.py --create-tables

    echo Complete
    pause