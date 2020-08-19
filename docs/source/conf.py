# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import mock

print('doc path = {0}'.format(os.path.abspath('../../')))

sys.path.insert(0, os.path.abspath('../../'))

for module in [
	"maya", "maya.mel", "maya.cmds", "maya.OpenMaya", "maya.OpenMayaUI" "wrapInstance", "shiboken",
	"hou", "hdefereval", "bpy"
]:
	sys.modules[module] = mock.MagicMock()

# -- Project information -----------------------------------------------------

project = 'Armada'
copyright = '2020, Mike Bourbeau'
author = 'Mike Bourbeau'

# The full version, including alpha/beta/rc tags
release = '2020.8.12b'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.todo',
	'sphinx.ext.napoleon',
	'sphinx.ext.coverage',
	'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to armada directory, that match files and
# directories to ignore when looking for armada files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# A list of prefixes to ignore for module listings.
modindex_common_prefix = [
    'mb_armada.'
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']