# Software Technology Department, Undergraduate Thesis Program

## Converting Short Stories Into Screenplays Through Abstract Story Representation

<div style="font-size: 1.17em;">Thesis Proponents</div>

| | | | | |
| ----------- | ----------- | ----------- | ----------- | ----------- | 
| <h3> ![Picture of Nicole](https://github.com/Losinek.png?size=150) </h3> | <h3> ![Picture of Jude](https://github.com/jude842.png?size=150) </h3> | <h3> ![Picture of Carlos](https://github.com/carlosngo.png?size=150) </h3> | <h3> ![Picture of Shasha](https://github.com/ShashaVillaroman.png?size=150) </h3> | <h3><img src="https://media.discordapp.net/attachments/674171433705799685/889074944154161152/unknown.png" alt="Picture of Austin" width="150"/> </h3> |
| Garay, Kathleen Nicole | Kang, Jude Evander | Ngo, Carlos Miguel | Villaroman, Ma. Patricia | Fernandez, Ryan Austin |
| Undergraduate Student | Undergraduate Student | Undergraduate Student | Undergraduate Student | Thesis Adviser |

## Table of Contents
- [Software Technology Department, Undergraduate Thesis Program](#software-technology-department-undergraduate-thesis-program)
  - [Converting Short Stories Into Screenplays Through Abstract Story Representation](#converting-short-stories-into-screenplays-through-abstract-story-representation)
  - [Table of Contents](#table-of-contents)
- [System Overview](#system-overview)
  - [System Features](#system-features)
    - [Convert Story to Screenplay](#convert-story-to-screenplay)
    - [Annotate Story Elements](#annotate-story-elements)
    - [View Story Extraction and Representation Results](#view-story-extraction-and-representation-results)
- [How to run the system](#how-to-run-the-system)
  - [System Prerequisites](#system-prerequisites)
  - [Easy setup](#easy-setup)
    - [Unexpected behavior](#unexpected-behavior)
  - [Manual setup](#manual-setup)
    - [Set up the coreference resolution server](#set-up-the-coreference-resolution-server)
    - [Set up the main server](#set-up-the-main-server)
    - [Unexpected behavior](#unexpected-behavior-1)
- [Research Overview](#research-overview)
  - [Abstract](#abstract)
  - [Research Document](#research-document)
- [Coref API Documentation](#coref-api-documentation)
  - [Get coreference clusters](#get-coreference-clusters)
    - [`GET /api/coref-clusters`](#get-apicoref-clusters)
      - [Parameters](#parameters)
      - [Returns](#returns)
- [Coref Class Documentation](#coref-class-documentation)
  - [`CorefResolver`](#corefresolver)
    - [`resolve_coreferences(text)`](#resolve_coreferencestext)
      - [Parameters](#parameters-1)
      - [Returns](#returns-1)
- [Main API Documentation](#main-api-documentation)
  - [View the landing page](#view-the-landing-page)
    - [`GET /converter/stories`](#get-converterstories)
      - [Parameters](#parameters-2)
      - [Returns](#returns-2)
  - [Generate the screenplay of a story](#generate-the-screenplay-of-a-story)
    - [`POST /converter/stories`](#post-converterstories)
      - [Parameters](#parameters-3)
      - [Returns](#returns-3)
  - [View the results of the element extraction module](#view-the-results-of-the-element-extraction-module)
    - [`GET /converter/stories/extraction-results`](#get-converterstoriesextraction-results)
      - [Parameters](#parameters-4)
      - [Returns](#returns-4)
  - [View the results of the element extraction module](#view-the-results-of-the-element-extraction-module-1)
    - [`GET /converter/stories/understanding-results`](#get-converterstoriesunderstanding-results)
      - [Parameters](#parameters-5)
      - [Returns](#returns-5)
  - [View the text file of a story](#view-the-text-file-of-a-story)
    - [`GET /converter/stories/:id/txt`](#get-converterstoriesidtxt)
      - [Parameters](#parameters-6)
      - [Returns](#returns-6)
  - [View the annotation page for a story](#view-the-annotation-page-for-a-story)
    - [`GET /converter/stories/:id/annotate`](#get-converterstoriesidannotate)
      - [Parameters](#parameters-7)
      - [Returns](#returns-7)
  - [View the extraction results page for a story](#view-the-extraction-results-page-for-a-story)
    - [`GET /converter/stories/:id/evaluate`](#get-converterstoriesidevaluate)
      - [Parameters](#parameters-8)
      - [Returns](#returns-8)
  - [View the generated screenplay for a story](#view-the-generated-screenplay-for-a-story)
    - [`GET /converter/stories/:id/screenplay`](#get-converterstoriesidscreenplay)
      - [Parameters](#parameters-9)
      - [Returns](#returns-9)
  - [Download the generated screenplay for a story as a PDF file](#download-the-generated-screenplay-for-a-story-as-a-pdf-file)
    - [`GET /converter/stories/:id/screenplay/pdf`](#get-converterstoriesidscreenplaypdf)
      - [Parameters](#parameters-10)
      - [Returns](#returns-10)
  - [Download the generated screenplay for a story as a TeX file](#download-the-generated-screenplay-for-a-story-as-a-tex-file)
    - [`GET /converter/stories/:id/screenplay/tex`](#get-converterstoriesidscreenplaytex)
      - [Parameters](#parameters-11)
      - [Returns](#returns-11)
- [Main Class Documentation](#main-class-documentation)
  - [`AnnotationHelper`](#annotationhelper)
    - [`process(text)`](#processtext)
      - [Parameters](#parameters-12)
      - [Returns](#returns-12)
  - [`ConceptNet`](#conceptnet)
    - [`checkIfProp(possibleCharacter, verb)`](#checkifproppossiblecharacter-verb)
      - [Parameters](#parameters-13)
      - [Returns](#returns-13)
    - [`checkIfNamedLocation(pobj)`](#checkifnamedlocationpobj)
      - [Parameters](#parameters-14)
      - [Returns](#returns-14)
    - [`checkForVerb(adp, verb)`](#checkforverbadp-verb)
      - [Parameters](#parameters-15)
      - [Returns](#returns-15)
  - [`CorefResolver`](#corefresolver-1)
    - [`resolve_coreferences(doc, data)`](#resolve_coreferencesdoc-data)
      - [Parameters](#parameters-16)
      - [Returns](#returns-16)
    - [`verify_resolution()`](#verify_resolution)
      - [Parameters](#parameters-17)
      - [Returns](#returns-17)
  - [`DialogueExtractor`](#dialogueextractor)
    - [`extract_dialogue(doc, story)`](#extract_dialoguedoc-story)
      - [Parameters](#parameters-18)
      - [Returns](#returns-18)
    - [`print_dialogue(dialogue)`](#print_dialoguedialogue)
      - [Parameters](#parameters-19)
      - [Returns](#returns-19)
    - [`get_speaker(start, end)`](#get_speakerstart-end)
      - [Parameters](#parameters-20)
      - [Returns](#returns-20)
    - [`extract_content()`](#extract_content)
      - [Parameters](#parameters-21)
      - [Returns](#returns-21)
    - [`extract_speakers()`](#extract_speakers)
      - [Parameters](#parameters-22)
      - [Returns](#returns-22)
    - [`resolve_speakers(mention_entity_dict)`](#resolve_speakersmention_entity_dict)
      - [Parameters](#parameters-23)
      - [Returns](#returns-23)
    - [`verify_dialogues()`](#verify_dialogues)
      - [Parameters](#parameters-24)
      - [Returns](#returns-24)
  - [`EntityExtractor`](#entityextractor)
    - [`extract_entities(doc, story, speakers)`](#extract_entitiesdoc-story-speakers)
      - [Parameters](#parameters-25)
      - [Returns](#returns-25)
    - [`get_distinct_entities(entities, doc)`](#get_distinct_entitiesentities-doc)
      - [Parameters](#parameters-26)
      - [Returns](#returns-26)
    - [`verify_characters()`](#verify_characters)
      - [Parameters](#parameters-27)
      - [Returns](#returns-27)
    - [`verify_props()`](#verify_props)
      - [Parameters](#parameters-28)
      - [Returns](#returns-28)
    - [`print_entity(entity)`](#print_entityentity)
      - [Parameters](#parameters-29)
      - [Returns](#returns-29)
    - [`get_character(start, end)`](#get_characterstart-end)
      - [Parameters](#parameters-30)
      - [Returns](#returns-30)
    - [`get_prop(start, end)`](#get_propstart-end)
      - [Parameters](#parameters-31)
      - [Returns](#returns-31)
    - [`resolve_characters(mention_entity_dict)`](#resolve_charactersmention_entity_dict)
      - [Parameters](#parameters-32)
      - [Returns](#returns-32)
    - [`resolve_props(mention_entity_dict)`](#resolve_propsmention_entity_dict)
      - [Parameters](#parameters-33)
      - [Returns](#returns-33)
  - [`ActionExtractor`](#actionextractor)
    - [`check_event_type(sentence, sent_characters, sent_props)`](#check_event_typesentence-sent_characters-sent_props)
      - [Parameters](#parameters-34)
      - [Returns](#returns-34)
    - [`parse_transition_sentence(sentence, idx, sent_characters, sent_props)`](#parse_transition_sentencesentence-idx-sent_characters-sent_props)
      - [Parameters](#parameters-35)
      - [Returns](#returns-35)
    - [`parse_action_sentence(sentence, idx, sent_characters, sent_props)`](#parse_action_sentencesentence-idx-sent_characters-sent_props)
      - [Parameters](#parameters-36)
      - [Returns](#returns-36)
    - [`extract_events(doc, story, dialogue_events, character_list, prop_list)`](#extract_eventsdoc-story-dialogue_events-character_list-prop_list)
      - [Parameters](#parameters-37)
      - [Returns](#returns-37)
    - [`verify_events()`](#verify_events)
      - [Parameters](#parameters-38)
      - [Returns](#returns-38)
  - [`ScreenplayGenerator`](#screenplaygenerator)
    - [`generate_screenplay()`](#generate_screenplay)
      - [Parameters](#parameters-39)
      - [Returns](#returns-39)
    - [`generate_tex()`](#generate_tex)
      - [Parameters](#parameters-40)
      - [Returns](#returns-40)
    - [`genetate_pdf()`](#genetate_pdf)
      - [Parameters](#parameters-41)
      - [Returns](#returns-41)
    - [`generate_tex_meta()`](#generate_tex_meta)
      - [Parameters](#parameters-42)
      - [Returns](#returns-42)
    - [`generate_tex_body()`](#generate_tex_body)
      - [Parameters](#parameters-43)
      - [Returns](#returns-43)
    - [`generate_tex_transition(transition_event)`](#generate_tex_transitiontransition_event)
      - [Parameters](#parameters-44)
      - [Returns](#returns-44)
    - [`generate_tex_action(action_event)`](#generate_tex_actionaction_event)
      - [Parameters](#parameters-45)
      - [Returns](#returns-45)
    - [`generate_tex_dialogue(dialogue_event)`](#generate_tex_dialoguedialogue_event)
      - [Parameters](#parameters-46)
      - [Returns](#returns-46)
  - [`SpacyUtil`](#spacyutil)
    - [`get_previous_token(token)`](#get_previous_tokentoken)
      - [Parameters](#parameters-47)
      - [Returns](#returns-47)
    - [`get_next_token(token)`](#get_next_tokentoken)
      - [Parameters](#parameters-48)
      - [Returns](#returns-48)
    - [`get_previous_word(token)`](#get_previous_wordtoken)
      - [Parameters](#parameters-49)
      - [Returns](#returns-49)
    - [`get_next_word(token)`](#get_next_wordtoken)
      - [Parameters](#parameters-50)
      - [Returns](#returns-50)
    - [`get_anchor(token)`](#get_anchortoken)
      - [Parameters](#parameters-51)
      - [Returns](#returns-51)
    - [`get_subject(anchor)`](#get_subjectanchor)
      - [Parameters](#parameters-52)
      - [Returns](#returns-52)
    - [`get_object(anchor)`](#get_objectanchor)
      - [Parameters](#parameters-53)
      - [Returns](#returns-53)
    - [`get_noun_chunk(noun)`](#get_noun_chunknoun)
      - [Parameters](#parameters-54)
      - [Returns](#returns-54)
    - [`get_sentence_index(sent)`](#get_sentence_indexsent)
      - [Parameters](#parameters-55)
      - [Returns](#returns-55)
  - [`StoryPresenter`](#storypresenter)
    - [`process()`](#process)
      - [Parameters](#parameters-56)
      - [Returns](#returns-56)
  - [`ExtractionEvaluator`](#extractionevaluator)
    - [`evaluate_extraction()`](#evaluate_extraction)
      - [Parameters](#parameters-57)
      - [Returns](#returns-57)
    - [`evaluate_dialogue_speaker(file)`](#evaluate_dialogue_speakerfile)
      - [Parameters](#parameters-58)
      - [Returns](#returns-58)
    - [`evaluate_dialogue_content(file)`](#evaluate_dialogue_contentfile)
      - [Parameters](#parameters-59)
      - [Returns](#returns-59)
    - [`evaluate_characters(file)`](#evaluate_charactersfile)
      - [Parameters](#parameters-60)
      - [Returns](#returns-60)
    - [`evaluate_props(file)`](#evaluate_propsfile)
      - [Parameters](#parameters-61)
      - [Returns](#returns-61)
    - [`evaluate_actions(file)`](#evaluate_actionsfile)
      - [Parameters](#parameters-62)
      - [Returns](#returns-62)
    - [`evaluate_transitions(file)`](#evaluate_transitionsfile)
      - [Parameters](#parameters-63)
      - [Returns](#returns-63)
    - [`count(prediction, annotation)`](#countprediction-annotation)
      - [Parameters](#parameters-64)
      - [Returns](#returns-64)
    - [`count_bianca(prediction, annotation)`](#count_biancaprediction-annotation)
      - [Parameters](#parameters-65)
      - [Returns](#returns-65)
    - [`evaluate(tp, fp, fn)`](#evaluatetp-fp-fn)
      - [Parameters](#parameters-66)
      - [Returns](#returns-66)
    - [`evaluate(perfect, missing, lacking, excess, missing, wrong)`](#evaluateperfect-missing-lacking-excess-missing-wrong)
      - [Parameters](#parameters-67)
      - [Returns](#returns-67)
  - [`UnderstandingEvaluator`](#understandingevaluator)
    - [`evaluate_understanding()`](#evaluate_understanding)
      - [Parameters](#parameters-68)
      - [Returns](#returns-68)
    - [`calculate_smc(x, y)`](#calculate_smcx-y)
      - [Parameters](#parameters-69)
      - [Returns](#returns-69)
    - [`calculate_jc(x, y)`](#calculate_jcx-y)
      - [Parameters](#parameters-70)
      - [Returns](#returns-70)
    - [`calculate_cs(x, y)`](#calculate_csx-y)
      - [Parameters](#parameters-71)
      - [Returns](#returns-71)
    - [`calculate_dot_product(x, y)`](#calculate_dot_productx-y)
      - [Parameters](#parameters-72)
      - [Returns](#returns-72)
    - [`calculate_length(x, y)`](#calculate_lengthx-y)
      - [Parameters](#parameters-73)
      - [Returns](#returns-73)
    - [`read_csv_file(csv_file)`](#read_csv_filecsv_file)
      - [Parameters](#parameters-74)
      - [Returns](#returns-74)
    - [`get_binary_representation(responses)`](#get_binary_representationresponses)
      - [Parameters](#parameters-75)
      - [Returns](#returns-75)

# System Overview

A system for screenwriters to generate a first draft of a screenplay adaptation from a short story. 

## System Features

### Convert Story to Screenplay

Convert a story to a screenplay in two simple steps:

1. Provide the title, author, and the story .txt file.

![Picture of Upload Page](https://drive.google.com/uc?export=view&id=1H9TktmQRLO4J3bojHn0cYMyeiSEYMWKt)

2. View and download the screenplay.

![Picture of Screenplay Page](https://drive.google.com/uc?export=view&id=1yihwrpFQSuoG6W40NZ7yszhjZoPJCB8o)

### Annotate Story Elements

For evaluation purposes, the system can be used to annotate story elements. 

![Picture of Annotation Page](https://drive.google.com/uc?export=view&id=1SHVQwD105R9MnasIuMaLeiXz__zZHmOO)

### View Story Extraction and Representation Results

The story representation results can be viewed. Metrics on the left require the story to be annotated first.  

![Picture of Results Page](https://drive.google.com/uc?export=view&id=1XaJJfBKt-H6YgzdzepftKsbft-H-Arnx)


# How to run the system

## System Prerequisites
1. [Python 3.7.9](https://www.python.org/downloads/release/python-379/)
2. [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
3. TeX distribution software, preferably [TeX Live](http://www.tug.org/texlive/acquire-netinstall.html)
4. [screenplay](https://www.ctan.org/pkg/screenplay) package for your chosen TeX distribution software 

## Easy setup

1. If it is your first time running the project, run `install.bat` from the root directory. Initial setup may take a while.
2. Run `run.bat` from the root directory.
3. The project webpage will be shown after a few seconds.

### Unexpected behavior
1. If the webpage is unresponsive, refresh after 30 seconds.
2. If the webpage is still unresponsive, try the manual setup.

## Manual setup

### Set up the coreference resolution server
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

### Unexpected behavior
1. If an error occurs during the setup, please take a screenshot and contact the developers. Thank you.

# Research Overview

## Abstract

A story is a series of events that can be represented in many ways. They are diverse and follow no strict format. The screenplay is a medium to tell stories clearly and straightforwardly. They focus on vital story elements that are ordered such that the story's meaning is retained. The conversion of stories into screenplays is currently time and human resource expensive due to the research and creativity needed to make a faithful adaptation. However, there are strategies in converting stories to screenplays that are repeatable for screenwriters. Thus, we created a system that automatically translates short stories into screenplays. Story elements were extracted and classified simultaneously and mapped to screenplay elements through abstract story representation. Of the story elements extracted, the system performed best with dialogue content and action lines, with precision, recall, and f1 scores above 60%. Readers were able to understand the screenplays across both corpora, performing with an above 60% similarity using Simple Matching Coefficient with story readers across all story elements.

## Research Document

The research document can be found [here](https://drive.google.com/file/d/1H7rBKoIqRntildEa-u5I1gcT1OebjSBp/view?usp=sharing). Please request access if prompted.

# Coref API Documentation

A lightweight REST API for coreference resolution in a text. Uses spaCy's neuralcoref library. 

## Get coreference clusters

### `GET /api/coref-clusters`

#### Parameters

`text` : `string`<br/>
The text to resolve coreferences from.

#### Returns

`coref`: JSON<br/>
A JSON object containing the coreference clusters found in the text. `coref[entity_start][entity_end]` returns a list of mentions, where each mention is 2-item list `[mention_start, mention_end]`. `*_start` and `*_end` are integers that represent the indices of the spaCy `Token` objects for the start and end of the noun phrase, respectively. 

# Coref Class Documentation

## `CorefResolver`

### `resolve_coreferences(text)`

#### Parameters

`text` : `string`<br/>
The text to resolve coreferences from.

#### Returns

`coref`: dict<br/>
A dictionary containing the coreference clusters found in the text. `coref[entity_start][entity_end]` returns a list of mentions, where each mention is 2-item list `[mention_start, mention_end]`. `*_start` and `*_end` are integers that represent the indices of the spaCy `Token` objects for the start and end of the noun phrase, respectively. 

# Main API Documentation

## View the landing page

### `GET /converter/stories`

#### Parameters

No parameters.

#### Returns

An HTML response of the landing page for the application.

## Generate the screenplay of a story

### `POST /converter/stories`

#### Parameters

`title` : `string`<br/>
The title of the story

`author` : `string`<br/>
The author of the story

`text_file` : `file`<br/>
The text file of the story

#### Returns

An HTML response of the screenplay page for the story.

## View the results of the element extraction module

### `GET /converter/stories/extraction-results`

#### Parameters

No parameters.

#### Returns

An HTML response of the page for the element extraction results.

## View the results of the element extraction module

### `GET /converter/stories/understanding-results`

#### Parameters

No parameters.

#### Returns

An HTML response of the page for the story understanding results.

## View the text file of a story

### `GET /converter/stories/:id/txt`

#### Parameters

`id` : `string`<br/>
Unique identifier for the story.

#### Returns

A plaintext HTTP response of the text file of the specified story.

## View the annotation page for a story

### `GET /converter/stories/:id/annotate`

#### Parameters

`id` : `string`<br/>
Unique identifier for the story.

#### Returns

An HTML response of the annotation page for the specific story.

## View the extraction results page for a story

### `GET /converter/stories/:id/evaluate`

#### Parameters

`id` : `string`<br/>
Unique identifier for the story.

#### Returns

An HTML response of the extraction results page for the specific story.

## View the generated screenplay for a story

### `GET /converter/stories/:id/screenplay`

#### Parameters

`id` : `string`<br/>
Unique identifier for the story.

#### Returns

An HTML response of the screenplay page for the specific story.

## Download the generated screenplay for a story as a PDF file

### `GET /converter/stories/:id/screenplay/pdf`

#### Parameters

`id` : `string`<br/>
Unique identifier for the story.

#### Returns

A downloadable .pdf file of the generated screenplay.

## Download the generated screenplay for a story as a TeX file

### `GET /converter/stories/:id/screenplay/tex`

#### Parameters

`id` : `string`<br/>
Unique identifier for the story.

#### Returns

A downloadable .tex file of the generated screenplay.

# Main Class Documentation

## `AnnotationHelper`

### `process(text)`

Splits the text into tokens and sentences for the annotation page. 

#### Parameters

`text` : `string`<br/>
The text to process.

#### Returns

No return values.

## `ConceptNet`

### `checkIfProp(possibleCharacter, verb)`

Checks if a noun is a prop or a character using ConceptNet.

#### Parameters

`possibleCharacter` : `string`<br/>
The noun to check if it's a prop or not.

`verb` : `string`<br/>
The verb to check if the noun can perform this action.

#### Returns

`flag` : `boolean`<br/>
If `flag == True`, then `possibleCharacter` is a prop. Otherwise, `possibleCharacter` is a character.

### `checkIfNamedLocation(pobj)`

Checks if a noun is a named location or not using ConceptNet.

#### Parameters

`pobj` : `string`
The noun to check if it's a named location or not.

#### Returns

`flag` : `boolean`<br/>
If `flag == True`, then `pobj` is a named location. Otherwise, `pobj` is not a named location.

### `checkForVerb(adp, verb)`

Checks for an adpositional phrase or verb to determine a location change.

#### Parameters

`adp` : `string`<br/>
The adpositional phrase to check if there's a location change.

`verb` : `string`<br/>
The verb to check if there's a location change.

#### Returns

`flag` : `boolean`<br/>
If `flag == True`, then a location change might have happened. Otherwise, there was no location change.

## `CorefResolver`

### `resolve_coreferences(doc, data)`

Builds a dictionary of coreferences from the JSON response from the Coref API.

#### Parameters

`doc` : `spaCy.Doc`<br/>
The story represented by spaCy's `Doc` object.

`data`: `dict`<br/>
The dictionary built from the JSON response from the Coref API.

#### Returns

No return values.

### `verify_resolution()`

Prints the dictionary of coreferences.

#### Parameters

No parameters.

#### Returns

No return values.

## `DialogueExtractor`

### `extract_dialogue(doc, story)`

Extracts the dialogue content, and then extracts the dialogue speakers.

#### Parameters

`doc` : `spaCy.Doc`<br/>
The story represented by spaCy's `Doc` object.

`story` : `Story`<br/>
The story represented by the `Story` object.

#### Returns

`dialogues` : `List<Dialogue>`<br/>
The list of dialogues extracted from the story.

### `print_dialogue(dialogue)`

Prints the speaker and the content of a dialogue.

#### Parameters

`dialogue` : `Dialogue`
The dialogue to be printed

#### Returns

No return values.

### `get_speaker(start, end)`

Gets the `Entity` object that starts at `start` and ends at `end`.

#### Parameters

`start` : `integer`<br/>
The token index of the start of the noun phrase.

`end` : `integer`<br/>
The token index of the end of the noun phrase.

#### Returns

`speaker` : `Entity`<br/>
The `Entity` object that starts at `start` and ends at `end`. `speaker == None` if no `Entity` is found.

### `extract_content()`

Extracts dialogue content using spaCy's `Matcher` class. Words enclosed in double quotes are considered for dialogue content.

#### Parameters

No parameters.

#### Returns

No return values.

### `extract_speakers()`

Extracts the speakers of the extracted dialogue contents. Three scenarios are considered:

1. Speaker said, "Hi."
2. "Hi," said Speaker.
3. "Hi."

#### Parameters

No parameters.

#### Returns

No return values.

### `resolve_speakers(mention_entity_dict)`

Resolves coreferences in the extracted dialogues using the dictionary from the `CorefResolver` class.

#### Parameters

`mention_entity_dict` : `dict`<br/>
The dictionary from the `CorefResolver` class.

#### Returns

No return values.

### `verify_dialogues()`

Prints all the dialogues.

#### Parameters

No parameters.

#### Returns

No return values.

## `EntityExtractor`

### `extract_entities(doc, story, speakers)`

Extracts the entities from the story. Uses spaCy's `DependencyMatcher` class to extract noun subject and action verb pairs, and classifies the noun subject as a character or prop. 

#### Parameters

`doc` : `spaCy.Doc`<br/>
The story represented by spaCy's `Doc` object.

`story` : `Story`<br/>
The story represented by the `Story` object.

`speakers` : `List<Entity>`<br/>
The list of speakers extracted from the `DialogueExtractor`.

#### Returns

No return values.

### `get_distinct_entities(entities, doc)`

#### Parameters

`entities` : `List<Entity>`<br/>
The total list of entities extracted from the story.

`doc` : `spaCy.Doc`<br/>
The story represented by spaCy's `Doc` object.

#### Returns

`distinct_entities` : `List<Entity>`<br/>
The list of entities where no two entities have the same string representation.

### `verify_characters()`

Prints the extracted characters from the story.

#### Parameters

No parameters.

#### Returns

No return values.

### `verify_props()`

Prints the extracted props from the story.

#### Parameters

No parameters.

#### Returns

No return values.

### `print_entity(entity)`

#### Parameters

`entity` : `Entity`<br/>
The entity to be printed

#### Returns

No return values.

### `get_character(start, end)`

Gets the `Character` object that starts at `start` and ends at `end`.

#### Parameters

`start` : `integer`<br/>
The token index of the start of the noun phrase.

`end` : `integer`<br/>
The token index of the end of the noun phrase.

#### Returns

`character` : `Character`<br/>
The `Character` object that starts at `start` and ends at `end`. `character == None` if no `Character` is found.

### `get_prop(start, end)`

Gets the `Prop` object that starts at `start` and ends at `end`.

#### Parameters

`start` : `integer`<br/>
The token index of the start of the noun phrase.

`end` : `integer`<br/>
The token index of the end of the noun phrase.

#### Returns

`prop` : `Prop`<br/>
The `Prop` object that starts at `start` and ends at `end`. `prop == None` if no `Prop` is found.

### `resolve_characters(mention_entity_dict)`

Resolves coreferences in the extracted characters using the dictionary from the `CorefResolver` class.

#### Parameters

`mention_entity_dict` : `dict`<br/>
The dictionary from the `CorefResolver` class.

#### Returns

No return values.

### `resolve_props(mention_entity_dict)`

Resolves coreferences in the extracted props using the dictionary from the `CorefResolver` class.

#### Parameters

`mention_entity_dict` : `dict`<br/>
The dictionary from the `CorefResolver` class.

#### Returns

No return values.

## `ActionExtractor`

### `check_event_type(sentence, sent_characters, sent_props)`

#### Parameters

`sentence` : `spaCy.Span`<br/>
The sentence to determine the event type of.

`sent_characters` : `List<Character>`<br/>
The characters found in the sentence.

`sent_props` : `List<Prop>`<br/>
The props found in the sentence.

#### Returns

The event type of the sentence, either a scene transition or an action event.

### `parse_transition_sentence(sentence, idx, sent_characters, sent_props)`

Instantiates and returns an `ActionEvent` with a scene transition classification.

#### Parameters

`sentence` : `spaCy.Span`<br/>
The sentence to determine the event type of.

`idx` : `integer`<br/>
The index of the sentence relative to all sentences in the spaCy `Doc`.

`sent_characters` : `List<Character>`<br/>
The characters found in the sentence.

`sent_props` : `List<Prop>`<br/>
The props found in the sentence.

#### Returns

A complete `ActionEvent` object that's classified as a scene transition and contains the characters and props found in the sentence.

### `parse_action_sentence(sentence, idx, sent_characters, sent_props)`

Instantiates and returns an `ActionEvent`.

#### Parameters

`sentence` : `spaCy.Span`<br/>
The sentence to determine the event type of.

`idx` : `integer`<br/>
The index of the sentence relative to all sentences in the spaCy `Doc`.

`sent_characters` : `List<Character>`<br/>
The characters found in the sentence.

`sent_props` : `List<Prop>`<br/>
The props found in the sentence.

#### Returns

A complete `ActionEvent` object that's not classified as a scene transition and contains the characters and props found in the sentence.


### `extract_events(doc, story, dialogue_events, character_list, prop_list)`

Iterates through all of the sentences in `doc` and instantiates `Scene` and `ActionEvent` objects based on the classification of each sentence. 

#### Parameters

`doc` : `spaCy.Doc`<br/>
The story represented by spaCy's `Doc` object.

`story` : `Story`<br/>
The story represented by the `Story` object.

`dialogue_events` : `List<Dialogue>`<br/>
The dialogue events extracted by the `DialogueExtractor` class.

`character_list` : `List<Character>`<br/>
The characters extracted by the `EntityExtractor` class.

`prop_list` : `List<Prop>`<br/>
The props extracted by the `EntityExtractor` class.

#### Returns

No return values.

### `verify_events()`

Prints the extracted `Scene` and `Event` objects.

#### Parameters

No parameters.

#### Returns

No return values.

## `ScreenplayGenerator`

### `generate_screenplay()`

Generates a .tex file from the abstract story representation, and then generates a .pdf file from the .tex file.

#### Parameters

No parameters.

#### Returns

No return values.

### `generate_tex()`

Generates a .tex file from the abstract story representation.

#### Parameters

No parameters.

#### Returns

No return values.

### `genetate_pdf()`

Generates a .pdf file from the generated .tex file.

#### Parameters

No parameters.

#### Returns

No return values.

### `generate_tex_meta()`

Generates the string representation of the title page for the screenplay.

#### Parameters

No parameters.

#### Returns

No return values.

### `generate_tex_body()`

Generates the string representation of the main body for the screenplay.

#### Parameters

No parameters.

#### Returns

No return values.

### `generate_tex_transition(transition_event)`

Generates the string representation of a scene transition.

#### Parameters

`transition_event` : `TransitionEvent`<br/>
The transition event to be generated.

#### Returns

No return values.

### `generate_tex_action(action_event)`

Generates the string representation of an action event.

#### Parameters

`action_event` : `ActionEvent`<br/>
The action event to be generated.

#### Returns

No return values.

### `generate_tex_dialogue(dialogue_event)`

Generates the string representation of a dialogue.

#### Parameters

`dialogue_event` : `DialogueEvent`<br/>
The dialogue event to be generated.

#### Returns

No return values.

## `SpacyUtil`

### `get_previous_token(token)`

#### Parameters

`token` : `spaCy.Token`<br/>
The token in question.

#### Returns

`previous_token` : `spaCy.Token`<br/>
The first non-whitespace and non-newline token before `token`.

### `get_next_token(token)`

#### Parameters

`token` : `spaCy.Token`<br/>
The token in question.

#### Returns

`next_token` : `spaCy.Token`<br/>
The first non-whitespace and non-newline token after `token`.

### `get_previous_word(token)`

#### Parameters

`token` : `spaCy.Token`<br/>
The token in question.

#### Returns

`previous_word` : `spaCy.Token`<br/>
The first word before `token`.

### `get_next_word(token)`

#### Parameters

`token` : `spaCy.Token`<br/>
The token in question.

#### Returns

`next_word` : `spaCy.Token`<br/>
The first word after `token`.

### `get_anchor(token)`

#### Parameters

`token` : `spaCy.Token`<br/>
The token in question.

#### Returns

`anchor` : `spaCy.Token`<br/>
The syntactic anchor of `token`

### `get_subject(anchor)`

#### Parameters

`anchor` : `spaCy.Token`<br/>
The syntactic anchor of a sentence.

#### Returns

`subject` : `spaCy.Token`<br/>
The noun subject of `anchor`.

### `get_object(anchor)`

#### Parameters

`anchor` : `spaCy.Token`<br/>
The syntactic anchor of a sentence.

#### Returns

`direct_object` : `spaCy.Token`<br/>
The direct object of `anchor`.

### `get_noun_chunk(noun)`

#### Parameters

`noun` : `spaCy.Token`<br/>
The noun in question.

#### Returns

`noun_chunk` : `spaCy.Span`<br/>
The `Span` noun chunk that contains the `Token` `noun`. 

### `get_sentence_index(sent)`

#### Parameters

`sent` : `spaCy.Span`<br/>
The sentence in question.

#### Returns

`idx` : `integer`<br/>
The index of the sentence with respect to the story `Doc`.

## `StoryPresenter`

### `process()`

Transforms the abstract story representation into a list of sentences and tokens for presentation. 

#### Parameters

No parameters.

#### Returns

No return values.

## `ExtractionEvaluator`

### `evaluate_extraction()`

Evaluates the precision, recall, and f1-score of each story element.

#### Parameters

No parameters.

#### Returns

No return values.

### `evaluate_dialogue_speaker(file)`

Evaluates the precision, recall, and f1-score of extracted dialogue speakers.

#### Parameters

`file` : `File`<br/>
The annotation .txt file to base the ground truth from. 

#### Returns

`score` : `tuple`<br/>
The evaluation score of the extraction for dialogue speakers formatted as a tuple `(precision, recall, f1-score)`

### `evaluate_dialogue_content(file)`

Evaluates the precision, recall, and f1-score of extracted dialogue content.

#### Parameters

`file` : `File`<br/>
The annotation .txt file to base the ground truth from. 

#### Returns

`score` : `tuple`<br/>
The evaluation score of the extraction for dialogue content formatted as a tuple `(precision, recall, f1-score)`

### `evaluate_characters(file)`

Evaluates the precision, recall, and f1-score of extracted characters.

#### Parameters

`file` : `File`<br/>
The annotation .txt file to base the ground truth from. 

#### Returns

`score` : `tuple`<br/>
The evaluation score of the extraction for characters formatted as a tuple `(precision, recall, f1-score)`

### `evaluate_props(file)`

Evaluates the precision, recall, and f1-score of extracted props.

#### Parameters

`file` : `File`<br/>
The annotation .txt file to base the ground truth from. 

#### Returns

`score` : `tuple`<br/>
The evaluation score of the extraction for props formatted as a tuple `(precision, recall, f1-score)`

### `evaluate_actions(file)`

Evaluates the precision, recall, and f1-score of extracted action lines.

#### Parameters

`file` : `File`<br/>
The annotation .txt file to base the ground truth from. 

#### Returns

`score` : `tuple`<br/>
The evaluation score of the extraction for action lines formatted as a tuple `(precision, recall, f1-score)`

### `evaluate_transitions(file)`

Evaluates the precision, recall, and f1-score of extracted scene transitions.

#### Parameters

`file` : `File`<br/>
The annotation .txt file to base the ground truth from. 

#### Returns

`score` : `tuple`<br/>
The evaluation score of the extraction for scene transitions formatted as a tuple `(precision, recall, f1-score)`.

### `count(prediction, annotation)`

Counts the number of true positives, false positives, and false negatives in the prediction.

#### Parameters

`prediction` : `List<integer>`<br/>
The predicted results of the system.

`annotation` : `List<integer>`<br/>
The annotated results.

#### Returns

`score` : `tuple`<br/>
The count score of the prediction formatted as a tuple `(true positives, false positives, false negatives)`

### `count_bianca(prediction, annotation)`

Implements Bianca's algorithm to count the number of perfect, missing, lacking, excess, missing, and wrong predictions.

#### Parameters

`prediction` : `List<integer>`<br/>
The predicted results of the system.

`annotation` : `List<integer>`<br/>
The annotated results.

#### Returns

`score` : `tuple`<br/>
The count score of the prediction formatted as a tuple `(perfect, missing, lacking, excess, missing, wrong)`

### `evaluate(tp, fp, fn)`

Calculates and returns the precision, recall, and f1-score given the count score.

#### Parameters

`tp` : `integer`<br/>
The number of true positives.

`fp` : `integer`<br/>
The number of false positives.

`fn` : `integer`<br/>
The number of false negatives.

#### Returns

`score` : `tuple`<br/>
The evaluation score formatted as a tuple `(precision, recall, f1-score)`.

### `evaluate(perfect, missing, lacking, excess, missing, wrong)`

Implements Bianca's algorithm to calculate and return the precision, recall, and f1-score given the count score.

#### Parameters

`perfect` : `integer`<br/>
The number of perfect predictions.

`missing` : `integer`<br/>
The number of missing predictions.

`lacking` : `integer`<br/>
The number of lacking predictions.

`excess` : `integer`<br/>
The number of excess predictions.

`missing` : `integer`<br/>
The number of missing predictions.

`wrong` : `integer`<br/>
The number of wrong predictions.

#### Returns

`score` : `tuple`<br/>
The evaluation score formatted as a tuple `(precision, recall, f1-score)`.

## `UnderstandingEvaluator`

### `evaluate_understanding()`

Calculates the simple matching coefficient, jaccard's coefficient, and cosine similarities of the story questionnaire responses and screenplay questionnaire responses.

#### Parameters

No parameters.

#### Returns

`story_understanding` : `dict`<br/>
The evaluation results of the story understanding module.

### `calculate_smc(x, y)`

Calculates the simple matching coefficient of sets `x` and `y`.

#### Parameters

`x` : `List<integer>`<br/>
The first set.

`y` : `List<integer>`<br/>
The second set.

#### Returns

`smc` : `double`<br/>
The simple matching coefficient of the two sets.

### `calculate_jc(x, y)`

Calculates the Jaccard's coefficient of sets `x` and `y`.

#### Parameters

`x` : `List<integer>`<br/>
The first set.

`y` : `List<integer>`<br/>
The second set.

#### Returns

`jc` : `double`<br/>
The Jaccard's coefficient of the two sets.


### `calculate_cs(x, y)`

Calculates the cosine similarity of vectors `x` and `y`.

#### Parameters

`x` : `List<integer>`<br/>
The first vector.

`y` : `List<integer>`<br/>
The second vector.

#### Returns

`cs` : `double`<br/>
The cosine similarity of the two vectors.

### `calculate_dot_product(x, y)`

Calculates the dot product of vectors `x` and `y`.

#### Parameters

`x` : `List<integer>`<br/>
The first vector.

`y` : `List<integer>`<br/>
The second vector.

#### Returns

`dot_product` : `double`<br/>
The dot product of the two vectors.

### `calculate_length(x, y)`

Calculates the length of vectors `x` and `y`.

#### Parameters

`x` : `List<integer>`<br/>
The first vector.

`y` : `List<integer>`<br/>
The second vector.

#### Returns

`length` : `double`<br/>
The length of the two vectors.

### `read_csv_file(csv_file)`

Reads a csv file and returns its 2D array representation. 

#### Parameters

`csv_file` : `File`<br/>
The csv file to be read.

#### Returns

`result` : `List<List<string>>`<br/>
The 2D array representation of the csv file.

### `get_binary_representation(responses)`

Transforms string responses into binary responses.

#### Parameters

`responses` : `dict`<br/>
The aggregated responses of the story and screenplay questionnaires. 

#### Returns

`result` : `dict`<br/>
`responses` but the `string` responses are now binary. 
