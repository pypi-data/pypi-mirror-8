import os

import html5css3
import html
import json

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

BASE_PATH = os.path.dirname(__file__)

join_path = os.path.join

def as_list(val):
    """return a list with val if val is not already a list, val otherwise"""
    if isinstance(val, list):
        return val
    else:
        return [val]

def abspath(path):
    return join_path(BASE_PATH, path)

def js_fullpath(path, embed=True):
    content = open(path).read().decode('utf-8')

    if embed:
        return html.Script(content)
    else:
        return html.Script(src=path)

def js(path, embed=True):
    return js_fullpath(abspath(path), embed)

def css(path, embed=True):
    content = open(abspath(path)).read().decode('utf-8')

    if embed:
        return html.Style(content, type="text/css")
    else:
        return html.Link(href=path, rel="stylesheet", type="text/css")

def pretty_print_code(tree, embed=True, params=None):
    head = tree[0]
    body = tree[1]

    body.append(js(join_path("thirdparty", "prettify.js"), embed))
    body.append(html.Script("$(function () { prettyPrint() })"))

    head.append(css(join_path("thirdparty", "prettify.css")))

def jquery(tree, embed=True, params=None):
    body = tree[1]
    body.append(js(join_path("thirdparty", "jquery.js"), embed))

def add_class(element, cls_name):
    cls = element.get("class", "")

    if cls:
        cls += " " + cls_name
    else:
        cls += cls_name

    element.set("class", cls)

def deckjs(tree, embed=True, params=None):
    head = tree[0]
    body = tree[1]

    def path(*args):
        return join_path("thirdparty", "deckjs", *args)

    head.remove(head.find("./style"))
    add_class(body, "deck-container")

    for section in tree.findall(".//section"):
        add_class(section, "slide")

    # Core and extension CSS files
    head.append(css(path("core", "deck.core.css"), embed))
    head.append(css(path("extensions", "goto", "deck.goto.css"), embed))
    head.append(css(path("extensions", "menu", "deck.menu.css"), embed))
    head.append(css(path("extensions", "navigation", "deck.navigation.css"), embed))
    head.append(css(path("extensions", "status", "deck.status.css"), embed))
    head.append(css(path("extensions", "hash", "deck.hash.css"), embed))

    # Theme CSS files (menu swaps these out)
    head.append(css(path("themes", "style", "web-2.0.css"), embed))
    head.append(css(path("themes", "transition", "horizontal-slide.css"), embed))

    body.append(js(path("modernizr.custom.js"), embed))
    jquery(tree, embed)

    # Deck Core and extensions
    body.append(js(path("core", "deck.core.js"), embed))
    body.append(js(path("extensions", "hash", "deck.hash.js"), embed))
    body.append(js(path("extensions", "menu", "deck.menu.js"), embed))
    body.append(js(path("extensions", "goto", "deck.goto.js"), embed))
    body.append(js(path("extensions", "status", "deck.status.js"), embed))
    body.append(js(path("extensions", "navigation", "deck.navigation.js"), embed))

    body.append(html.Script("$(function () { $.deck('.slide'); });"))

def add_js(tree, embed=True, params=None):
    params = params or {}
    paths = as_list(params.get("path", []))

    body = tree[1]
    for path in paths:
        body.append(js_fullpath(path, embed))

def revealjs(tree, embed=True, params=None):
    head = tree[0]
    body = tree[1]
    params = params or {}
    theme_name = params.pop("theme", "default") + ".css"
    theme_base_dir = params.pop("themepath", None)

    def path(*args):
        return join_path("thirdparty", "revealjs", *args)

    if theme_base_dir:
        theme_path = join_path(os.path.expanduser(theme_base_dir), theme_name)
    else:
        theme_path = path("css", "theme", theme_name)

    add_class(body, "reveal")
    slides = html.Div(class_="slides")

    for item in list(body):
        body.remove(item)
        slides.append(item)

    body.append(slides)

    # <link rel="stylesheet" href="css/reveal.css">
    # <link rel="stylesheet" href="css/theme/default.css" id="theme">
    head.append(css(path("css", "reveal.css"), embed))
    head.append(css(theme_path, embed))

    # <script src="lib/js/head.min.js"></script>
    # <script src="js/reveal.min.js"></script>
    body.append(js(path("lib", "js", "head.min.js"), embed))
    body.append(js(path("js", "reveal.min.js"), embed))

    head.append(css("rst2html5-reveal.css", embed))

    params['history'] = True
    param_s = json.dumps(params)
    body.append(
        html.Script("$(function () { Reveal.initialize(%s); });" % param_s))

def impressjs(tree, embed=True, params=None):
    head = tree[0]
    body = tree[1]

    def path(*args):
        return join_path("thirdparty", "impressjs", *args)

    # remove the default style
    #head.remove(head.find("./style"))
    add_class(body, "impress-not-supported")
    failback = html.Div('<div class="fallback-message">' +
        '<p>Your browser <b>doesn\'t support the features required</b> by' +
        'impress.js, so you are presented with a simplified version of this' +
        'presentation.</p>' +
        '<p>For the best experience please use the latest <b>Chrome</b>,' +
        '<b>Safari</b> or <b>Firefox</b> browser.</p></div>')

    slides = html.Div(id="impress")

    for item in list(body):
        body.remove(item)
        slides.append(item)

    body.append(slides)

    # <script src="js/impress.js"></script>
    body.append(js(path("js", "impress.js"), embed))

    body.append(html.Script("impress().init();"))

def bootstrap_css(tree, embed=True, params=None):
    head = tree[0]

    head.append(css(join_path("thirdparty", "bootstrap.css"), embed))
    head.append(css("rst2html5.css", embed))

def embed_images(tree, embed=True, params=None):
    import base64
    for image in tree.findall(".//img"):
        path = image.attrib['src']
        lowercase_path = path.lower()

        if lowercase_path.endswith(".png"):
            content_type = "image/png"
        elif lowercase_path.endswith(".jpg"):
            content_type = "image/jpg"
        elif lowercase_path.endswith(".gif"):
            content_type = "image/gif"
        else:
            continue

        encoded = base64.b64encode(open(path).read())
        content = "data:%s;base64,%s" % (content_type, encoded)
        image.set('src', content)

def pygmentize(tree, embed=True, params=None):
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter

    pygments_formatter = HtmlFormatter()
    body = tree[1]

    def highlight_code(lang, code):
        try:
            lexer = get_lexer_by_name(lang)
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = get_lexer_by_name('text')

        parsed = highlight(code, lexer, pygments_formatter)
        return parsed

    for block in body.findall(".//pre"):
        cls = block.attrib.get('class', '')
        classes = cls.split()
        if 'code' in classes:
            lang_classes = [cls for cls in classes if cls.startswith('lang-')]

            if len(lang_classes) > 0:
                lang = lang_classes[0][5:]

                new_content = highlight_code(lang, block.text)
                block.tag = 'div'
                block.text = new_content

def mathjax(tree, embed=True, params=None):
    body = tree[1]
    params = params or {}
    config_path = params.get("config")
    url = params.get("url", "http://cdn.mathjax.org/mathjax/latest/MathJax.js")


    if config_path is None:
        content = """
      MathJax.Hub.Config({
        extensions: [],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
          inlineMath: [ ['$','$'], ["\\(","\\)"] ],
          displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
          processEscapes: true
        },
        "HTML-CSS": { availableFonts: ["TeX"] }
      });
        """
    else:
        with open(config_path) as f_in:
            content = f_in.read()

    body.append(html.Script(content, type="text/x-mathjax-config"))
    body.append(html.Script(src=url))


PROCESSORS = {
    "mathjax": {
        "name": "add mathjax support",
        "processor": mathjax
    },
    "jquery": {
        "name": "add jquery",
        "processor": jquery
    },
    "pretty_print_code": {
        "name": "pretty print code",
        "processor": pretty_print_code
    },
    "pygments": {
        "name": "pygments",
        "processor": pygmentize
    },
    "deck_js": {
        "name": "deck.js",
        "processor": deckjs
    },
    "reveal_js": {
        "name": "reveal.js",
        "processor": revealjs
    },
    "impress_js": {
        "name": "impress.js",
        "processor": impressjs
    },
    "bootstrap_css": {
        "name": "bootstrap css",
        "processor": bootstrap_css
    },
    "embed_images": {
        "name": "embed images",
        "processor": embed_images
    },
    "add_js": {
        "name": "add js files",
        "processor": add_js
    }
}

class Code(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self):
        language = self.arguments[0]
        content = self.content

        attrs = {
            'class': "code lang-" + language
        }

        return [nodes.literal_block('', "\n".join(content), **attrs)]

class Slide3D(Directive):

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
            'x': int,
            'y': int,
            'z': int,
            'rotate': int,
            'rotate-x': int,
            'rotate-y': int,
            'scale': int,
            'class': directives.unchanged,
            'id': directives.unchanged,
            'title': directives.unchanged
    }
    has_content = True

    def run(self):
        attributes = {}

        for key, value in self.options.items():
            if key in ('class', 'id', 'title'):
                attributes[key] = value
            else:
                attributes['data-' + key] = value

        node = nodes.container(rawsource=self.block_text, **attributes)
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]

directives.register_directive('slide-3d', Slide3D)
directives.register_directive('code-block', Code)
