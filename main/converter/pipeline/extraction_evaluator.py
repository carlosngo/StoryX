from django.conf import settings

from converter.models import Character, Prop, Entity
from converter.pipeline.spacy_util import SpacyUtil
from converter.pipeline.entity_extractor import EntityExtractor

import os


def convert_entities_to_string(entities, doc):
    arr = []
    for entity in entities:
        arr.append(EntityExtractor.to_string(entity, doc).lower())
    return arr

class ExtractionEvaluator:
    # dialogues is a list of dialogues, file is the file object from .read()
    # Context:
    # The file will have different formats, but generally the features are space-separated and one line is one entry:
    # For dialogue, an entry is formatted as content_start content_end speaker_start speaker_end
    # For characters and props, an entry is entity_start entity_end
    # For action and transition events, an entry is sentence_index
    # Read the file given the following formats, and create a list of tuples, and pass it to the self.count function as the annotation parameter
    # With the list of story elements provided, also create a list of tuples following the same format above, and pass it to the self.count function as the prediction parameter
    def __init__(self, story):
        self.story = story
        self.characters = []
        self.props = []
        self.dialogues = []
        self.actions = []
        self.transitions = []
        self.dialogue_content_score = None
        self.dialogue_speaker_score = None
        self.character_score = None
        self.prop_score = None
        self.action_score = None
        self.transition_score = None

        self.doc = SpacyUtil.nlp(story.text_file.open('r').read())
        
        for scene in story.scene_set.all().order_by('scene_number'):
            for event in scene.event_set.all().order_by('event_number'):
                if hasattr(event, 'dialogueevent'):
                    self.dialogues.append(event)
                elif hasattr(event, 'actionevent'):
                    self.actions.append(event)
                if event.is_transition:
                    self.transitions.append(event)
                        
        for entity in story.entity_set.all().order_by('reference_start'):
            if self.doc[entity.reference_end - 1].pos_ != 'PRON':
                in_dialogue = False
                for d in self.dialogues:
                    dialogue = d.dialogueevent
                    if entity.reference_start in range(dialogue.content_start, dialogue.content_end):
                        in_dialogue = True
                if not in_dialogue:
                    if hasattr(entity, 'character'):
                        self.characters.append(entity.character)
                    elif hasattr(entity, 'prop'):
                        self.props.append(entity.prop)

        self.characters = convert_entities_to_string(EntityExtractor.get_distinct_entities(self.characters, self.doc), self.doc)
        self.props = convert_entities_to_string(EntityExtractor.get_distinct_entities(self.props, self.doc), self.doc)

        

    def evaluate_extraction(self):
        print('checking ' + (os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_dialogues.txt')))
        print('checking file for dialogue_content_score')
        file = open(os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_dialogues.txt'), 'r')
        self.dialogue_content_score = self.evaluate_dialogue_content(file)
        print('checking file for dialogue_speaker_score')
        file = open(os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_dialogues.txt'), 'r')
        self.dialogue_speaker_score = self.evaluate_dialogue_speaker(file)
        print('checking file for character_score')
        file = open(os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_characters.txt'), 'r')
        self.character_score = self.evaluate_characters(file)
        print('checking file for prop_score')
        file = open(os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_props.txt'), 'r')
        self.prop_score = self.evaluate_props(file)
        print('checking file for action_score')
        file = open(os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_action lines.txt'), 'r')
        self.action_score = self.evaluate_actions(file)
        print('checking file for transition_score')
        file = open(os.path.join(settings.ANNOTATION_ROOT, self.story.title.lower() + '_scene transitions.txt'), 'r')
        self.transition_score = self.evaluate_transitions(file)


        

    def evaluate_dialogue_speaker(self, file):
        prediction = []
        annotation = []

        for d in self.dialogues:
            if d.characters.count() > 0:
                for speaker in d.characters.all():
                    entity = speaker.entity
                tPrd = (entity.reference_start, entity.reference_end)
                prediction.append(tPrd)

        for line in file:
            line.strip()
            sAnn = line.split(" ")
            tAnn = (int(sAnn[2]), int(sAnn[3]) + 1)
            annotation.append(tAnn)
            
        tp, fp, fn = self.count(prediction, annotation)
        return self.evaluate(tp, fp, fn)
    
    def evaluate_dialogue_content(self, file):
        prediction = []
        annotation = []

        for d in self.dialogues:
            dialogue = d.dialogueevent
            tPrd = (dialogue.content_start, dialogue.content_end)
            prediction.append(tPrd)

        for line in file:
            line.strip()
            sAnn = line.split(" ")
            tAnn = (int(sAnn[0]), int(sAnn[1]) + 1)
            annotation.append(tAnn)

        tp, fp, fn = self.count(prediction, annotation)
        return self.evaluate(tp, fp, fn)

    def evaluate_characters(self, file):
        prediction = self.characters
        annotation = []

        for line in file:
            line.strip()
            sAnn = line.split(" ")
            tAnn = Character(entity=Entity(reference_start=int(sAnn[0]), reference_end=int(sAnn[1]) + 1))
            annotation.append(tAnn)

        annotation = convert_entities_to_string(EntityExtractor.get_distinct_entities(annotation, self.doc), self.doc)
        return self.evaluate_bianca(*self.count_bianca(prediction, annotation))
    
    def evaluate_props(self, file):
        prediction = self.props
        annotation = []

        for line in file:
            line.strip()
            sAnn = line.split(" ")
            tAnn = Prop(entity=Entity(reference_start=int(sAnn[0]), reference_end=int(sAnn[1]) + 1))
            annotation.append(tAnn)

        annotation = convert_entities_to_string(EntityExtractor.get_distinct_entities(annotation, self.doc), self.doc)
        return self.evaluate_bianca(*self.count_bianca(prediction, annotation))
    
    def evaluate_actions(self, file):
        prediction = []
        annotation = []

        for a in self.actions:
            tPrd = (a.sentence_start)
            prediction.append(tPrd)

        for line in file:
            tAnn = (int(line.strip()))
            annotation.append(tAnn)

        tp, fp, fn = self.count(prediction, annotation)
        return self.evaluate(tp, fp, fn)

    def evaluate_transitions(self, file):
        prediction = []
        annotation = []

        for t in self.transitions:
            tPrd = (t.sentence_start)
            prediction.append(tPrd)

        for line in file:
            tAnn = (int(line.strip()))
            annotation.append(tAnn)

        tp, fp, fn = self.count(prediction, annotation)
        return self.evaluate(tp, fp, fn)
    
    def count(self, prediction, annotation):
        tp = 0
        fp = 0
        fn = 0
        p_idx = 0
        a_idx = 0
        prediction.sort()
        annotation.sort()
        print('preditions')
        print(prediction)
        print('annotations')
        print(annotation)
        while p_idx < len(prediction) and a_idx < len(annotation):
            a = prediction[p_idx]
            b = annotation[a_idx]
            # a is a false positive
            if a < b:
                fp = fp + 1
                p_idx = p_idx + 1
            # a is a true positive
            elif a == b:
                tp = tp + 1
                p_idx = p_idx + 1
                a_idx = a_idx + 1
            # b is a false negative
            else:
                fn = fn + 1
                a_idx = a_idx + 1
        
        # rest of prediction are false positives
        while p_idx < len(prediction):
            fp = fp + 1
            p_idx = p_idx + 1
        
        # rest of annotation are false negatives
        while a_idx < len(annotation):
            fn = fn + 1
            a_idx = a_idx + 1
    
        print(f'tp = {tp}, fp = {fp}, fn = {fn}')
        return tp, fp, fn

    def count_bianca(self, prediction, annotation):
        perfect = 0
        lacking = 0
        excess = 0
        missing = 0
        wrong = 0
        p_idx = len(prediction) - 1
        a_idx = len(annotation) - 1
        prediction.sort(reverse=True)
        annotation.sort(reverse=True)
        print('preditions')
        print(prediction)
        print('annotations')
        print(annotation)
        while p_idx >= 0 and a_idx >= 0:
            a = prediction[p_idx]
            b = annotation[a_idx]
            # a is a true positive
            if a == b:
                perfect = perfect + 1
                prediction.pop(p_idx)
                annotation.pop(a_idx)
                p_idx = p_idx - 1
                a_idx = a_idx - 1
            elif a < b:
                p_idx = p_idx - 1
            else:
                a_idx = a_idx - 1
        
        p_idx = len(prediction) - 1
        while p_idx >= 0:
            a = prediction[p_idx]
            a_idx = len(annotation) - 1
            is_lacking = False
            while a_idx >= 0 and not is_lacking:
                b = annotation[a_idx]
                if a in b:
                    lacking = lacking + 1
                    prediction.pop(p_idx)
                    annotation.pop(a_idx)
                    is_lacking = True
                a_idx = a_idx - 1
            p_idx = p_idx - 1
        
        a_idx = len(annotation) - 1
        while a_idx >= 0:
            a = annotation[a_idx]
            p_idx = len(prediction) - 1
            is_excess = False
            while p_idx >= 0 and not is_excess:
                b = prediction[p_idx]
                if a in b:
                    excess = excess + 1
                    prediction.pop(p_idx)
                    annotation.pop(a_idx)
                    is_excess = True
                p_idx = p_idx - 1
            a_idx = a_idx - 1
        
        missing = len(annotation)
        wrong = len(prediction)
    
        print(f'perfect = {perfect}, lacking = {lacking}, excess = {excess}, missing = {missing}, wrong = {wrong}')
        return perfect, lacking, excess, missing, wrong

    # Precision = TruePositives / (TruePositives + FalsePositives)
    # Recall = TruePositives / (TruePositives + FalseNegatives)
    # F-Measure = (2 * Precision * Recall) / (Precision + Recall)   
    def evaluate(self, tp, fp, fn):
        if tp + fp == 0:
            precision = 0
        else:
            precision = 1.0 * tp / (tp + fp)
        if tp + fn == 0:
            recall = 0
        else:
            recall = 1.0 * tp / (tp + fn)
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = (2 * precision * recall) / (precision + recall)
        return precision, recall, f1

    def evaluate_bianca(self, perfect, lacking, excess, missing, wrong):
        if perfect + lacking + excess + wrong == 0:
            precision = 0
        else:
            precision = (perfect + lacking + excess) / (perfect + lacking + excess + wrong)
        if perfect + lacking + excess + missing == 0:
            recall = 0
        else:
            recall = (perfect + lacking + excess) / (perfect + lacking + excess + missing)
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = (2 * precision * recall) / (precision + recall)
        return precision, recall, f1