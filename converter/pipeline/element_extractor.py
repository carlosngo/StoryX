import spacy

from converter.models import Story
from converter.pipeline.coref_resolver import CorefResolver
from converter.pipeline.dialogue_extractor import DialogueExtractor
from converter.pipeline.entity_extractor import EntityExtractor

class ElementExtractor:
    def __init__(self):
        self.doc = None
        self.scenes = []
        self.events = []
        self.entities = []

    def extract_elements(self, text, data):
        nlp = spacy.load("en_core_web_sm")
        self.doc = nlp(text)
        coref_resolver = CorefResolver()
        coref_resolver.resolve_coreferences(self.doc, data)
        dialogue_extractor = DialogueExtractor()
        dialogue_extractor.extract_dialogue(self.doc)
        # dialogue_extractor.verify_dialogues()
        entity_extractor = EntityExtractor()
        entity_extractor.extract_entities(self.doc)
        entity_extractor.verify_characters()
        entity_extractor.verify_props()
        