import spacy

class SpacyUtil:
    nlp = spacy.load("en_core_web_sm")

    # gets the first non-whitespace and non-newline token before the given token 
    def get_previous_token(token):
        try:
            previous_token = token.nbor(-1)
            while not previous_token.text.strip():
                previous_token = previous_token.nbor(-1)
            return previous_token
        except:
            return None

    # gets the first non-whitespace and non-newline token after the given token
    def get_next_token(token):
        try:
            next_token = token.nbor()
            while not next_token.text.strip():
                next_token = next_token.nbor()
            return next_token
        except:
            return None

    # gets the first word before the given token. returns None if no words are found
    def get_previous_word(token):
        try:
            previous_token = token.nbor(-1)
            while not previous_token.text.strip() or previous_token.is_punct:
                previous_token = previous_token.nbor(-1)
            return previous_token
        except:
            return None

    # gets the first word before the given token. returns None if no words are found
    def get_next_word(token):
        try:
            next_token = token.nbor()
            while not next_token.text.strip() or next_token.is_punct:
                next_token = next_token.nbor()
            return next_token
        except:
            return None

    # gets the syntactic anchor of a token
    def get_anchor(token):
        cur_token = token
        # current token = head iff anchor
        while cur_token.head.text != cur_token.text:
            cur_token = cur_token.head
        return cur_token

    # gets the nsubj from the anchor verb
    def get_subject(anchor):
        for token in anchor.children:
            if token.dep_ == 'nsubj':
                return SpacyUtil.get_noun(token)
        return None

    # sometimes, tokens with nsubj are not always nouns
    def get_noun(nsubj):
        if nsubj.pos_[-1] == 'N':
            return nsubj
        for token in nsubj.subtree:
            if token.pos_[-1] == 'N':
                return token
        return None

    def get_object(anchor):
        for token in anchor.children:
            if token.dep_ == 'dobj':
                return token
        return None

    # gets the noun chunk
    def get_noun_chunk(noun):
        for noun_chunk in noun.doc.noun_chunks:
            if noun in noun_chunk:
                    return noun_chunk
        return None

    # gets the index of the input sentence in the document's list of sentences
    def get_sentence_index(sent):
        for idx, s in enumerate(sent.doc.sents):
            if s == sent:
                return idx
        return -1

    # gets the index of the token in its local sentence 
    # (i.e. if the sentence begins with the input token, this returns 0)
    def get_local_index(token):
        return token.idx - token.sent.start

    # gets the noun subjects from sentences. may return pronouns
    # can use get_noun_chunk for each noun subject
    def get_subjects_from_sent(sent):
        subjects = []
        for i in range(sent.start, sent.end):
            token = sent.doc[i]
            if token.dep_ == 'nsubj':
                subjects.append(SpacyUtil.get_noun(token))
        return subjects