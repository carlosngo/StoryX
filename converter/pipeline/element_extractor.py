import spacy

from converter.models import Story, Scene, Event, DialogueEvent, ActionEvent, TransitionEvent, Entity, Character, Prop
from converter.pipeline.coref_resolver import CorefResolver
from converter.pipeline.dialogue_extractor import DialogueExtractor
from converter.pipeline.entity_extractor import EntityExtractor
from converter.pipeline.action_extractor import ActionExtractor
from converter.pipeline.spacy_util import SpacyUtil

class ElementExtractor:
    def __init__(self):
        self.doc = None
        self.story = None
        self.events = []
        self.main_characters = []
        self.characters = []
        self.props = []

    def extract_elements(self, story, text, data):
        self.doc = SpacyUtil.nlp(text)
        self.story = story
        coref_resolver = CorefResolver()
        coref_resolver.resolve_coreferences(self.doc, data)
        dialogue_extractor = DialogueExtractor()
        dialogue_extractor.extract_dialogue(self.doc, self.story)
        dialogue_extractor.resolve_speakers(coref_resolver.mention_entity_dict)
        # dialogue_extractor.verify_dialogues()
        entity_extractor = EntityExtractor()
        entity_extractor.extract_entities(self.doc, self.story, dialogue_extractor.speakers)
        entity_extractor.resolve_characters(coref_resolver.mention_entity_dict)
        entity_extractor.resolve_props(coref_resolver.mention_entity_dict)
        self.main_characters = entity_extractor.get_main_characters() 
        # print(self.main_characters)
        self.main_characters.reverse()
        # print(self.main_characters)
        # entity_extractor.verify_characters()
        # entity_extractor.verify_props()

        action_extractor = ActionExtractor()
        action_extractor.parse_events(self.doc, self.story, dialogue_extractor.dialogues, entity_extractor.characters, entity_extractor.props)
        # action_extractor.verify_events()
        # self.events = action_extractor.events
        # self.characters = action_extractor.characters
        # self.props = action_extractor.props
    
    def verify_elements(self):
        
        print('main characters:')
        for i in range(min(10, len(self.main_characters))):
            character = self.main_characters[i]
            print(self.doc[character.reference_start:character.reference_end].text)
        sents = list(self.doc.sents)
        for scene in list(Scene.objects.filter(story=self.story).order_by('scene_number')):
            print(f'scene { scene.scene_number }:')
            for event in scene.event_set.all().order_by('event_number'):
                if hasattr(event, 'dialogueevent'):
                    event_type = 'dialogue'
                elif hasattr(event, 'actionevent') and hasattr(event.actionevent, 'transitionevent'):
                    event_type = 'scene transition'
                else:
                    event_type = 'action line'
                    
                print(f'event { event.event_number }: {event_type}')
                s = ''
                for idx in range(event.sentence_start, event.sentence_end):
                    s = s + sents[idx].text_with_ws
                print(s)
                print('characters:')
                for character in event.characters.all():
                    print(self.doc[character.entity.reference_start:character.entity.reference_end].text)
                print('props:')
                for prop in event.props.all():
                    print(self.doc[prop.entity.reference_start:prop.entity.reference_end].text)


        # scene_number = -1
        # sents = list(self.doc.sents)
        # for evt in self.events:
        #     event_type = ''
        #     if type(evt) == ActionEvent:
        #         event = evt.event
        #         event_type = 'action line'
        #     elif type(evt) == DialogueEvent:
        #         event = evt.event
        #         event_type = 'dialogue'
        #     elif type(evt) == TransitionEvent:
        #         event = evt.action_event.event
        #         event_type = 'scene transition'
        #     if (event.scene.scene_number != scene_number):
        #         print(f'scene { event.scene.scene_number }:')
        #         scene_number = event.scene.scene_number  
        #     print(f'event { event.event_number }: { event_type }')
            
            
        #     for idx in range(event.sentence_start, event.sentence_end):
        #         print(sents[idx].text_with_ws)
        

    