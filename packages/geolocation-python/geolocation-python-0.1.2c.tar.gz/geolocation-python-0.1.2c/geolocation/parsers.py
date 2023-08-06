# -*- coding: utf-8 -*-


class GeocodeParser(object):
    _json_data = None

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, value):
        self._json_data = value

    def set_json_data(self, value):
        """Method sets value to json_data"""
        self.json_data = value

    def _search_address_components(self, type_, shortcut=False):
        """Method searches address components in google maps json data."""
        if not self.json_data:
            return None

        for address_component in self.json_data['address_components']:
            types = address_component['types']

            if type_ in types:
                if shortcut:
                    return address_component['short_name'].encode('utf-8')
                else:
                    return address_component['long_name'].encode('utf-8')

        return None

    def _search_geometry_location(self, type_):
        """Method searches geometry location in google maps json data"""
        if not self.json_data:
            return None

        geometry_location = self.json_data['geometry']['location']

        return geometry_location[type_]

    def get_formatted_address(self):
        """Method should return full address of current location."""
        if not self.json_data:
            return None

        return self.json_data['formatted_address']

    def get_street_number(self):
        """Method should returns street number of current location."""
        return self._search_address_components('street_number')

    def get_route(self):
        """Method should returns route long name of current location."""
        return self._search_address_components('route')

    def get_postal_code(self):
        """Method should returns postal code of current location."""
        return self._search_address_components('postal_code')

    def get_city(self):
        """Method should returns city long name of current location."""
        return self._search_address_components('locality')

    def get_country(self):
        """Method should returns country long name from current location."""
        return self._search_address_components('country')

    def get_country_shortcut(self):
        """Method should returns country short name from current location."""
        return self._search_address_components('country', True)

    def get_lat(self):
        """Method should returns lat property of current location."""
        return self._search_geometry_location('lat')

    def get_lng(self):
        """Method should returns lng property of current location."""
        return self._search_geometry_location('lng')

    def get_administrative_area(self):
        """Method should returns all administrative areas of current location."""
        data = list()

        administrative_areas = [
            'administrative_area_level_1', 'administrative_area_level_2', 'administrative_area_level_3'
        ]

        for area_type in administrative_areas:
            name = self._search_address_components(area_type)

            if name:
                data.append(dict(name=name, area_type=area_type))

        return data
