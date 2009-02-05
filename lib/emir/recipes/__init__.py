#!/usr/bin/env python

#
# Copyright 2008-2009 Sergio Pascual
# 
# This file is part of PyEmir
# 
# PyEmir is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyEmir is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyEmir.  If not, see <http://www.gnu.org/licenses/>.
# 

# $Id$

import logging
from optparse import OptionParser

logger = logging.getLogger("emir.recipes")

class Recipe:
    parser =  OptionParser(usage = "usage: %prog [options] recipe [recipe-options]")
    parser.add_option('-e',action="store_true", dest="test", default=False, help="test documentation")
    def run(self):
        logger.info("Hello, I\'m Recipe")