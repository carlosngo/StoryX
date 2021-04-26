import spacy

from converter.models import Story
from converter.pipeline.coref_resolver import CorefResolver
from converter.pipeline.dialogue_extractor import DialogueExtractor
from converter.pipeline.entity_extractor import EntityExtractor
from converter.pipeline.action_extractor import ActionExtractor
from converter.pipeline.spacy_util import SpacyUtil

class ElementExtractor:
    def __init__(self):
        self.doc = None
        self.events = []
        self.characters = []
        self.props = []

    def extract_elements(self, text, data):
        self.doc = SpacyUtil.nlp(text)
        coref_resolver = CorefResolver()
        coref_resolver.resolve_coreferences(self.doc, data)
        dialogue_extractor = DialogueExtractor()
        dialogue_extractor.extract_dialogue(self.doc)
        # dialogue_extractor.verify_dialogues()
        entity_extractor = EntityExtractor()
        entity_extractor.extract_entities(self.doc)
        # entity_extractor.verify_characters()
        # entity_extractor.verify_props()
        action_extractor = ActionExtractor()
        action_extractor.parse_events(self.doc, dialogue_extractor.dialogues, entity_extractor.characters, entity_extractor.props)
        # action_extractor.verify_scenes()
        self.events = action_extractor.events
        self.characters = action_extractor.characters
        self.props = action_extractor.props

    