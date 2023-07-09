@ECHO OFF

:venv_configured_question
cls
set /p "venv_configured=Do you have configured a venv in this repo(y/n): "

IF NOT "%venv_configured%"=="y" IF NOT "%venv_configured%"=="n" GOTO venv_configured_question

IF "%venv_configured%"=="y" SET python = .\venv\Scripts\python.exe
IF "%venv_configured%"=="n" SET python = python

cls
%python % -m pip install -r requirements.txt

IF "%ERRORLEVEL%"=="0" GOTO END

set /p "python_new_quoted=Enter the path to your python exe: "

%python_new_quoted% -m pip install -r requirements.txt

:END
PAUSE