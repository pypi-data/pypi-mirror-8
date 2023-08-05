'''
HDF parser specific to TES files.

@author: Luca Cinquini
'''
import datetime as dt
from esgfpy.publish.parsers import HdfMetadataFileParser
import os
import re
from dateutil.tz import tzutc
import numpy as np
from esgfpy.publish.consts import TAI93_DATETIME_START

# TES-Aura_L2-CO2-Nadir_r0000015508_C01_F07_10.he5
FILENAME_PATTERN = "TES-Aura_L2-CO2-Nadir_.+10\.he5"

class TesFileParser(HdfMetadataFileParser):
    
    def matches(self, filepath):
        '''Example filename: TES-Aura_L2-CO2-Nadir_r0000015508_C01_F07_10.he5'''
        dir, filename = os.path.split(filepath)
        return re.match(FILENAME_PATTERN, filename)
    
    def getLatitudes(self, h5file):
        return h5file['HDFEOS']['SWATHS']['CO2NadirSwath']['Geolocation Fields']['Latitude'][:]
 
    def getLongitudes(self, h5file):
        return h5file['HDFEOS']['SWATHS']['CO2NadirSwath']['Geolocation Fields']['Longitude'][:]
    
    def getTimes(self, h5file):
        
        # uses TAI time
        seconds = h5file['HDFEOS']['SWATHS']['CO2NadirSwath']['Geolocation Fields']['Time'][:]
        times = []
        for secs in seconds:
            if secs>0: # avoid Time:MissingValue = -999. ;
                utcdateTime = TAI93_DATETIME_START + dt.timedelta(seconds=int(secs)) - dt.timedelta(seconds=35)
                times.append( utcdateTime )
        return np.asarray(times, dtype=dt.datetime)
    
    def getVariables(self, h5file):
        
        variables = []
        for vname, vobj in h5file['HDFEOS']['SWATHS']['CO2NadirSwath']['Data Fields'].items():
            variables.append(str(vname))
    
        return variables