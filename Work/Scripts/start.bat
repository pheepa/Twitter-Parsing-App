@echo off

start %USERPROFILE%\AppData\Local\Programs\TwitterParsing\TwitterParsing.exe > nul  ^&  exit

cd back

call activate base

python manage.py runserver

call conda deactivate

exit
