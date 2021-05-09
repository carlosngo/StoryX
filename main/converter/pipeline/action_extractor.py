from converter.pipeline.concept_net import ConceptNet

from converter.models import Scene, Event, DialogueEvent, ActionEvent, TransitionEvent, Entity, Prop, Character

class ActionExtractor:
    # Event type values
    EVENT_DIALOGUE = 0
    EVENT_TRANSITION = 1
    EVENT_ACTION = 2

    def __init__(self):
        self.doc = None
        self.story = None
        self.events = []
        self.scenes = []
        self.scene_total = 0
        self.scene_counter = 0
        self.d_idx = 0
        self.seq = -1

    def check_event_type(self, sentence, sent_characters, sent_props):
        pobjTokens = []
        verbTokens = []
        possibleCharacter = ''
        adp = ''

        # if <insert scene transition rule conditions>
        for token in sentence:
            tokenText = token.text
            if token.dep_ == "pobj":
                # get all pobj tokens after
                #iterate through sentence to get all consecutive pobj tokens after finding the first
                if ConceptNet.checkIfNamedLocation(tokenText):
                    return ActionExtractor.EVENT_TRANSITION
            elif token.pos_ == 'verb':
                if ConceptNet.checkForVerb(adp, tokenText) and len(sent_props) > 0:
                #iterate through sentence to get all verb pobj tokens after finding the first
                    return ActionExtractor.EVENT_TRANSITION
            elif token.pos_ == 'adp':
                #iterate through sentence to get all verb pobj tokens after finding the first
                adp = tokenText

        # IF there is a setting change or a time change, it's an event transition
        # IF there's a prepositional object, check if it's a character or a setting,

        return ActionExtractor.EVENT_ACTION

    def parse_transition_sentence(self, sent, idx, sent_characters, sent_props):
        # create a Transition Event
        event = Event(
            sentence_start = idx,
            sentence_end = idx + 1,
            event_number = self.seq,
        )
        event.save()
        # set scene and sequence ids
        # event.set_scene_id = self.scene_counter

        # action: the full sentence
        # event.set_action = str(sent)

        # insert code to get actor (e.g. "Carlos", "He", "she")
        for character in sent_characters:
            event.characters.add(character)
        for prop in sent_props:
            event.props.add(prop)
        # event.set_actor = sent_characters
        # event.characters = sent_characters
        # event.props = sent_props

        self.scene_counter = self.scene_counter + 1
        
        return TransitionEvent(action_event=ActionEvent(event=event))

    def parse_action_sentence(self, sent, idx, sent_characters, sent_props):
        # create a Transition Event
        event = Event(
            sentence_start = idx,
            sentence_end = idx + 1,
            event_number = self.seq,
        )
        event.save()

        # set scene and sequence ids
        # event.set_scene_id = self.scene_counter

        # action: the full sentence
        # Note: This is temporary, change this to a range
        # event.set_action = str(sent)

        # insert code to get actor (e.g. "Carlos", "He", "she")
        for character in sent_characters:
            event.characters.add(character)
        # event.characters = sent_characters
        for prop in sent_props:
            event.props.add(prop)
        # event.props = sent_props
        
        return ActionEvent(event=event)

    def extract_events(self, doc, story, dialogue_events, character_list, prop_list):
        self.scene_counter = 1
        self.d_idx = 0
        self.seq = -1
        self.doc = doc
        self.story = story
        d_len = len(dialogue_events)
        is_dialogue = False
        char_idx = 0
        prop_idx = 0
        sent_characters = []
        sent_props = []
        scene = Scene(story=self.story, scene_number=self.scene_counter)
        scene.save()
        dialogue_total = 0
        i = 0
        type = -1
        
        #iterate through the document by sentence
        for idx, sent in enumerate(doc.sents):
            if i <= idx:
                # check if current sentence is a dialogue event
                # print("\n\ndlen", d_len, "\nself.d_idx: ", self.d_idx, "\nidx: ", idx, "\n[self.d_idx]sentence_range: ",    range(dialogue_events[self.d_idx].event.sentence_start, dialogue_events[self.d_idx].event.sentence_end))

                while self.d_idx < d_len and idx in range(dialogue_events[self.d_idx].event.sentence_start, dialogue_events[self.d_idx].event.sentence_end):

                    
                    type = ActionExtractor.EVENT_DIALOGUE
                    
                    
                    self.seq = self.seq + 1
                    event = dialogue_events[self.d_idx].event
                    event.event_number = self.seq
                    
                    # event.set_scene_id = self.scene_counter
                    # event.type = ActionExtractor.EVENT_DIALOGUE
                    event.scene = scene
                    event.save()
                    # print('found dialogue: ')
                    self.events.append(dialogue_events[self.d_idx])
                    dialogue_total = dialogue_total + 1
                    i = max(i, event.sentence_end - 1)
                    is_dialogue = True
                    self.d_idx = self.d_idx + 1

                
                if is_dialogue == False and doc[sent.start].text.strip() != '"':

                    # this sets the sent_characters list
                    for character in character_list:
                        if sent == doc[character.entity.reference_start].sent:
                            sent_characters.append(character)

                    for prop in prop_list:
                        if sent == doc[prop.entity.reference_start].sent:
                            sent_props.append(prop)
                    # if char_idx < len(character_list):
                    #     temp_character = character_list[char_idx]

                    # if prop_idx < len(prop_list):
                    #     temp_prop = prop_list[prop_idx]

                    # # check if the character is in the current sentence
                    # if sent == doc[temp_character.entity.reference_start].sent:
                    #     # save all sentence characters into sent_characters
                    #     while (sent == doc[temp_character.entity.reference_start].sent):
                    #         sent_characters.append(temp_character)
                    #         char_idx = char_idx + 1
                    #         if char_idx < len(character_list):
                    #             temp_character = character_list[char_idx]
                    #         else:
                    #             break

                    # # check if the prop is in the current sentence
                    # if sent == doc[temp_prop.entity.reference_start].sent:
                    #     # save all sentence props into sent_props
                    #     while (sent == doc[temp_prop.entity.reference_start].sent):
                    #         sent_props.append(temp_prop)
                    #         prop_idx = prop_idx + 1
                    #         if prop_idx < len(prop_list):
                    #             temp_prop = prop_list[prop_idx]
                    #         else:
                    #             break
                    
                    self.seq = self.seq + 1
                    type = self.check_event_type(sent, sent_characters, sent_props)

                    if type == ActionExtractor.EVENT_TRANSITION:
                        event = self.parse_transition_sentence(sent, idx, sent_characters, sent_props)
                        event.action_event.event.scene = scene
                        event.action_event.event.save()
                        event.action_event.save()
                        event.save()
                        self.scenes.append(scene)
                        scene = Scene(story=self.story, scene_number=self.scene_counter)
                        scene.save()
                    else:
                        event = self.parse_action_sentence(sent, idx, sent_characters, sent_props)
                        event.event.scene = scene
                        event.event.save()
                        event.save()
                        # scene.events.append(event)
                    self.events.append(event)
                
                # print('type: ', type)
                # reset array
                sent_characters = []
                sent_props = []
                i = i + 1
                is_dialogue = False

        if type != ActionExtractor.EVENT_TRANSITION:
            self.scenes.append(scene)
        
        self.scene_total = self.scene_counter
        # print(dialogue_total)
        # print("out of ")
        # print(len(dialogue_events))
        # return self.scenes

    def verify_events(self):
        scene_number = -1
        sents = list(self.doc.sents)
        for evt in self.events:
            event_type = ''
            if type(evt) == ActionEvent:
                event = evt.event
                event_type = 'action line'
            elif type(evt) == DialogueEvent:
                event = evt.event
                event_type = 'dialogue'
            elif type(evt) == TransitionEvent:
                event = evt.action_event.event
                event_type = 'scene transition'
            if (event.scene.scene_number != scene_number):
                print(f'scene { event.scene.scene_number }:')
                scene_number = event.scene.scene_number  
            print(f'event { event.event_number }: { event_type }')
            
            
            for idx in range(event.sentence_start, event.sentence_end):
                print(sents[idx].text_with_ws)
        

                
