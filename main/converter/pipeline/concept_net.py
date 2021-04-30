from django.conf import settings

from converter.pipeline.spacy_util import SpacyUtil

import os
import json
import spacy

class ConceptNet:

    def checkIfProp(possibleCharacter, verb):
        
        doc = SpacyUtil.nlp(verb)
        flag = True
        for token in doc:
            # print(token.lemma_)
            lemmatizedVerb = token.lemma_

            jPerson = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/personJson.json')).read())
            jMain = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/dltkJson.json')).read())

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

    def checkIfNamedLocation(pobj):
        doc = SpacyUtil.nlp(pobj)
        flag = True
        jMain = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/dltkJson.json')).read())
        #change to DLTK json
        #First check if the pobj is already a character we know
        #if pobj is a character name that already exists
        #return false immediately

        if pobj.lower() == "he" or pobj.lower() == "him" or pobj.lower() == "her" or pobj.lower() == "she" or pobj.lower() == "they" or pobj.lower() == "them" or pobj.lower() =="it":
            return False
        
        #Goes through SpaCy NER
        for ent in doc.ents:
            if ent.label_ == "GPE" or ent.label_ == "ORG" or ent.label_ == "LOC":
                return True


        for c in jMain:
            if pobj.lower() in c['context1'].lower():
                flag = False

        return flag

    def checkForVerb(adp, verb):
        doc = SpacyUtil.nlp(verb)
        flag = False
        for token in doc:
            print(token.lemma_)
            lemmatizedVerb = token.lemma_

            verbsLocationChange = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'json/verbsDictionary.json')).read())

            for v in verbsLocationChange:
                if lemmatizedVerb in v['word'].lower():
                    return True
                
                if "in" in adp.lower() or "to" in adp.lower() or "on" in adp.lower():
                    return True

                if not flag:
                    return False
        return flag