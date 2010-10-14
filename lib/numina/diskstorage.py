#
# Copyright 2008-2010 Sergio Pascual
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

import os
import shutil
try:
    import json
except ImportError:
    import simplejson as json
import logging

from pyfits import HDUList

from generic import generic
from jsonserializer import to_json
from numina.image import DiskImage
from numina.recipes import RecipeResult

_logger = logging.getLogger("numina.storage")

@generic
def store(obj, where=None):
    raise TypeError(repr(type(obj)) + ' is not storable')

@store.register(HDUList)
def _store_fits(obj, where=None):
    '''Save to disk an HDUList structure.'''
    where = where or obj['primary'].header.get('FILENAME', 'file.fits')
    obj.writeto(where, clobber=True, output_verify='ignore')

@store.register(DiskImage)
def _store_disk_image(obj, where=None):
    '''Save to disk a DiskImage structure.'''
    obj.open()
    fitsobj = obj.hdulist
    where = where or fitsobj['primary'].header.get('FILENAME', 'file.fits')
    # File already exists in obj.filename
    # Hardlink it or copy it
    try:
        os.link(obj.filename, where)
    except OSError, e:
        _logger.warning('Hardlinking %s: %s', obj.filename, e)
        # hardlinking failed
        shutil.copy(obj.filename, where)
    obj.close()

@store.register(RecipeResult)
def _store_rr(obj, where):
    '''Save to disk a RecipeResult.
    
    Every object registered with store will be substituted by
    a string containing a filename. The object will be saved
    in the filename.
    '''
    
    external = [] 
    
    parsed = _parse_rr(dict(obj), external)
        
    f = open(where, 'w+') 
    try:
        json.dump(parsed, f, default=to_json, indent=1, encoding='utf-8')
    finally:
        f.close()
        
    for filename, nobj in external:
        store(nobj, filename)

def _parse_rr(val, external):
    t = type(val)
    
    if store.is_registered(t):
        filename = generate_fname(val)
        external.append((filename, val))
        return '<file>: %s' % filename
    if t is dict:
        return dict(map(lambda x: (x[0], _parse_rr(x[1], external)), val.items()))
    if t is list or t is tuple:
        return map(lambda x: _parse_rr(x, external), val)
    return val

@generic
def generate_fname(obj):
    raise TypeError('A filename cannot be generated for % s' % repr(type(obj)))

@generate_fname.register(HDUList)
def _generate_fits(obj):
    '''Generate a filename for a HDUList structure.'''
    return obj['primary'].header.get('FILENAME', 'file.fits')

@generate_fname.register(DiskImage)
def _generate_fits(obj):
    '''Generate a filename for a  DiskImage structure.'''
    obj.open()
    fitsobj = obj.hdulist
    where = fitsobj['primary'].header.get('FILENAME', 'file.fits')
    obj.close()
    return where
