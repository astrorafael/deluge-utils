# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) 2021
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

# Access template within the package
#from pkg_resources import resource_filename

# ---------------
# Airflow imports
# ---------------

#--------------
# local imports
# -------------

from ._version import get_versions


# ----------------
# Module constants
# ----------------

#HTML_TEMPLATE = resource_filename(__name__, 'templates/kit-template.j2')

__version__ = get_versions()['version']

del get_versions
