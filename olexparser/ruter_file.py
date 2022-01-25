import re

import gpxpy

from olexparser.rute import Rute
from olexparser import convert


class RuterFile:
    """A class representing a Ruter file.

    A ruter file consists of a number of Rutes (Routes).
    See :class:`olexparser.rute.Rute` for a description of a Rute.

    The Ruter file is a text file. The first line of the file will be  "Ferdig forenklet" ("Completely simplified").
    This line may also appear elsewhere in the file.

    :param file: the full file path of the Ruter file
    :type file: str
    :var self.full_path: The full path of the Ruter file
    :var self.rutes: A list of :class:`Rutes<olexparser.rute.Rute>` found in the Ruter file
    :var self.warnings: A list of warnings generated by the RuterFile class

    .. todo:: more Ruter file research. # of rutes between ferdig? ais? saving trips as rutes?
    """

    def __init__(self, file):
        """ A constructor method

        :param file: the full file path of the Ruter file
        :type file: str
        """
        self.full_path = file
        self.rutes = []
        self.warnings = []

        self.find_rutes()
        return

    def __str__(self):
        """
        :returns: A string describing the contents of the RuterFile
        :rtype: str
        """

        s = "\nRuter file path: {}".format(self.full_path)
        s = s + "\nRutes:"
        if len(self.rutes) > 0:
            for i in self.rutes:
                s = s + i.__str__()
        else:
            s = s + "\nNo rutes found in this Ruter file."
        return s

    def print_ruter(self):
        """
        Prints a description of the contents of the RuterFile
        """
        print("**********")
        print("Ruter file path: {}".format(self.full_path))
        print("Rutes:")
        if len(self.rutes) > 0:
            for i in self.rutes:
                i.print_rute()
        else:
            print("No rutes found in this Ruter file.")
        print("**********")
        return

    def check_header(self):
        """Internal method to check if the file is a valid Ruter file

        :return: True is valid, false otherwise
        :rtype: bool
        """
        with open(self.full_path, 'r') as data:
            header = data.readline()
        if header != "Ferdig forenklet\n":
            return False
        else:
            return True

    def find_rutes(self):
        """Internal method to parse the Ruter file and identify individual Rutes based on a regular expression.

        Identified Rutes are stored in a list.
        """
        if self.check_header():
            rute_re = r'Rute.*?\n\n'
            try:
                with open(self.full_path, 'r') as data:
                    ruter_file_data = data.read()
                rute_matches = re.findall(rute_re, ruter_file_data, re.DOTALL)

                for rute in rute_matches:
                    self.rutes.append(Rute(rute))
            except Exception as error:
                self.warnings.append(error)
        else:
            warn = "Warning, Ruter file does not have proper header: {}".format(self.full_path)
            self.warnings.append(warn)
        return

    def get_full_path(self):
        """
        :return: The full path of the Ruter File
        :rtype: str
        """
        return self.full_path

    def get_rutes(self):
        """
        :return: A list of Rutes identified in the RuterFile
        :rtype: list
        """
        return self.rutes.copy()

    def get_warnings(self):
        """
        :return: A list of warnings generated by the RuterFile, and it's child objects
        :rtype: list
        """
        warn = self.warnings.copy()
        for rute in self.rutes:
            warn.extend(rute.get_warnings())
        return warn

    def to_gpx(self):
        """
        .. todo: test RuterFile.to_gpx

        :return The data from the :class:`RuterFile` as a gpxpy.gpx.GPX object.
        :rtype: :class:`gpxpy.gpx.GPX`
        """
        gpx = gpxpy.gpx.GPX()

        for rute in self.rutes:
            route = gpxpy.gpx.GPXRoute()
            route.name = rute.get_rute_name()
            route.comment = rute.get_notes()
            route.type = rute.get_rute_type()
            desc = 'Plottsett: {} (Olex Layer {}). Rute Color: {}'.format(rute.get_plottsett(), rute.get_layer(),
                                                                          rute.get_rute_color())
            route.description = desc

            for point in rute.get_rute_entries():
                lat = convert.get_lat_or_long_dd(point.get_lat_float())
                long = convert.get_lat_or_long_dd(point.get_long_float)
                timestamp = convert.get_timestamp_str_from_int(point.get_timestamp_int())
                icon_str = point.get_icon_str()
                route.points.append(gpxpy.gpx.GPXRoutePoint(latitude=lat, longitude=long,
                                                            time=timestamp, symbol=icon_str))
            gpx.routes.append(route)
        return gpx
