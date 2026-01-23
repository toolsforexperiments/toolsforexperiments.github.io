# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tools for Experiments'
copyright = '2026, Wolfgang Pfaff, Marcos Frenkel, Oliver Wolff'
author = 'Wolfgang Pfaff, Marcos Frenkel, Oliver Wolff'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser']

templates_path = ['_templates']
exclude_patterns = []

# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language = "en"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_baseurl = 'https://toolsforexperiments.github.io/toolsforexperiments/'

html_theme_options = {
    "logo": {
        "text": "Tools for Experiments",
    },
    "external_links": [
        {
            "url": "https://toolsforexperiments.github.io/labcore/",
            "name": "Labcore",
        },
        {
            "url": "https://toolsforexperiments.github.io/instrumentserver/",
            "name": "Instrumentserver",
        },
        {
            "url": "https://toolsforexperiments.github.io/plottr/",
            "name": "Plottr",
        },
        {
            "url": "https://toolsforexperiments.github.io/cqedtoolbox/",
            "name": "CQEDtoolbox",
        }

    ],
    "icon_links" : [
        {
            "name": "GitHub",
            "url": "https://github.com/toolsforexperiments",
            "icon": "fa-brands fa-github",
        }
    ]
}