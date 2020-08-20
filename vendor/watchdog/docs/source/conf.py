# -*- coding: utf-8 -*-
#
# watchdog documentation build configuration file, created by
# sphinx-quickstart on Tue Nov 30 00:43:58 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os.path

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
TOP_DIR_PATH = os.path.abspath('../../')  # noqa
SRC_DIR_PATH = os.path.join(TOP_DIR_PATH, 'src')  # noqa
sys.path.insert(0, SRC_DIR_PATH)  # noqa

import watchdog.version

PROJECT_NAME = 'watchdog'
AUTHOR_NAME = 'Yesudeep Mangalapilly and contributors'
COPYRIGHT = '2010-2020, ' + AUTHOR_NAME


# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of armada filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = PROJECT_NAME
copyright = COPYRIGHT

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = watchdog.version.VERSION_STRING
# The full version, including alpha/beta/rc tags.
release = version

# List of patterns, relative to armada directory, that match files and
# directories to ignore when looking for armada files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'pyramid'

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % PROJECT_NAME


# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (armada start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ('index', '%s.tex' % PROJECT_NAME, '%s Documentation' % PROJECT_NAME,
     AUTHOR_NAME, 'manual'),
]

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (armada start file, name, description, authors, manual section).
man_pages = [
    ('index', PROJECT_NAME, '%s Documentation' % PROJECT_NAME,
     [AUTHOR_NAME], 1)
]


# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = PROJECT_NAME
epub_author = AUTHOR_NAME
epub_publisher = AUTHOR_NAME
epub_copyright = COPYRIGHT
