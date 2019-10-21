#!/bin/bash
args=("$@")

function goto
{
    label=$1
    cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}

#@echo off
title Linkify - Update Serverless
cd ../
goto :INPUT

#  Request user input

goto INPUT
INPUT:

    export  ENVIRONMENT=dev
 read -p "Environment (dev [Default], test, prod):" ENVIRONMENT 
    goto :TAIL

#  Run Tail

goto TAIL
TAIL:

    zappa tail $ENVIRONMENT $*

    sleep 
    goto :EOF