#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of klove
# License: GPLv3
# See the documentation at benvial.gitlab.io/klove

from .__about__ import __author__, __description__, __version__

try:
    import numdiff
    from numdiff import *
    from numdiff import _reload_package

    def set_backend(backend):
        numdiff.set_backend(backend)
        _reload_package("klove")

    BACKEND = get_backend()

except:
    import numpy as backend

    def set_backend(backend):
        pass

    BACKEND = "numpy"


from .core import *
from .viz import *
