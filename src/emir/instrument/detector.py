#
# Copyright 2008-2013 Universidad Complutense de Madrid
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

import itertools as ito

import numpy

from numina.treedict import TreeDict
from numina.instrument.detector import nIRDetector, Channel, DAS
from numina.instrument.detector import SingleReadoutMode
from numina.instrument.detector import CdsReadoutMode
from numina.instrument.detector import RampReadoutMode
from numina.instrument.detector import FowlerReadoutMode

from .channels import CHANNELS, CHANNELS_2, CHANNELS_3, CHANNELS_READOUT
from .channels import CHANNELS_READOUT_2, QUADRANTS

class EMIR_DAS(DAS):
    def __init__(self, detector):
        super(EMIR_DAS, self).__init__(detector)
                
    def readout_mode_single(self, repeat=1):
        self.readmode(SingleReadoutMode(repeat=repeat)) 
    
    def readout_mode_cds(self, repeat=1):
        mode = CdsReadoutMode(repeat=repeat)
        self.readmode(mode)
    
    def readout_mode_fowler(self, reads, repeat=1, readout_time=0.0):
        mode = FowlerReadoutMode(reads, repeat=repeat, 
                                 readout_time=readout_time)
        self.readmode(mode)    

    def readout_mode_ramp(self, reads, repeat=1):
        mode = RampReadoutMode(reads, repeat=repeat)
        self.readmode(mode)

class EMIR_Detector_1(nIRDetector):
    def __init__(self, dark=0.25, flat=1.0, bad_pixel_mask=None):
        gain = 3.02
        ron = 2.1 # ADU
        pedestal = 5362
        wdepth = 55292
        saturation = 57000
        channels = [Channel((slice(0,2048), slice(0,2048)), gain, ron, pedestal, wdepth, saturation)]
        super(EMIR_Detector_1, self).__init__((2048, 2048), channels, 
                dark=dark, flat=flat,
                bad_pixel_mask=bad_pixel_mask)

class EMIR_Detector_4(nIRDetector):
    def __init__(self, dark=0.25, flat=1.0, bad_pixel_mask=None):
        gain = [3.02, 2.98, 3.00, 2.91]
        ron = [2.1, 1.9, 1.9, 2.2] # Electrons
        pedestal = [5362, 5362, 5362, 5362]
        wdepth = [55292, 56000, 56000, 56000]
        saturation = [57292, 57000, 57000, 57000]

        channels = [Channel(*vs) for vs in zip(QUADRANTS, gain, ron, pedestal, 
        wdepth, saturation)]
        super(EMIR_Detector_4, self).__init__((2048, 2048), channels, 
                dark=dark, flat=flat,
                bad_pixel_mask=bad_pixel_mask)

class EMIR_Detector_32(nIRDetector):
    def __init__(self, dark=0.25, flat=1.0, bad_pixel_mask=None):
        # from Carlos Gonzalez Thesis, page 147
        # ADU
        ron = [2.03, 1.98, 1.96, 1.95, 1.99, 1.95, 1.97, 1.95,
               1.94, 1.96, 1.94, 1.92, 2.03, 1.93, 1.96, 1.98,
               2.01, 1.99, 1.97, 1.98, 1.99, 1.97, 1.97, 2.00,
               2.02, 2.02, 2.05, 1.98, 2.00, 2.02, 2.01, 2.03
              ]

        # from Carlos Gonzalez Thesis, page 127
        # e-/ADU
        gain = [3.08, 2.90, 2.68, 3.12, 2.63, 3.10, 3.00, 3.02,
                3.18, 3.11, 3.09, 3.19, 3.11, 2.99, 2.60, 3.02,
                2.99, 3.16, 3.18, 3.11, 3.17, 3.07, 3.12, 3.02,
                2.92, 3.07, 2.90, 2.91, 2.95, 3.00, 3.01, 3.01
                ]

        # ADU per AMP
        wdepth = [42353.1, 42148.3, 42125.5, 42057.9, 41914.1, 42080.2, 42350.3, 
                  41830.3, 41905.3, 42027.9, 41589.5, 41712.7, 41404.9, 41068.5, 
                  40384.9, 40128.1, 41401.4, 41696.5, 41461.1, 41233.2, 41351.0, 
                  41803.7, 41450.2, 41306.2, 41609.4, 41414.1, 41324.5, 41691.1, 
                  41360.0, 41551.2, 41618.6, 41553.5]
        
        pedestal = [5362]*32
        saturation = [57000]*32

        channels = [Channel(*vs) for vs in zip(CHANNELS_3, gain, ron, pedestal, wdepth, saturation)]
        super(EMIR_Detector_32, self).__init__((2048, 2048), channels, 
                dark=dark,flat=flat,
                bad_pixel_mask=bad_pixel_mask)

EMIR_Detector = EMIR_Detector_32
