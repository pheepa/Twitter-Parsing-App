@echo off
@rem это комментарий 
@rem echo - речатает на экран  %~dp0TwitterParsing

start %USERPROFILE%\AppData\Local\Programs\TwitterParsing\TwitterParsing.exe

cd back
python manage.py runserver




pause
exit
