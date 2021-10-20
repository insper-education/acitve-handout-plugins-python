from mkdocs.plugins import BasePlugin
import mkdocs.config.config_options
import os

from .exercise import get_title, add_vscode_button, find_code_exercises, find_exercises_in_handout, get_meta_for, override_yaml, post_exercises


token = os.environ.get('REPORT_TOKEN', '')

class FindExercises(BasePlugin):
    config_scheme = (
        ('report_url', mkdocs.config.config_options.Type(str, default='')),
    )

    def on_pre_build(self, config):
        self.pages_with_exercises = []
        self.yaml_overrides = {}

    def on_files(self, files, config):
        code_exercises = find_code_exercises(files)
        self.pages_with_exercises.extend(code_exercises)
        return files

    def on_page_markdown(self, markdown, page, config, files):
        meta_file = get_meta_for(page.file, files)
        if meta_file:
            self.yaml_overrides[meta_file.abs_dest_path] = {
                'title': get_title(markdown)
            }
            return add_vscode_button(markdown, meta_file, config['site_url'])

        return markdown

    def on_page_content(self, html, page, config, files):
        new_exercises, new_html = find_exercises_in_handout(html, page.url)
        self.pages_with_exercises.extend(new_exercises)
        return new_html

    def on_post_build(self, config):
        post_exercises(self.pages_with_exercises, token, self.config['report_url'])
        for abs_dest_path, overrides in self.yaml_overrides.items():
            override_yaml(abs_dest_path, overrides)
