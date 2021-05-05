from converter.models import Event, DialogueEvent, Character, Entity
from converter.pipeline.spacy_util import SpacyUtil

from spacy.matcher import Matcher

import spacy

class DialogueExtractor:
    def __init__(self):
        self.doc = None
        self.story = None
        self.dialogues = []
        self.speakers = []

    def extract_dialogue(self, doc, story):
        self.doc = doc
        self.story = story
        self.dialogues = []
        self.speakers = []
        self.extract_content()
        self.extract_speakers()
        return self.dialogues

    # HELPER FUNCTIONS START

    # def print_event(self, event):
    #     i = 0
    #     for sent in doc.sents:
    #         if i >= event.sentence_range.start and i < event.sentence_range.stop:
    #             print(sent)
    #         i = i + 1

    # prints the dialogue in a readable format
    def print_dialogue(self, dialogue):
        string = ''
        if dialogue.event.characters.count() == 0:
            string = 'Unknown speaker: '
        else:
            for character in dialogue.event.characters.all():
                entity = character.entity
                if entity.refers_to is not None:
                    entity = entity.refers_to
                for i in range(entity.reference_start, entity.reference_end):
                    string = string + self.doc[i].text_with_ws
                string = string.strip() + ': '
        for i in range(dialogue.content_start, dialogue.content_end):
            string = string + self.doc[i].text_with_ws
        print(string)
        # self.print_event(dialogue)


    def get_speaker(self, start, end):
        for speaker in self.speakers:
            if speaker.entity.reference_start == start and speaker.entity.reference_end == end:
                return speaker
        return None
    # HELPER FUNCTIONS END

    def extract_content(self):
        arr = []

        matcher = Matcher(SpacyUtil.nlp.vocab)

        pattern = [
            {"ORTH": '"'}
        ]

        matcher.add("DialogueStart", [pattern])

        matches = matcher(self.doc)

        if len(matches) > 0:
            arr.append([matches[0][1], -1])

        processed = [False for i in range(len(matches))]

        # for each double quotes found in the text
        for i in range(0, len(matches)):
            current_index = matches[i][1]
            # if closing double quotes
            if processed[i] == True or i == len(matches) - 1:
                # the end of the latest dialogue is the current index
                arr[len(arr) - 1][1] = current_index
                # if the "dialogue" does not end with punctuation, discard
                if not SpacyUtil.get_previous_token(self.doc[current_index]).is_punct:
                    arr.pop()
                # create new dialogue if there are more
                if i < len(matches) - 1:
                    arr.append([matches[i + 1][1], -1])
                # don't process tokens after closing double quotes
                continue
            
            next_index = matches[i + 1][1]
            # flag for dialogue continuation after line break
            has_break = False

            # for each token between the current and next double quotes
            for j in range(current_index + 1, next_index):
                token = self.doc[j]
                # line breaks are empty if stripped

                if not token.text.strip() and self.doc[next_index].is_sent_start:
                    has_break = True
                    break
                    
            if has_break is False:
                # if there is no dialogue continuation, next double quotes is a closing double quotes
                processed[i + 1] = True
        
        for i in range(len(arr)):
            first_token = self.doc[arr[i][0] + 1]
            last_token = self.doc[arr[i][1] - 1]
            sentence_start = SpacyUtil.get_sentence_index(first_token.sent)
            sentence_end = SpacyUtil.get_sentence_index(last_token.sent) + 1
            event = Event(
                sentence_start = sentence_start, 
                sentence_end = sentence_end
            )
            dialogue_event = DialogueEvent(
                event = event,
                content_start = arr[i][0],
                content_end = arr[i][1] + 1,
            )
            event.save()
            dialogue_event.save()
            self.dialogues.append(dialogue_event)

    def extract_speakers(self):

        # First format
        for dialogue in self.dialogues:
            opening_quotes = self.doc[dialogue.content_start]
            closing_quotes = self.doc[dialogue.content_end - 1]
            previous_token = SpacyUtil.get_previous_token(opening_quotes)
            if (
                previous_token is not None 
                and (
                    previous_token.text == ','
                    or previous_token.is_alpha
                )
            ):
                previous_word = SpacyUtil.get_previous_word(opening_quotes)
                while previous_word.pos_ != 'VERB' and previous_word.pos_ != 'AUX':
                    previous_word = SpacyUtil.get_previous_word(previous_word)
                speaker_verb = previous_word
                speaker_noun = SpacyUtil.get_subject(speaker_verb)
                while speaker_noun is None:
                    while (
                        speaker_verb.head.pos_ != 'VERB' 
                        and speaker_verb.head.pos_ != 'AUX'
                        and speaker_verb.head == speaker_verb
                    ):
                        speaker_verb = speaker_verb.head
                    
                    speaker_verb = speaker_verb.head
                    speaker_noun = SpacyUtil.get_subject(speaker_verb)
                    if speaker_noun is None:
                        speaker_noun = SpacyUtil.get_object(speaker_verb)

                speaker_noun_chunk = SpacyUtil.get_noun_chunk(speaker_noun)
                speaker = self.get_speaker(speaker_noun_chunk.start, speaker_noun_chunk.end)
                if speaker is None:
                    speaker = Character(entity = Entity(
                        story = self.story,
                        reference_start = speaker_noun_chunk.start,
                        reference_end = speaker_noun_chunk.end
                    ))
                    speaker.entity.save()
                    speaker.save()
                    self.speakers.append(speaker)
                dialogue.event.characters.add(speaker)
                # dialogue.event.actor_start = speaker_noun_chunk.start
                # dialogue.event.actor_end = speaker_noun_chunk.end

        # Second format
        for i in range(len(self.dialogues) - 1, -1, -1) :
            dialogue = self.dialogues[i]
            closing_quotes = self.doc[dialogue.content_end - 1]
            previous_token = SpacyUtil.get_previous_token(closing_quotes)
            next_token = self.doc[closing_quotes.i + 1]
            next_word = SpacyUtil.get_next_word(closing_quotes)
            if (
                dialogue.event.characters.count() == 0
                and next_word is not None
                and next_token.text.strip()
                and (
                    # if the story starts with a dialogue
                    previous_token is None
                    # if the first character of the next word after the dialogue is lowercase
                    or self.doc.text[next_word.idx].islower()
                    # if the dialogue content ends in a comma
                    or previous_token.text == ','
                    # if the previous token is a line break
                    or previous_token.text.strip()
                )
            ):
                while next_word.pos_ != 'VERB' and next_word.pos_ != 'AUX':
                    next_word = SpacyUtil.get_next_word(next_word)
                speaker_verb = next_word
                speaker_noun = SpacyUtil.get_subject(speaker_verb)
                if speaker_noun is None:
                    speaker_noun = SpacyUtil.get_object(speaker_verb)
                if speaker_noun is None and speaker_verb.head.pos_ == 'VERB':
                    speaker_noun = SpacyUtil.get_subject(speaker_verb.head)
                speaker_noun_chunk = SpacyUtil.get_noun_chunk(speaker_noun)

                speaker = self.get_speaker(speaker_noun_chunk.start, speaker_noun_chunk.end)
                if speaker is None:
                    # print(f'speaker {speaker_noun_chunk.start}, {speaker_noun_chunk.end} is not found')
                    speaker = Character(entity = Entity(
                        story = self.story,
                        reference_start = speaker_noun_chunk.start,
                        reference_end = speaker_noun_chunk.end
                    ))
                    speaker.entity.save()
                    speaker.save()
                    self.speakers.append(speaker)
                dialogue.event.characters.add(speaker)
                # dialogue.event.actor_start = speaker_noun_chunk.start
                # dialogue.event.actor_end = speaker_noun_chunk.end

                if i < len(self.dialogues) - 1:
                    next_dialogue = self.dialogues[i + 1]
                    
                    if (
                        # if the start of the next dialogue is right after the end of the sentence
                        next_dialogue.content_start == next_word.sent.end
                        # if the next dialogue is not preceded by a newline
                        and self.doc[next_dialogue.content_start - 1].text.strip()
                        # if next_dialogue has no speaker yet
                        and next_dialogue.event.actor_start is None
                    ):
                        next_dialogue.event.characters.add(speaker)
                        # next_dialogue.event.actor_start = speaker_noun_chunk.start
                        # next_dialogue.event.actor_end = speaker_noun_chunk.end
    
        # Third format
        for i in range(len(self.dialogues)):
            current_dialogue = self.dialogues[i]
            if current_dialogue.event.characters.count() == 0:
                previous_dialogue = self.dialogues[i - 1]
                if i < len(self.dialogues) - 1:
                    next_dialogue = self.dialogues[i + 1]
                else:
                    next_dialogue = None
                
                for character in previous_dialogue.event.characters.all():
                    speaker = character
                # speaker_start = previous_dialogue.event.actor_start
                # speaker_end = previous_dialogue.event.actor_end

                # if next dialogue has no speaker, it's going to be alternate
                if next_dialogue is None or next_dialogue.event.characters.count() == 0:
                    listener_dialogue = self.dialogues[i - 2]
                    for character in listener_dialogue.event.characters.all():
                        listener = character
                    # listener_start = listener_dialogue.event.actor_start
                    # listener_end = listener_dialogue.event.actor_end
                    is_listener = True
                    for j in range(i, len(self.dialogues)):
                        current_dialogZue = self.dialogues[j]
                        if current_dialogue.event.actor_start is not None:
                            break
                        if is_listener == True:
                            current_dialogue.event.characters.add(listener)
                            # current_dialogue.event.actor_start = listener_start
                            # current_dialogue.event.actor_end = listener_end
                        else:
                            current_dialogue.event.characters.add(speaker)
                            # current_dialogue.event.actor_start = speaker_start
                            # current_dialogue.event.actor_end = speaker_end
                        is_listener = not is_listener
                
                # if next dialogue has a speaker
                else:
                    # it's going to be the same speaker as the previous dialogue
                    current_dialogue.event.characters.add(speaker)
                    # current_dialogue.event.actor_start = speaker_start
                    # current_dialogue.event.actor_end = speaker_end

    def resolve_speakers(self, mention_entity_dict):
        # length = len(self.speakers)
        for referer in self.speakers:
            # referer = self.speakers[i]
            referer_start = referer.entity.reference_start
            referer_end = referer.entity.reference_end
            if (referer_start, referer_end) in mention_entity_dict:
                speaker_start, speaker_end = mention_entity_dict[(referer_start, referer_end)]
                speaker = self.get_speaker(speaker_start, speaker_end)
                if speaker is None:
                    speaker = Character(entity = Entity(
                        story = self.story,
                        reference_start = speaker_start,
                        reference_end = speaker_end,
                    ))
                    speaker.entity.save()
                    speaker.save()
                    self.speakers.append(speaker)
                # print(self.doc[referer_start:referer_end].text)
                # print('refers to')
                # print(self.doc[speaker_start:speaker_end].text)
                referer.entity.refers_to = speaker.entity
                referer.entity.save()
                

    # verify extracted dialogues
    def verify_dialogues(self):
        print('EXTRACTED DIALOGUES: ' + str(len(self.dialogues)))

        for dialogue in self.dialogues:
            self.print_dialogue(dialogue)