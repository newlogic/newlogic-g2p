import os
import re
import sys

from sphinx.locale import _

# Prefer to use the version of the theme in this repo
# and not the installed version of the theme.
sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("./demo/"))
sys.path.append(os.path.abspath("./using/"))


project = "Newlogic G2P"
slug = re.sub(r"\W+", "-", project.lower())
version = "0.1"
# release = theme_version_full
author = "Newlogic Pte. Ltd."
# copyright = author
copyright = "2022 Newlogic Pte. Ltd. Licensed under CC BY 4.0"  # pylint: disable=redefined-builtin
language = "en"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinxcontrib.httpdomain",
    "sphinx_rtd_theme",
    "myst_parser",
]

templates_path = ["_templates"]
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}
exclude_patterns = []
locale_dirs = ["locale/"]
gettext_compact = False

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

master_doc = "index"
suppress_warnings = ["image.nonlocal_uri"]
pygments_style = "default"

intersphinx_mapping = {
    "rtd": ("https://docs.readthedocs.io/en/stable/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

html_theme = "sphinx_rtd_theme"
html_title = "Newlogic G2P Docs"
html_theme_options = {
    "logo_only": False,
    "navigation_depth": 5,
}
html_context = {
    "display_github": True,
    "github_user": "newlogic",  # Username
    "github_repo": "newlogic_g2p",  # Repo name
    "github_version": "main",  # Version
    "conf_py_path": "/docs/",  # Path in the checkout to the docs root
}

if "READTHEDOCS" not in os.environ:
    html_static_path = ["_static/"]
    html_js_files = ["debug.js"]

    # Add fake versions for local QA of the menu
    # html_context["test_versions"] = list(map(lambda x: str(x / 10), range(1, 100)))

# html_logo = "demo/static/logo-wordmark-light.svg"
html_show_sourcelink = True

htmlhelp_basename = slug


latex_documents = [
    ("index", "{}.tex".format(slug), project, author, "manual"),
]

man_pages = [("index", slug, project, [author], 1)]

texinfo_documents = [
    ("index", slug, project, author, slug, project, "Miscellaneous"),
]


# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field

    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
        doc_field_types=[
            PyField(
                "type",
                label=_("Type"),
                has_arg=False,
                names=("type",),
                bodyrolename="class",
            ),
            Field(
                "default",
                label=_("Default"),
                has_arg=False,
                names=("default",),
            ),
        ],
    )


todo_include_todos = True

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
