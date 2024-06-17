# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Assurez-vous que le chemin vers votre projet est correct
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../vis'))
sys.path.insert(0, os.path.abspath('../cont_eval_proj'))

# Définir le module de paramètres Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'cont_eval_proj.settings'

# Initialiser Django
import django
django.setup()

project = 'IRLEI'
copyright = '2024, Pernier/Sage'
author = 'Pernier/Sage'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'  # Si vous préférez 'furo' au lieu de 'alabaster'
html_static_path = ['_static']