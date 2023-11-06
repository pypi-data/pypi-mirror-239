import json
import logging
import os
import tempfile
import datetime

cache_timeformat = '%Y-%m-%d %H:%M:%S'


class CacheEntry():
    def __init__(self, entryName,  time, expiry, data={}) -> None:
        self.entryName = entryName
        self.time = time
        self.expiry = expiry
        self.data = data

    def isExpired(self):
        isExpired = False
        delta = datetime.datetime.now() - self.time
        if delta >= self.expiry:
            isExpired = True
        else:
            isExpired = False

        return isExpired

    def __name__(self):
        return self.entryName

    def __dict__(self):
        return {'name': self.entryName, 'time': self.time, 'expiry': self.expiry, 'data': dict(self.data)}


class CacheManager():
    def __init__(self, cachefile='ic2pychecker_cache.json') -> None:
        self.path = os.path.join(tempfile.gettempdir(), 'pyIcingaFramework', cachefile)
        self.cache = {}
        self.cache['entries'] = []
        self.cache_version = 1.0

        logging.info(f'Loading cachefile: {self.path}')
        self.loadCache(self.path)

    def getEntry(self, entryName):
        logging.debug(f'searching for cache entry {entryName}')
        for entry in self.cache['entries']:
            if entry.name.lower() == entryName.lower():
                return entry

        return None

    def createCacheFile(self, path):
        logging.debug(f'Looking for cachefile {path}')
        if not os.path.exists(path):
            logging.debug(f' creating cachefile {path}')
            self.cache["pyIcingaFramework"] = self.cache_version
            logging.debug(f' commiting cachefile {path}')
            self.commitCache()

    def loadCache(self, path):
        logging.info(f'Looking for cachefile {path}')

        if os.path.exists(path):
            with open(path, 'r') as cache:
                try:
                    cacheData = json.load(cache)
                    if not cacheData.get('pyIcingaFramework', None):
                        logging.error(f'Cache file {path} is not a pyIcingaFramework cache file')
                        self.cache["pyIcingaFramework"] = self.cache_version
                    else:
                        logging.info('looping entries')
                        entries = self.cacheData.get('entries')
                        for entry in entries:
                            self.cache['entries'].append(CacheEntry(entry['name'],
                                                                    entry['time'],
                                                                    entry['expiry'],
                                                                    entry['data']))

                        self.cache = cacheData
                except Exception as e:
                    logging.error(f'Cache file {path} is not a json file')
                    logging.debug(e)
        else:
            logging.info(f'No  Cache file at {path}')
            self.createCacheFile(path)

    def commitCache(self):
        logging.debug(f'cache to commit: {self.cache}')
        if os.path.exists(os.path.join(tempfile.gettempdir(), 'pyIcingaFramework')) is False:
            os.mkdir(os.path.join(tempfile.gettempdir(), 'pyIcingaFramework'))
            
        jsondata = json.dumps(self.cache, default=lambda x: x.__dict__)
        logging.info('commiting cache:')
        with open(self.path, "w") as f:
            f.write(jsondata)

    def setCache(self, module: str, cacheEntry: CacheEntry):
        logging.debug(f'Caching {module}, data: {cacheEntry.__dict__()}')

        logging.debug(f'Adding cache to pollercache[{module}][{cacheEntry.entryName}]')
        self.cache['entries'].append(cacheEntry.__dict__())
