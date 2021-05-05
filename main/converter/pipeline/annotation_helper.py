from converter.pipeline.spacy_util import SpacyUtil

class AnnotationHelper:
    def __init__(self):
        self.tokens = []
        self.sentences = []
    
    def process(self, text):
        doc = SpacyUtil.nlp(text)
        for i in range(doc.__len__()): 
            token = doc[i]
            self.tokens.append(token.text_with_ws)
        for i, sent in enumerate(doc.sents):
            # print(i)
            # print(sent)
            self.sentences.append(sent.text_with_ws)
            
            
