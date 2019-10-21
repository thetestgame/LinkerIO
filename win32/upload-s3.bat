@echo off
title Linkify - Upload S3 assets
cd ../

rem Upload Assets
:main 
    echo Activating environment.
    CALL "env/Scripts/activate.bat"

    echo Starting upload.
    python manage.py --upload-s3

    echo Complete
    pause