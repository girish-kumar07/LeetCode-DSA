@echo off
powershell.exe -NoProfile -Command "$env:GITHUB_TOKEN=[Environment]::GetEnvironmentVariable('GITHUB_TOKEN','User'); Set-Location 'G:\LeetCode-DSA'; python -u '.\automation\server.py'"