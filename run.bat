cd ".\main\"
start runserver.bat
cd "..\coref\"
start runserver.bat
timeout /t 5
start "" http://localhost:8000/converter/stories
exit