"""Sphinx configuration."""

project = "Gridworks Uploader"
author = "Andrew Schweitzer"
copyright = "2025, Andrew Schweitzer"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
