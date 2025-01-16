"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from __future__ import annotations

import datetime

# -- Project information -----------------------------------------------------

project = "Contrail Forecast"
copyright = f"{datetime.datetime.now().year}, Contrails.org, Google"

author = "Contrails.org, Google"
version = "1"
release = "1"

# -- General configuration ---------------------------------------------------

# parsed files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.imgconverter",
    "sphinx.ext.mathjax",
    # https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html
    "sphinxcontrib.bibtex",
    # https://nbsphinx.readthedocs.io/en/0.8.5/
    "nbsphinx",
    # https://sphinx-copybutton.readthedocs.io/en/latest/
    "sphinx_copybutton",
    # Markdown parsing, https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
    "myst_parser",
    # https://github.com/jbms/sphinx-immaterial/issues/38#issuecomment-1055785564
    "IPython.sphinxext.ipython_console_highlighting",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "drafts/**",
]

# suppress warnings during build
suppress_warnings = ["myst.header"]

# Display todos by setting to True
todo_include_todos = True

# Add references in bibtex format here
# use with :cite:`perez2011python` etc
# See the References section of the README for instructions to add new references
bibtex_bibfiles = ["_static/references.bib"]
bibtex_reference_style = "author_year"
bibtex_default_style = "unsrt"
bibtex_cite_id = "cite-{key}"

nbsphinx_timeout = 600
nbsphinx_execute = "never"

# Allow headers to be linkable to level 3.
myst_heading_anchors = 3

# Disable myst translations
myst_disable_syntax: list[str] = []

# Optional MyST Syntaxes
myst_enable_extensions: list[str] = []

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-pygments_style
# https://pygments.org/styles/
pygments_style = "default"
pygments_dark_style = "monokai"  # furo-specific

# https://sphinx-copybutton.readthedocs.io/en/latest/use.html#strip-and-configure-input-prompts-for-code-cells
copybutton_prompt_text = "$ "


# -- Options for HTML output -------------------------------------------------

# https://github.com/pradyunsg/furo
html_theme = "furo"
html_title = f"{project} v{release}"

# Adds a "last updated on" to the bottom of each page
# Set to None to disable
html_last_updated_fmt = ""

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "source_repository": "https://github.com/contrailcirrus/contrail-forecast",
    "source_branch": "main",
    "source_directory": "docs/",
    # "sidebar_hide_name": False,   # default
    # "top_of_page_button": "edit", # default
    # this adds a github icon to the footer. Ugly, but useful.
    # See https://pradyunsg.me/furo/customisation/footer/#using-embedded-svgs
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/contrailcirrus/contrail-forecast",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
    # "light_css_variables": {
    #     "color-brand-primary": "#0F6F8A",
    #     "color-brand-content": "#0F6F8A",
    # },
    # "dark_css_variables": {
    #     "color-brand-primary": "#34C3EB",
    #     "color-brand-content": "#34C3EB",
    # },
    # Note these paths must be relative to `_static/`
    # "light_logo": "img/logo.png",
    # "dark_logo": "img/logo-dark.png",
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = "_static/img/logo.png"
html_favicon = "_static/img/favicon.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/style.css"]
# html_js_files = []

html_sourcelink_suffix = ""

# -- Options for Latex output -------------------------------------------------

# latex_logo = "_static/img/logo.png"
