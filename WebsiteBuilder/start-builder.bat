@echo off
title WebsiteBuilder Launcher
chcp 65001 >nul

cls
echo ===========================================
echo          Welcome to WebsiteBuilder        
echo ===========================================
echo.
timeout /t 2 >nul
cls

echo =========================================
echo      WebsiteBuilder Debug Terminal       
echo -----------------------------------------
echo       [33m[ Press CTRL + C To Exit ][0m
echo =========================================
echo.
timeout /t 1 >nul
start "" "http://127.0.0.1:5000"
call python dashboard.py | call python webserver.py
