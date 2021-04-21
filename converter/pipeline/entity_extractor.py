from converter.models import Entity, Character, Prop
from converter.pipeline.spacy_util import SpacyUtil
from converter.pipeline.concept_net import ConceptNet

from spacy.matcher import DependencyMatcher

import spacy

class EntityExtractor:
    def __init__(self):
        self.doc = None
        self.characters = []
        self.props = []
    
    def extract_entities(self, doc):
        self.doc = doc
        self.characters = []
        self.props = []

        nlp = spacy.load("en_core_web_sm")
        
        matcher = DependencyMatcher(nlp.vocab)

        pattern = [
            {
                "RIGHT_ID": "action_verb",
                "RIGHT_ATTRS": {"POS": "VERB"}
            },
            {
                "LEFT_ID": "action_verb",
                "REL_OP": ">",
                "RIGHT_ID": "action_subject",
                "RIGHT_ATTRS": {"DEP": "nsubj"},
            }
        ]

        matcher.add("CHARACTER_ACTIONS", [pattern])
        matches = matcher(doc)

        for i in range(len(matches)):
            match_id, token_ids = matches[i]
            verb = self.doc[token_ids[0]]
            nsubj = self.doc[token_ids[1]]
            dobj = SpacyUtil.get_object(verb)

            # character 
            noun = SpacyUtil.get_noun(nsubj)
            if noun is not None and noun.pos_ != 'PRON':
                
                noun_chunk = SpacyUtil.get_noun_chunk(noun)
                if ConceptNet.checkIfProp(noun.text, verb.text) is False:
                    entity = Entity(
                        reference_start = noun_chunk.start,
                        reference_end = noun_chunk.end,
                    )
                    character = Character(entity = entity)
                    self.characters.append(character)

            # prop
            if dobj is not None:
                
                noun = SpacyUtil.get_noun(dobj)

                # print(str(verb) + " " + str(noun))
                if noun is not None and noun.pos_ != 'PRON':
                    noun_chunk = SpacyUtil.get_noun_chunk(noun)
                    entity = Entity(
                        reference_start = noun_chunk.start,
                        reference_end = noun_chunk.end,
                    )
                    prop = Prop(entity = entity)
                    self.props.append(prop)
            
        # clean props
        for i in range(len(self.props) - 1, -1, -1) :
            prop = self.props[i]
            found = False
            for char in self.characters:
                if (
                    doc[prop.entity.reference_end - 1].text.lower() 
                    == doc[char.entity.reference_end - 1].text.lower()
                ):
                    found = True
            if found is True:
                self.props.pop(i)

    def get_distinct_characters(self):
        distinct_characters = {}
        for character in self.characters:
            char_string = self.to_string(character.entity)
            distinct_characters[char_string.lower()] = character
        return list(distinct_characters.values())

    def verify_characters(self):
        print("extracted " + str(len(self.characters)) + " characters")
        for character in self.characters:
            self.print_entity(character)

        print('')

        distinct_characters = self.get_distinct_characters()
        print("extracted " + str(len(distinct_characters)) + " distinct characters")
        for character in distinct_characters:
            self.print_entity(character)
    
    def get_distinct_props(self):
        distinct_props = {}
        for prop in self.props:
            prop_string = self.to_string(prop.entity)
            distinct_props[prop_string.lower()] = prop
        return list(distinct_props.values())

    def verify_props(self):
        print("extracted " + str(len(self.props)) + " props")
        for prop in self.props:
            self.print_entity(prop)

        print('')

        distinct_props = self.get_distinct_props()
        print("extracted " + str(len(distinct_props)) + " distinct props")
        for prop in distinct_props:
            self.print_entity(prop)

    def print_entity(self, entity):
        if type(entity) is Character:
            print('character: ' + self.to_string(entity.entity))
        else:
            print('prop: ' + self.to_string(entity.entity))

    def to_string(self, entity):
        s = ''
        for i in range(entity.reference_start, entity.reference_end):
            s = s + self.doc[i].text_with_ws
        return s    
