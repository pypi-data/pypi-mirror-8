import httplib # Used only for handling httplib.HTTPException (case #26701)
import os
import sys
import platform
import re
import urllib
import urllib2
import traceback
import time
from StringIO import StringIO


from kunai.log import logger
from kunai.collector import Collector


class NetworkTraffic(Collector):
    def launch(self):
        logger.debug('getNetworkTraffic: start')

        if sys.platform == 'linux2':
            logger.debug('getNetworkTraffic: linux2')

            try:
                logger.debug('getNetworkTraffic: attempting open')
                proc = open('/proc/net/dev', 'r')
                lines = proc.readlines()
                proc.close()

            except IOError, e:
                logger.error('getNetworkTraffic: exception = %s', e)
                return False

            logger.debug('getNetworkTraffic: open success, parsing')

            columnLine = lines[1]
            _, receiveCols , transmitCols = columnLine.split('|')
            receiveCols = map(lambda a:'recv_' + a, receiveCols.split())
            transmitCols = map(lambda a:'trans_' + a, transmitCols.split())

            cols = receiveCols + transmitCols

            logger.debug('getNetworkTraffic: parsing, looping')

            faces = {}
            for line in lines[2:]:
                if line.find(':') < 0: continue
                face, data = line.split(':')
                faceData = dict(zip(cols, data.split()))
                faces[face] = faceData

            logger.debug('getNetworkTraffic: parsed, looping')

            interfaces = {}

            # Now loop through each interface
            for face in faces:
                key = face.strip()

                # We need to work out the traffic since the last check so first time we store the current value
                # then the next time we can calculate the difference
                try:
                    if key in self.networkTrafficStore:
                        interfaces[key] = {}
                        interfaces[key]['recv_bytes'] = long(faces[face]['recv_bytes']) - long(self.networkTrafficStore[key]['recv_bytes'])
                        interfaces[key]['trans_bytes'] = long(faces[face]['trans_bytes']) - long(self.networkTrafficStore[key]['trans_bytes'])

                        if interfaces[key]['recv_bytes'] < 0:
                            interfaces[key]['recv_bytes'] = long(faces[face]['recv_bytes'])

                        if interfaces[key]['trans_bytes'] < 0:
                            interfaces[key]['trans_bytes'] = long(faces[face]['trans_bytes'])

                        # Get the traffic
                        interfaces[key]['recv_bytes/s'] = interfaces[key]['recv_bytes'] / 10
                        interfaces[key]['trans_bytes/s'] = interfaces[key]['trans_bytes'] / 10

                        interfaces[key]['recv_bytes'] = str(interfaces[key]['recv_bytes'])
                        interfaces[key]['trans_bytes'] = str(interfaces[key]['trans_bytes'])


                        # And update the stored value to subtract next time round
                        self.networkTrafficStore[key]['recv_bytes'] = faces[face]['recv_bytes']
                        self.networkTrafficStore[key]['trans_bytes'] = faces[face]['trans_bytes']

                    else:
                        self.networkTrafficStore[key] = {}
                        self.networkTrafficStore[key]['recv_bytes'] = faces[face]['recv_bytes']
                        self.networkTrafficStore[key]['trans_bytes'] = faces[face]['trans_bytes']

                    # Logging
                    logger.debug('getNetworkTraffic: %s = %s', key, self.networkTrafficStore[key]['recv_bytes'])
                    logger.debug('getNetworkTraffic: %s = %s', key, self.networkTrafficStore[key]['trans_bytes'])

                except KeyError, ex:
                    logger.error('getNetworkTraffic: no data for %s', key)

                except ValueError, ex:
                    logger.error('getNetworkTraffic: invalid data for %s', key)

            logger.debug('getNetworkTraffic: completed, returning')

            return interfaces

        elif sys.platform.find('freebsd') != -1:
            logger.debug('getNetworkTraffic: freebsd')

            try:
                try:
                    logger.debug('getNetworkTraffic: attempting Popen (netstat)')

                    proc = subprocess.Popen(['netstat', '-nbid'], stdout=subprocess.PIPE, close_fds=True)
                    netstat = proc.communicate()[0]

                    if int(pythonVersion[1]) >= 6:
                        try:
                            proc.kill()
                        except Exception, e:
                            logger.debug('Process already terminated')

                except Exception, e:
                    logger.error('getNetworkTraffic: exception = %s', traceback.format_exc())

                    return False
            finally:
                if int(pythonVersion[1]) >= 6:
                    try:
                        proc.kill()
                    except Exception, e:
                        logger.debug('Process already terminated')

            logger.debug('getNetworkTraffic: open success, parsing')

            lines = netstat.split('\n')

            # Loop over available data for each inteface
            faces = {}
            rxKey = None
            txKey = None

            for line in lines:
                logger.debug('getNetworkTraffic: %s', line)

                line = re.split(r'\s+', line)

                # Figure out which index we need
                if rxKey == None and txKey == None:
                    for k, part in enumerate(line):
                        logger.debug('getNetworkTraffic: looping parts (%s)', part)

                        if part == 'Ibytes':
                            rxKey = k
                            logger.debug('getNetworkTraffic: found rxKey = %s', k)
                        elif part == 'Obytes':
                            txKey = k
                            logger.debug('getNetworkTraffic: found txKey = %s', k)

                else:
                    if line[0] not in faces:
                        try:
                            logger.debug('getNetworkTraffic: parsing (rx: %s = %s / tx: %s = %s)', rxKey, line[rxKey], txKey, line[txKey])
                            faceData = {'recv_bytes': line[rxKey], 'trans_bytes': line[txKey]}

                            face = line[0]
                            faces[face] = faceData
                        except IndexError, e:
                            continue

            logger.debug('getNetworkTraffic: parsed, looping')

            interfaces = {}

            # Now loop through each interface
            for face in faces:
                key = face.strip()

                try:
                    # We need to work out the traffic since the last check so first time we store the current value
                    # then the next time we can calculate the difference
                    if key in self.networkTrafficStore:
                        interfaces[key] = {}
                        interfaces[key]['recv_bytes'] = long(faces[face]['recv_bytes']) - long(self.networkTrafficStore[key]['recv_bytes'])
                        interfaces[key]['trans_bytes'] = long(faces[face]['trans_bytes']) - long(self.networkTrafficStore[key]['trans_bytes'])

                        interfaces[key]['recv_bytes'] = str(interfaces[key]['recv_bytes'])
                        interfaces[key]['trans_bytes'] = str(interfaces[key]['trans_bytes'])

                        if interfaces[key]['recv_bytes'] < 0:
                            interfaces[key]['recv_bytes'] = long(faces[face]['recv_bytes'])

                        if interfaces[key]['trans_bytes'] < 0:
                            interfaces[key]['trans_bytes'] = long(faces[face]['trans_bytes'])



                        # And update the stored value to subtract next time round
                        self.networkTrafficStore[key]['recv_bytes'] = faces[face]['recv_bytes']
                        self.networkTrafficStore[key]['trans_bytes'] = faces[face]['trans_bytes']

                    else:
                        self.networkTrafficStore[key] = {}
                        self.networkTrafficStore[key]['recv_bytes'] = faces[face]['recv_bytes']
                        self.networkTrafficStore[key]['trans_bytes'] = faces[face]['trans_bytes']

                except KeyError, ex:
                    logger.error('getNetworkTraffic: no data for %s', key)

                except ValueError, ex:
                    logger.error('getNetworkTraffic: invalid data for %s', key)

            logger.debug('getNetworkTraffic: completed, returning')

            return interfaces

        else:
            logger.debug('getNetworkTraffic: other platform, returning')

            return False
