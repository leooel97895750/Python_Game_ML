@echo off

for /l %%x in (1, 1, 10000) do (
   echo %%x
   start race.bat
   timeout /t 10
)
   

