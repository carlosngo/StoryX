
class Evaluator:
    # dialogues is a list of dialogues, file is the file object from .read()
    # Context:
    # The file will have different formats, but generally the features are space-separated and one line is one entry:
    # For dialogue, an entry is formatted as content_start content_end speaker_start speaker_end
    # For characters and props, an entry is entity_start entity_end
    # For action and transition events, an entry is sentence_index
    # Read the file given the following formats, and create a list of tuples, and pass it to the count function as the annotation parameter
    # With the list of story elements provided, also create a list of tuples following the same format above, and pass it to the count function as the prediction parameter


    def evaluate_dialogue_speaker(self, dialogues, file):
        for line in file:
            pass
        return evaluate(tp, fp, fn)
    
    def evaluate_dialogue_content(self, dialogues, file):
        return evaluate(tp, fp, fn)

    def evaluate_characters(self, characters, file):
        return evaluate(tp, fp, fn)
    
    def evaluate_props(self, props, file):
        return evaluate(tp, fp, fn)
    
    def evaluate_actions(self):
        return evaluate(tp, fp, fn)

    def evaluate_transitions(self):
        return evaluate(tp, fp, fn)
    
    def count(self, prediction, annotation):
        tp = 0
        fp = 0
        fn = 0
        p_idx = 0
        a_idx = 0
        prediction.sort()
        annotation.sort()
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
    
        return tp, fp, fn


    # Precision = TruePositives / (TruePositives + FalsePositives)
    # Recall = TruePositives / (TruePositives + FalseNegatives)
    # F-Measure = (2 * Precision * Recall) / (Precision + Recall)   
    def evaluate(self, tp, fp, fn):
        precision = 1.0 * tp / (tp + fp)
        recall = 1.0 * tp / (tp + fn)
        f1 = (2 * precision * recall) / (precision + recall)
        return precision, recall, f1
