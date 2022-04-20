""" Jinja2 templates """

import os
import json
from jinja2 import Environment, FileSystemLoader


def json_render(path, template_file, params):
    """ Render a json template into json """
    path = os.path.dirname(path) + "/templates"
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(template_file)
    return json.loads(template.render(params))
