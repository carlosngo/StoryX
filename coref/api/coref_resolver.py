import spacy
import neuralcoref
import json

class CorefResolver:
    def resolve_coreferences(self, text):
        nlp = spacy.load("en_core_web_sm")
        neuralcoref.add_to_pipe(nlp)
        doc = nlp(text)

        coref = {}
        for cluster in doc._.coref_clusters:
            coref[cluster.main.start] = {}
            coref[cluster.main.start][cluster.main.end] = []
            for mention in cluster.mentions:
                coref[cluster.main.start][cluster.main.end].append([mention.start, mention.end])
        return coref