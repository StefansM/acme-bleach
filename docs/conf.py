"""Sphinx configuration."""
project = "Acme Bleach"
author = "Stefans Mezulis"
copyright = "2023, Stefans Mezulis"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
