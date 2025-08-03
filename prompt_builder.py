import yaml
from jinja2 import Template

def render_template(yaml_path, context):
    with open(yaml_path, 'r') as f:
        raw_template = f.read()

    rendered = Template(raw_template).render(**context)
    return yaml.safe_load(rendered)

