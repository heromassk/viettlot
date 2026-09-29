@echo off
setlocal
set TS=%RANDOM%%RANDOM%
start "" "file:///%~dp0index.html?nocache=%TS%"
