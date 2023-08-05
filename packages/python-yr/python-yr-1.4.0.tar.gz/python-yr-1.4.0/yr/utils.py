#!/usr/bin/env python3

import sys
import os.path
import json # Language
import tempfile # Cache
import datetime # Cache
import urllib.request # Connect
import urllib.parse # Location

class YrObject: encoding = 'utf-8'

class YrException(Exception):
    pass

class Language(YrObject):

    script_directory = os.path.dirname(os.path.abspath(__file__)) # directory of the script
    directory = 'languages'

    def __init__(self, language_name='en'):
        self.language_name = language_name
        self.filename = os.path.join(
            self.script_directory,
            self.directory,
            '{root}.{ext}'.format(root=self.language_name, ext='json') # basename of filename
        )
        self.dictionary = self.get_dictionary()

    def get_dictionary(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', encoding=self.encoding) as f:
                return json.load(f)
        else:
            raise YrException('unavailable language ~> {language_name}'.format(language_name=self.language_name))

class Location(YrObject):

    def __init__(self, location_name, forecast_link='forecast', language=Language()):
        self.location_name = location_name
        self.forecast_link = forecast_link
        self.language = language
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        url = 'http://www.yr.no/{place}/{location_name}/{forecast_link}.xml'.format(
            location_name = urllib.parse.quote(self.location_name),
            forecast_link = urllib.parse.quote(self.forecast_link),
            **self.language.dictionary # **self.language.dictionary contain ~> place + forecast_link
        )
        return url

    def get_hash(self):
        return self.location_name.replace('/', '-')

class LocationXYZ(YrObject):
    """Class to use the API of yr.no"""

    def __init__(self, x, y, z=0, language=Language()):
        """
        :param double x: longitude coordinate
        :param double y: latitude coordinate
        :param double z: altitude (meters above sea level)
        :param language: a Language object
        """
        self.x = x
        self.y = y
        self.z = z
        self.language = language
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        """Return the url of API service"""
        url = "http://api.yr.no/weatherapi/locationforecast/1.9/?lat={y};" \
              "lon={x};msl={z}".format(x=self.x, y=self.y, z=self.z)
        return url

    def get_hash(self):
        """Create an hash with the three coordinates"""
        return "location_{x}_{y}_{z}".format(x=self.x, y=self.y, z=self.z)

class Connect(YrObject):

    def __init__(self, location):
        self.location = location

    def read(self):
        cache = Cache(self.location)
        if not cache.exists() or not cache.is_fresh():
            try:
                response = urllib.request.urlopen(self.location.url)
            except:
                raise YrException('unavailable url ~> {url}'.format(url=self.location.url))
            if response.status != 200:
                raise YrException('unavailable url ~> {url}'.format(url=self.location.url))
            weatherdata = response.read().decode(self.encoding)
            cache.dump(weatherdata)
        else:
            weatherdata = cache.load()
        return weatherdata

class Cache(YrObject):

    directory = tempfile.gettempdir()
    extension = 'weatherdata.xml'
    timeout = 30 # cache timeout in minutes

    def __init__(self, location):
        self.location = location
        self.filename = os.path.join(
            self.directory,
            '{root}.{ext}'.format(root=self.location.hash, ext=self.extension) # basename of filename
        )

    def dump(self, data):
        with open(self.filename, mode='w', encoding=self.encoding) as f:
            f.write(data)

    def is_fresh(self):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))
        now = datetime.datetime.now()
        timeout = datetime.timedelta(minutes=self.timeout)
        return now - mtime <= timeout # thanks for the fix antorweep

    def exists(self):
        return os.path.isfile(self.filename)

    def load(self):
        with open(self.filename, mode='r', encoding=self.encoding) as f:
            return f.read()

if __name__ == '__main__':
    print(Connect(Location(location_name='Czech_Republic/Prague/Prague')).read())
