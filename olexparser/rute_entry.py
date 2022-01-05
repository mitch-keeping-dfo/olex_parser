import olexparser.convert as convert


class RuteEntry:
    """
    A class used to represent a Rute Entry from the :class:`Olex Ruter file<olexparser.ruter_file.RuterFile>`

    Each entry represents a point on the map for it's parent :class:`Rute<olexparser.rute.Rute>`

    Each entry consists of:
        - a latitude coordinate
        - a longitude coordinate
        - a unix timestamp
        - a text descriptor of the icon for the entry

    :param lat: the "Olex float" of a latitude coordinate
    :type lat: float
    :param long: the "Olex float" of a longitude coordinate
    :type long: float
    :param timestamp: a Unix timestamp
    :type timestamp: int
    :param icon: a string describing the icon used for the entry
    :type icon: str
    """

    def __init__(self, lat, long, timestamp, icon):
        """A constructor for the RuteEntry class

        :param lat: the "Olex float" of a latitude coordinate
        :type lat: float
        :param long: the "Olex float" of a longitude coordinate
        :type long: float
        :param timestamp: a Unix timestamp
        :type timestamp: int
        :param icon: a string describing the icon used for the entry
        :type icon: str
        """
        self.lat = float(lat)
        self.long = float(long)
        self.timestamp = int(timestamp)
        self.icon = str(icon)

    def __str__(self):
        """A descriptive string representation of the Rute class
        :return: String representation of the Rute class
        :rtype: str
        """
        s = "\nRute Entry Latitude float: {} Latitude coordinate: {}".format(
            self.lat, convert.get_lat_dmm(self.lat))
        s = s + "\nRute Entry Longitude float: {} Longitude coordinate: {}".format(
            self.long, convert.get_lat_dmm(self.long))
        s = s + "\nRute Entry Unix Timestamp: {} Timestamp converted to UTC: {}".format(
            self.timestamp, convert.get_timestamp_str_from_int(self.timestamp))
        s = s + "\nRute Entry Icon: {}".format(self.icon)
        return s

    def print_rute_entry(self):
        """Prints a description of the RuteEntry contents.
        """
        print("Rute Entry Latitude float: {} Latitude coordinate: {}".format(
            self.lat, convert.get_lat_dmm(self.lat)))
        print("Rute Entry Longitude float: {} Longitude coordinate: {}".format(
            self.long, convert.get_lat_dmm(self.long)))
        print("Rute Entry Unix Timestamp: {} Timestamp converted to UTC: {}".format(
            self.timestamp, convert.get_timestamp_str_from_int(self.timestamp)))
        print("Rute Entry Icon: {}".format(self.icon))
        return

    def get_lat_float(self):
        """
        :return: the 'Olex float' representing the latitude coordinate
        :rtype: float
        """
        return self.lat

    def get_long_float(self):
        """
        :return: the 'Olex float' representing the longitude coordinate
        :rtype: float
        """
        return self.long

    def get_timestamp_int(self):
        """
        :return: the Unix timestamp
        :rtype: int
        """
        return self.timestamp

    def get_icon_str(self):
        """
        :return: the string describing the icon
        :rtype: str
        """
        return self.icon
