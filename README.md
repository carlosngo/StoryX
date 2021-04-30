# StoryX
A Django web application that uses Stanford's Stanza and CoreNLP libraries to generate a screenplay document from a short story. 

Written for a thesis in partial fulfillment of the requirements for the degree of Bachelor of Science in Computer Science by <br/>

Garay, Kathleen Nicole <br/>
Kang, Jude Evan <br/>
Ngo, Carlos Miguel <br/>
Villaroman, Ma. Patricia <br/>

Advised by Ryan Austin Fernandez <br/>

## Pre-requisites
1. Python 3.7.9
2. virtualenv

## How to run the project

### Set up the API server
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

### Set up the main server
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
