""" Jinja2 templates """

import os
import json
from jinja2 import Environment, FileSystemLoader


def plain_render(path, template_file, params):
    """Render plain-text template"""
    path = os.path.dirname(path) + "/templates"
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(template_file)
    return template.render(params)


def json_render(path, template_file, params):
    """Render a json template into json"""
    path = os.path.dirname(path) + "/templates"
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(template_file)
    return json.loads(template.render(params))
