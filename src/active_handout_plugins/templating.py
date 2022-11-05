from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from jinja2 import Environment
import random


class RandomIntVariable:
    def __init__(self):
        self.new()

    def new(self, start=0, end=10):
        self.value = random.randint(start, end)
        return str(self.value)

    def __str__(self):
        return str(self.value)


class Chooser:
    def __init__(self):
        pass

    def __call__(self, *args):
        return random.choice(args)


class Jinja2PreProcessor(Preprocessor):
    def run(self, lines):
        text = '\n'.join(lines)
        e = Environment()
        random_elements = {
            'choose': Chooser(),
        }
        random_elements.update(
            {f'randint{i}': RandomIntVariable() for i in range(1, 11)})
        new_text = e.from_string(text).render(random_elements)

        return new_text.split('\n')
