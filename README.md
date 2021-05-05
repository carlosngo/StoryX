# StoryX
A Django web application that uses spaCy NLP libraries to generate a screenplay document from a short story. 

Written for a thesis in partial fulfillment of the requirements for the degree of Bachelor of Science in Computer Science by <br/>

Garay, Kathleen Nicole <br/>
Kang, Jude Evan <br/>
Ngo, Carlos Miguel <br/>
Villaroman, Ma. Patricia <br/>

Advised by Ryan Austin Fernandez <br/>

## Pre-requisites
1. [Python 3.7.9](https://www.python.org/downloads/release/python-379/)
2. [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
3. TeX distribution software, preferably [TeX Live](http://www.tug.org/texlive/acquire-netinstall.html)
4. [screenplay](https://www.ctan.org/pkg/screenplay) package for your chosen TeX distribution software 

## How to run the project

### Easy setup

1. If it is your first time running the project, run `install.bat` from the root directory. Initial setup may take a while.
2. Run `run.bat` from the root directory.
3. The project webpage will be shown after a few seconds.

#### Unexpected behavior
1. If the webpage is unresponsive, refresh after 30 seconds.
2. If the webpage is still unresponsive, try the manual setup.

### Manual setup

#### Set up the API server
1. Go to the `coref` directory using the command prompt
2. Create and activate a Python 3.7.9 virtual environment
```
py -m venv env
.\env\Scripts\activate
```
3. Install dependencies
```
py -m pip install -r requirements.txt
```
4. Download spaCy pre-trained models
```
py -m spacy download en_core_web_sm
```
5. Run `py manage.py runserver`

#### Set up the main server
1. Go to the `main` directory using the command prompt
2. Create and activate a Python 3.7.9 virtual environment
```
py -m venv env
.\env\Scripts\activate
```
3. Install dependencies
```
py -m pip install -r requirements.txt
```
4. Download spaCy pre-trained models
```
py -m spacy download en_core_web_sm
```
5. Set up database
```
py manage.py makemigrations
py manage.py migrate
```
6. Run `py manage.py runserver`
7. Open your browser and enter the URL localhost:8000

#### Unexpected behavior
1. If an error occurs during the setup, please take a screenshot and contact the developers. Thank you.