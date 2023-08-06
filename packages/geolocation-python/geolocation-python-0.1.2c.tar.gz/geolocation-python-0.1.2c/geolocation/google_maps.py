#!/usr/bin/env python
# encoding: utf-8

from geolocation.models import LocationModel
from geolocation.parsers import GeocodeParser
from geolocation.api import GeocodeApi
import logging


class GoogleMaps(object):
    """To find address use: GoogleMaps.search(location=full_address)."""
    _geocode_parser = GeocodeParser()
    _data = set()

    log = logging.Logger('google_maps')

    def __init__(self, api_key):
        self._geocode_api = GeocodeApi(api_key)
        self._reset_data()

    def __repr__(self):
        return '<GoogleMaps %s >' % self.all()

    def _reset_data(self):
        self._data = set()

    def _to_python(self, json_results):
        """Method should converts json_results to python object."""
        for item in json_results:
            self._geocode_parser.json_data = item

            location = LocationModel()

            location.city = self._geocode_parser.get_city()
            location.route = self._geocode_parser.get_route()
            location.street_number = self._geocode_parser.get_street_number()
            location.postal_code = self._geocode_parser.get_postal_code()

            location.country = self._geocode_parser.get_country()
            location.country_shortcut =\
                self._geocode_parser.get_country_shortcut()

            location.administrative_area =\
                self._geocode_parser.get_administrative_area()

            location.lat = self._geocode_parser.get_lat()
            location.lng = self._geocode_parser.get_lng()

            location.formatted_address =\
                self._geocode_parser.get_formatted_address()

            self._data.add(location)

        return self.all()

    def all(self):
        """Method returns location list."""
        return list(self._data)

    def first(self):
        if self._data:
            return list(self._data)[0]

        return None

    def search(self, location=None, lat=None, lng=None):
        json_results = self._geocode_api.query(location=location, lat=lat, lng=lng)

        if json_results:
            self._to_python(json_results)

        return self

    def query(self, location):
        """Main method should returns GoogleMaps instance."""

        self.log.warning(
            'This method is deprecated. You should call search() method.')

        return self.search(location)
