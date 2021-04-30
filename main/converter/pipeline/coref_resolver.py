class CorefResolver():
    def __init__(self):
        self.doc = None
        self.coref_clusters = {}
        self.mention_entity_dict = {}
  
    # tentative, actual function will have to connect to another Django project to
    # do the actual coreference resolution using an spaCy version 2.1.0
    def resolve_coreferences(self, doc, data):
        for start in data:
            for end in data[start]:
                mentions = []
                for mention in data[start][end]:
                    mentions.append((mention[0], mention[1]))
                    self.mention_entity_dict[(mention[0], mention[1])] = (int(start), int(end))
                    self.coref_clusters[(int(start), int(end))] = mentions

    def verify_resolution(self):
        print(self.coref_clusters)
        print(self.mention_entity_dict)