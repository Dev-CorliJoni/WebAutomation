@ECHO OFF

:venv_configured_question
cls
set /p "venv_configured=Do you have configured a venv in this repo(y/n): "

IF NOT "%venv_configured%"=="y" IF NOT "%venv_configured%"=="n" GOTO venv_configured_question

IF "%venv_configured%"=="y" SET python = .\venv\Scripts\python.exe
IF "%venv_configured%"=="n" SET python = python

cls
SET script = .\main.py

set /p "configuration_path=Enter the configuration file you want to start: "
GOTO execute_python

:ask_for_python_path

set /p "python_new_quoted=Enter the path to your python exe: "
IF %python_new_quoted:~0,1%%python_new_quoted:~-1% == "" SET python_new=%python_new_quoted:~1,-1%
IF NOT %python_new_quoted:~0,1%%python_new_quoted:~-1% == "" SET python_new=%python_new_quoted%

%python_new % %script % --configuration %configuration_path%
GOTO END

:execute_python
%python % %script % --configuration %configuration_path%

IF NOT "%ERRORLEVEL%"=="0" GOTO ask_for_python_path

:END
PAUSE