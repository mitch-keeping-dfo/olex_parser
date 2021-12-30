import re
from olexparser.rute import Rute


class RuterFile:
    """A class representing a Ruter file.

    A ruter file consists of a number of Rutes (Routes).
    See :class:`olexparser.rute.Rute` for a description of a Rute.

    The Ruter file is a text file. The first line of the file will be  "Ferdig forenklet" ("Completely simplified").
    This line may also appear elsewhere in the file.

    :param file: the full file path of the Ruter file
    :type file: str

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

        if self.check_header():
            self.find_rutes()
        else:
            warn = "Warning, Ruter file does not have proper header: {}".format(self.full_path)
            self.warnings.append(warn)
        return

    def __str__(self):
        """
        :returns: A string describing the contents of the RuterFile
        :rtype: str
        """
        s = "\n**********"
        s = s + "\nRuter file path: {}".format(self.full_path)
        s = s + "\nRutes:"
        if len(self.rutes) > 0:
            for i in self.rutes:
                s = s + "\n" + str(i)
        else:
            s = s + "\nNo rutes found in this Ruter file."
        s = s + "\n**********"
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
        header = open(self.full_path, 'r').readline()
        if header != "Ferdig forenklet\n":
            return False
        else:
            return True

    def find_rutes(self):
        """Internal method to parse the Ruter file and identify individual Rutes based on a regular expression.

        Identified Rutes are stored in a list.
        """
        rute_re = r'Rute.*?\n\n'
        ruter_file_data = open(self.full_path, 'r').read()
        rute_matches = re.findall(rute_re, ruter_file_data, re.DOTALL)

        for rute in rute_matches:
            self.rutes.append(Rute(rute))
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
        return self.rutes

    def get_warnings(self):
        """
        :return: A list of warnings generated while processing the RuterFile
        :rtype: list
        """
        return self.warnings

