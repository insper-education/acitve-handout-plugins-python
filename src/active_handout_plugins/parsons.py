import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor
from .question import QuestionAdmonition
import random

class ParsonsQuestion(QuestionAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('question', ['parsons'], *args, **kwargs)

    def create_question_form(self, el, submission_form):
        code = submission_form.findall('*')[-2]
        end_char = code.text.find("\x03")
        start_index = code.text.find(":") + 1
        html_idx = int(code.text[start_index:end_char])
        processed_code = self.md.htmlStash.rawHtmlBlocks[html_idx]
        
        start_index = processed_code.find("<code>") + 6
        lines = processed_code.split("\n")[:-1]
        lines[0] = lines[0][start_index:]

        random.shuffle(lines)
        left_panel = '<div class="highlight original-code"><pre><code class="parsons-drag-area">'
        for l in lines:
            indent_count = l.count('    ')
            l_no_indent = l.replace('    ', '')
            left_panel += f'<div class="parsons-line" draggable="true" data-indentCount={indent_count}>{l_no_indent}</div>'
        left_panel += '</code></pre></div>'
        
        right_panel = '''
<div class="highlight parsons-drop-div">
    <pre><code class="parsons-drop-area"><div class="indent-line"> </div></code></pre>
</div>
'''
        code.set("class", "parsons-code")
        code.tag = 'div'
        code.text = self.md.htmlStash.store(left_panel + right_panel)

        return '''
        <input type="hidden" name="data" value=""/>
        <input type="button" name="sendButton" value="Testar"/>
        <input type="button" name="resetButton" value="Reset"/>
        '''


