import httplib # Used only for handling httplib.HTTPException (case #26701)
import os
import platform
import re
import urllib
import urllib2
import traceback
import time
from StringIO import StringIO


from kunai.log import logger
from kunai.collector import Collector


class DiskUsage(Collector):
    def launch(self):
        #logger.debug('getDiskUsage: start')

        #logger.debug('getDiskUsage: attempting Popen')

        _cmd = 'df -k -x smbfs -x tmpfs -x cifs -x iso9660 -x udf -x nfsv4'
        df = self.execute_shell(_cmd)
        if not df:
            return False
                
        #logger.debug('getDiskUsage: Popen success, start parsing')

        # Split out each volume
        volumes = df.split('\n')

        #logger.debug('getDiskUsage: parsing, split')

        # Remove first (headings) and last (blank)
        volumes.pop(0)
        volumes.pop()

        #logger.debug('getDiskUsage: parsing, pop')

        usageData = []

        regexp = re.compile(r'([0-9]+)')

        # Set some defaults
        previousVolume = None
        volumeCount = 0

        #logger.debug('getDiskUsage: parsing, start loop')

        for volume in volumes:
            #logger.debug('getDiskUsage: parsing volume: %s', volume)

            # Split out the string
            volume = volume.split(None, 10)

            # Handle df output wrapping onto multiple lines (case 27078 and case 30997)
            # Thanks to http://github.com/sneeu
            if len(volume) == 1: # If the length is 1 then this just has the mount name
                previousVolume = volume[0] # We store it, then continue the for
                continue

            if previousVolume != None: # If the previousVolume was set (above) during the last loop
                volume.insert(0, previousVolume) # then we need to insert it into the volume
                previousVolume = None # then reset so we don't use it again

            volumeCount = volumeCount + 1

            # Sometimes the first column will have a space, which is usually a system line that isn't relevant
            # e.g. map -hosts              0         0          0   100%    /net
            # so we just get rid of it
            # Also ignores lines with no values
            if re.match(regexp, volume[1]) == None or re.match(regexp, volume[2]) == None or re.match(regexp, volume[3]) == None:
                pass
            else:
                #print "DUMPING VOLUME", volume
                try:
                    volume[1] = int(volume[1]) / 1024  # total
                    volume[2] = int(volume[2]) / 1024  # Used
                    volume[3] = int(volume[3]) / 1024  # Available
                except Exception, e:
                    logger.error('getDiskUsage: parsing, loop %s - Used or Available not present' % (repr(e),))
                usageData.append(volume)

        return usageData

