py -m venv env
call ".\env\Scripts\activate.bat"
py -m pip install -r requirements.txt
py -m spacy download en_core_web_sm
deactivate