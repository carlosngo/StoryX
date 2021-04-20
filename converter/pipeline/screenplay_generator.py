class ScreenplayGenerator:
    def __init__(self, doc, title, author, scenes):
        self.doc = doc
        self.title = title
        self.author = author
        self.scenes = scenes

    def generate_screenplay(self):
        story_str = '\\documentclass{screenplay}'
        story_str += self.tex_meta()
        story_str += '\\begin{document}\n\coverpage\n'
        story_str += self.tex_body()
        story_str += '\n\\theend\n\\end{document}'
        return story_str

    def tex_meta(self):
        return "\\title{{{}}}\n\\author{{{}}}\n".format(self.title, self.author)

    def tex_body(self):
        str_body = ''
        for scene in scenes:
            scene_header = "Scene {}\n\n".format(scene.number)
            str_body += scene_header
            for event in scene.events:
                if event.type == EVENT_TRANSITION:
                    str_body += tex_transition
                elif event.type == EVENT_ACTION:
                    str_body += tex_action
                elif event.type == EVENT_DIALOGUE:
                    str_body += tex_dialogue
                str_body+= '\n'
        return str_body

    def tex_transition(self, transition_event):
        action = ''
        for i in transition_event.content_range:
            action = action + self.doc[i].text_with_ws
        return action

    def tex_action(self, action_event):
        action = ''
        for i in action_event.content_range:
            action = action + self.doc[i].text_with_ws
        return action

    # REFERENCE
    # \begin{dialogue}{April}
    #     Okay, okay, don't panic.
    # \end{dialogue}
    def tex_dialogue(self, dialogue_event):
        character = ''
        if dialogue_event.actor is None:
            character = 'Unknown speaker'
        else:
            for i in dialogue_event.actor:
                character = character + self.doc[i].text_with_ws
        dialogue = ''
        for i in dialogue_event.content_range:
            dialogue = dialogue + self.doc[i].text_with_ws
        tex = "\\begin{{dialogue}}{{{}}}\n\t{}\n\\end{{dialogue}}\n".format(character, dialogue)
        return tex