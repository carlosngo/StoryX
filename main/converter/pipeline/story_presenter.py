from converter.pipeline.spacy_util import SpacyUtil

class StoryPresenter:
    def __init__(self, story):
        self.story = story
        self.entities = []
        self.events = []
        
        self.doc = SpacyUtil.nlp(story.text_file.open('r').read())
        self.sentences = []
        for scene in story.scene_set.all().order_by('scene_number'):
            for event in scene.event_set.all().order_by('event_number'):
                self.events.append(event)
        for entity in story.entity_set.all().order_by('reference_start'):
            self.entities.append(entity)

        
        
    def process(self):
        for idx, sent in enumerate(self.doc.sents):
            sentence = {
                'is_dialogue': False,
                'is_action': False,
                'is_transition': False,
                'tokens': []
            }
            cur_event = None
            for event in self.events:
                if idx in range(event.sentence_start, event.sentence_end):
                    if hasattr(event, 'dialogueevent'):
                        sentence['is_dialogue'] = True
                        cur_event = event
                    elif hasattr(event, 'actionevent'):
                        if hasattr(event.actionevent, 'transitionevent'):
                            sentence['is_transition'] = True
                        else:
                            sentence['is_action'] = True
            for i in range(sent.start, sent.end):
                tkn = self.doc[i]
                token = {
                    'is_character': False,
                    'is_prop': False,
                    'text': tkn.text_with_ws
                }

                for entity in self.entities:
                    
                    if i in range(entity.reference_start, entity.reference_end):
                        in_dialogue = False
                        if sentence['is_dialogue']:
                            dialogue = cur_event.dialogueevent
                            if entity.reference_start in range(dialogue.content_start, dialogue.content_end):
                                in_dialogue = True
                        if not in_dialogue:
                            if hasattr(entity, 'character'):
                                token['is_character'] = True
                            if hasattr(entity, 'prop'):
                                token['is_prop'] = True
                sentence['tokens'].append(token)

            

            self.sentences.append(sentence)


        
        
