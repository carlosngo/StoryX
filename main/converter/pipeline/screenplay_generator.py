from pdflatex import PDFLaTeX
from converter.pipeline.spacy_util import SpacyUtil
from django.conf import settings

import os
import subprocess


class ScreenplayGenerator:
    def __init__(self, story, text):
        self.doc = SpacyUtil.nlp(text)
        self.sent_list = list(self.doc.sents)
        self.story = story
        self.tex_str = ''

    def generate_screenplay(self):
        self.generate_tex()
        self.generate_pdf()

    def generate_tex(self):
        self.tex_str = '\\documentclass{screenplay}\n\\newenvironment{simplechar}{%\n\catcode`\$=12\n\catcode`\&=12\n\catcode`\#=12\n\catcode`\^=12\n\catcode`\_=12\n\catcode`\~=12\n\catcode`\%=12\n}{}\n'
        self.tex_str += self.generate_tex_meta()
        self.tex_str += '\\begin{document}\n\\coverpage\n\\begin{simplechar}'
        self.tex_str += self.generate_tex_body()
        self.tex_str += '\n\\theend\n\\end{simplechar}\n\\end{document}'
        
        # print(self.tex_str)
    
        with open(os.path.join(settings.SCREENPLAY_ROOT, self.story.get_filename() + '.tex'), 'w') as f:
            f.write(self.tex_str)

    def generate_tex_meta(self):
        return "\\title{{{}}}\n\n\\author{{{}}}\\address{{}}\n".format(self.story.title, self.story.author)

    def generate_tex_body(self):
        str_body = ''
        for scene in self.story.scene_set.all().order_by('scene_number'):
            # scene_str = "\n\CUT TO SCENE {}\n\n".format(scene.scene_number)
            scene_str = "\n\n\\begin{flushright}CUT TO:\\end{flushright}\n\n"
            
            for event in scene.event_set.all().order_by('event_number'):
                if hasattr(event, 'dialogueevent'):
                    scene_str += self.generate_tex_dialogue(event)
                elif hasattr(event, 'actionevent'):
                    scene_str += self.generate_tex_action(event)
                else:
                    scene_str += self.generate_tex_transition(event)
            if scene_str.strip(' \n').count('\n') > 0:
                str_body += scene_str
        
        return str_body

    def generate_tex_transition(self, transition_event):
        action = ''
        start = transition_event.sentence_start

        for token in self.sent_list[start]:
            action = action + token.text_with_ws

        action = action.strip('" ')

        newaction = action[:1].upper() + action[1:]
        return newaction

    def generate_tex_action(self, action_event):
        action = ''
        start = action_event.sentence_start

        for token in self.sent_list[start]:
            action = action + token.text_with_ws

        action = action.strip('" ')
        
        newaction = action[:1].upper() + action[1:] + ' '
        return newaction

    # REFERENCE
    # \begin{dialogue}{April}
    #         Okay, okay, don't panic.
    # \end{dialogue}


    def generate_tex_dialogue(self, dialogue_event):
        character = ''
        if dialogue_event.characters.count() == 0:
            character = 'UNKNOWN'
        else:
            for speaker in dialogue_event.characters.all():
                entity = speaker.entity
                if entity.refers_to is not None:
                    entity = entity.refers_to
                for i in range(entity.reference_start, entity.reference_end):
                    character = character + self.doc[i].text_with_ws
            character = character.strip()
        
        character = character.strip('" ')
        dialogue_str = ''
        for i in range(dialogue_event.dialogueevent.content_start, dialogue_event.dialogueevent.content_end):
            dialogue_str = dialogue_str + self.doc[i].text_with_ws
        dialogue_str = dialogue_str.strip()[1:-1].replace("\n", " ")
        if dialogue_str[-1] == ',':
            dialogue_str = dialogue_str[:-1] + '.'
        dialogue_str = dialogue_str[:1].upper() + dialogue_str[1:]
        dialogue_char_limit = 1500
        dialogue_chunks = len(dialogue_str) // dialogue_char_limit
        if len(dialogue_str) % dialogue_char_limit != 0:
           dialogue_chunks = dialogue_chunks + 1 
        tex = ''
        for i in range(dialogue_chunks):
            start = i * dialogue_char_limit
            end = min(len(dialogue_str), (i + 1) * dialogue_char_limit)
            dialogue_slice = ''
            if start != 0:
                dialogue_slice = '-'
            dialogue_slice = dialogue_slice + dialogue_str[start:end]
            if end != len(dialogue_str):
                dialogue_slice = dialogue_slice + '-'
            tex = tex + "\n\n\\begin{{dialogue}}{{{}}}\n\t{}\n\\end{{dialogue}}\n\n".format(character, dialogue_slice)

        return tex


    def generate_pdf(self):
        path_to_tex = os.path.join(settings.SCREENPLAY_ROOT, self.story.get_filename() + '.tex')
        cmd = ['pdflatex', '-interaction', 'nonstopmode', '-output-directory', 'media/screenplays', path_to_tex]
        proc = subprocess.Popen(cmd)
        proc.communicate()
        # print(path_to_tex)
        # pdfl = PDFLaTeX.from_texfile(path_to_tex)

        # pdf, log, completed_process = pdfl.create_pdf()
        # with open(os.path.join(settings.SCREENPLAY_ROOT, self.story.get_filename() + '.pdf'), 'wb') as f:
        #     f.write(pdf)

