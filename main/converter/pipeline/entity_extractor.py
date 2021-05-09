from converter.models import Entity, Character, Prop
from converter.pipeline.spacy_util import SpacyUtil
from converter.pipeline.concept_net import ConceptNet

from spacy.matcher import DependencyMatcher

import spacy

class EntityExtractor:
    def __init__(self):
        self.doc = None
        self.story = None
        self.characters = []
        self.props = []
    
    def extract_entities(self, doc, story, speakers):
        self.doc = doc
        self.story = story
        self.characters = speakers
        self.props = []
        
        for ent in doc.ents:
            if ent.label_ == 'PERSON' and self.get_character(ent.start, ent.end) is None:
                entity = Entity(
                    story = self.story,
                    reference_start = ent.start,
                    reference_end = ent.end,
                )
                self.characters.append(Character(entity=entity))
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        char_pronouns = [
            'he', 'she', 'him', 'her', 'they', 'them',
        ]
        matcher = DependencyMatcher(SpacyUtil.nlp.vocab)

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
            
            # subject
            noun = SpacyUtil.get_noun(nsubj)
            if noun is not None:
                
                noun_chunk = SpacyUtil.get_noun_chunk(noun)
                if noun_chunk is not None and self.get_character(noun_chunk.start, noun_chunk.end) is None:
                    entity = Entity(
                        story = self.story,
                        reference_start = noun_chunk.start,
                        reference_end = noun_chunk.end,
                    )
                    if noun.text.lower() == 'it':
                        prop = Prop(entity = entity)
                        self.props.append(prop)
                    elif self.is_mentioned(noun_chunk.text):
                        character = Character(entity = entity)
                        self.characters.append(character)
                    elif ConceptNet.checkIfProp(noun.text, verb.text) == False:  
                        character = Character(entity = entity)
                        self.characters.append(character)
                    # else:
                    #     prop = Prop(entity = entity)
                    #     self.props.append(prop)

            # direct object
            dobj = SpacyUtil.get_object(verb)
            if dobj is not None:

                noun = SpacyUtil.get_noun(dobj)

                # print(str(verb) + " " + str(noun))
                if noun is not None:
                    noun_chunk = SpacyUtil.get_noun_chunk(noun)
                    if noun_chunk is not None and self.get_character(noun_chunk.start, noun_chunk.end) is None:
                        entity = Entity(
                            story = self.story,
                            reference_start = noun_chunk.start,
                            reference_end = noun_chunk.end,
                        )
                        # if ConceptNet.checkIfProp(noun.text, 'say') is False:  
                        #     character = Character(entity = entity)
                        #     self.characters.append(character)
                        # else:
                        
                        if noun.text.lower() in char_pronouns:
                            character = Character(entity = entity)
                            self.characters.append(character)
                        elif self.is_mentioned(noun_chunk.text):
                            character = Character(entity = entity)
                            self.characters.append(character)
                        else:
                            prop = Prop(entity = entity)
                            self.props.append(prop)
        
        for character in self.characters:
            character.entity.save()
            character.save()
        for prop in self.props:
            prop.entity.save()
            prop.save()
            
        # clean props
        # for i in range(len(self.props) - 1, -1, -1):
        #     prop = self.props[i]
        #     found = False
        #     for char in self.characters:
        #         if (
        #             doc[prop.entity.reference_end - 1].text.lower() 
        #             == doc[char.entity.reference_end - 1].text.lower()
        #         ):
        #             found = True
        #     if found is True:
        #         self.props.pop(i)
        #         self.characters.append(Character(entity=prop.entity))

    def get_distinct_characters(self):
        distinct_characters = {}
        for character in self.characters:
            char_string = self.to_string(character.entity).lower()
            if char_string not in distinct_characters:
                distinct_characters[char_string] = character
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
            prop_string = self.to_string(prop.entity).lower()
            if prop_string not in distinct_props:
                distinct_props[prop_string] = prop
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
        if type(entity) == Character:
            print('character: ' + self.to_string(entity.entity))
        else:
            print('prop: ' + self.to_string(entity.entity))

    def to_string(self, entity):
        s = ''
        for i in range(entity.reference_start, entity.reference_end):
            s = s + self.doc[i].text_with_ws
        return s    

    def get_character(self, start, end):
        for character in self.characters:
            if character.entity.reference_start == start and character.entity.reference_end == end:
                return character
        return None

    def get_prop(self, start, end):
        for prop in self.props:
            if prop.entity.reference_start == start and prop.entity.reference_end == end:
                return prop
        return None
    
    def is_mentioned(self, char_string):
        for speaker in self.characters:
            speaker_start = speaker.entity.reference_start
            speaker_end = speaker.entity.reference_end
            if self.doc[speaker_start:speaker_end].text.lower() == char_string.lower():
                return True
        return False

    def resolve_characters(self, mention_entity_dict):
        for referer in self.characters:
            referer_start = referer.entity.reference_start
            referer_end = referer.entity.reference_end
            if self.doc[referer_end - 1].pos_ == 'PRON' and referer.entity.refers_to is None and (referer_start, referer_end) in mention_entity_dict:
                char_start, char_end = mention_entity_dict[(referer_start, referer_end)]
                char = self.get_character(char_start, char_end)
                if char is None:
                    char = Character(entity = Entity(
                        story = self.story,
                        reference_start = char_start,
                        reference_end = char_end,
                    ))
                    char.entity.save()
                    char.save()
                    self.characters.append(char)
                # print(self.doc[referer_start:referer_end].text)
                # print('refers to')
                # print(self.doc[speaker_start:speaker_end].text)
                referer.entity.refers_to = char.entity
                referer.entity.save()
    
    def resolve_props(self, mention_entity_dict):
        for referer in self.props:
            referer_start = referer.entity.reference_start
            referer_end = referer.entity.reference_end
            if referer.entity.refers_to is None and (referer_start, referer_end) in mention_entity_dict:
                prop_start, prop_end = mention_entity_dict[(referer_start, referer_end)]
                prop = self.get_prop(prop_start, prop_end)
                if prop is None:
                    prop = Prop(entity = Entity(
                        story = self.story,
                        reference_start = prop_start,
                        reference_end = prop_end,
                    ))
                    prop.entity.save()
                    prop.save()
                    self.props.append(prop)
                # print(self.doc[referer_start:referer_end].text)
                # print('refers to')
                # print(self.doc[speaker_start:speaker_end].text)
                referer.entity.refers_to = prop.entity
                referer.entity.save()

    def get_main_characters(self):
        count = {}
        for character in self.characters:
            entity = character.entity
            if entity not in count:
                count[entity] = 0
            count[entity] = count[entity] + 1
            if entity.refers_to is not None:
                if entity.refers_to not in count:
                    count[entity.refers_to] = 0
                count[entity.refers_to] = count[entity.refers_to] + 1
        sorted_count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1])}
        # for key, value in sorted_count.items():
        #     print(f'{key}: {str(value)}')
        return list(sorted_count.keys())
        