import spacy

from converter.models import Story
from converter.pipeline.coref_resolver import CorefResolver

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
        