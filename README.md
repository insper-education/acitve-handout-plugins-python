## Environment Variables

You can set the following variables to override some settings:

- `BACKEND_URL`: change the backend url (useful for backend development)
- `BACKEND_USER_MENU_URL`: set the user menu url (default: `BACKEND_URL/api/user-menu`)

## Compiling SCSS and JS assets

Never modify the `assets/js` or `assets/css` folders. You should change the files under `assets_src` and then compile them.

When you are first compiling the assets locally, install the dependencies with:

    $ yarn

Then, during development, run:

    $ yarn start

Finally, to build the optimized version:

    $ yarn build

## Watching changes in the plugin from some other project

You will probably test your changes in this project with some other mkdocs project with your contents. Install the local repository with:

    $ pip install -e PATH_TO_THIS_DIR

Then, to serve mkdocs:

    $ mkdocs serve --watch PATH_TO_THIS_DIR

## Creating new types of exercises in your project

You can create new exercises to your course's specific needs without modifying the theme project. Start by creating a mkdocs hook file (e.g. `hooks/custom_exercise.py`). You need to register the hook in your `mkdocs.yml` with (path is relative to the `mkdocs.yml` file):

```yml
hooks:
  - hooks/custom_exercise.py
```

In your hook file, create a `on_startup` function and register the visitor builder function. Example:

```python
import random
from active_handout_plugins import register_exercise_visitor_builder, ExerciseAdmonition

def on_startup(*args, **kwargs):
    register_exercise_visitor_builder(RandomQuestionExercise, 4)

class RandomQuestionExercise(ExerciseAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['random-question'], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
        questions = ["What's your name?", "What is the answer to life, the universe and everything?"]

        return f'''
        <p>{random.choice(questions)}</p>
        <input type="text" value="" name="data"/>
        <input class="ah-button ah-button--primary" type="submit" value="Submit"/>
        '''
```

### Syntax

Add the exercise to your Markdown file with:

```
!!! exercise random-question
    You can add text here
```

## Adding new admonition visitors

You can also add custom `AdmonitionVisitor`s to extend Markdown without creating a whole new extension. Start by creating a hook, following the same process for custom exercises. Then you can add your processor with the following:

```python
from active_handout_plugins import register_treeprocessor_builder, AdmonitionVisitor

register_treeprocessor_builder(CustomAdmonition, 'custom-editor', 20)

class CustomAdmonition(AdmonitionVisitor):
    def visit(self, el):
        if 'custom-admonition-name' not in el.attrib['class']:
            return

        # Modify the element el here.
```
