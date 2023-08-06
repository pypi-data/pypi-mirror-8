from markdown import markdown as _markdown
from jingo import register
from jinja2 import Markup

@register.filter
def markdown(text, *args, **kwargs):
    """
    Parse text with markdown library.

    :param text:   - text for parsing;
    :param args:   - markdown arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
    :param kwargs: - markdown keyword arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
    :return:       - parsed result.
    """
    return Markup(_markdown(text, *args, **kwargs))
