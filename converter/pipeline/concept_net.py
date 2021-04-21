from django.conf import settings

import os
import json
import spacy

class ConceptNet:
    def checkIfProp(possibleCharacter, verb):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(verb)
        flag = True
        for token in doc:
            # print(token.lemma_)
            lemmatizedVerb = token.lemma_

            jPerson = json.loads(open(os.path.join(settings.STATIC_ROOT, 'json/personJson.json')).read())
            jMain = json.loads(open(os.path.join(settings.STATIC_ROOT, 'json/dltkJson.json')).read())

            if possibleCharacter.lower() == "he" or possibleCharacter.lower() == "him" or possibleCharacter.lower() == "her" or possibleCharacter.lower() == "she" or possibleCharacter.lower() == "they" or possibleCharacter.lower() == "them":
                return False

            for v in jPerson:
                if lemmatizedVerb.lower() in v['context2'].lower():
                    flag = False

            for c in jMain:
                if c['context1'].lower() == possibleCharacter.lower():
                    flag = False
            
            for c in jMain:
                if lemmatizedVerb.lower() in c['context2'].lower():
                    flag = False

        return flag

    