import re
import math

from olexparser.rute_entry import RuteEntry


class Rute:
    """A class used to represent a Rute found in the :class:`Olex Ruter file<olexparser.ruter_file.RuterFile>`

    :param rute: a string containing a Rute from the Ruter file
    :type rute: str

    .. note::
        The plottsett value of 65 seems to break the power of 2 relationship
        between the plottsett number and layer.
        Casting all numbers as int seems to give the correct values and maintains the relationship.
        No special case for plottsett 65 (layer G) is required.

    .. todo:: check for more possible rute options
    """
    def __init__(self, rute):
        """A constructor method for the Rute class

        :param rute: a string containing a Rute from the Ruter file
        :type rute: str
        """
        plot_layer_names = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                            "A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1", "J1",
                            "A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2", "J2",
                            "A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", "I3", "J3",
                            "A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4", "I4", "J4",
                            "A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5", "J5")

        # Rute Name; Rute type; Line Color; Plot Layer; Positions
        plot_layer_re = r'Plottsett (\d*)'  # Plottsett
        rute_type_re = r'Rutetype (.*)'  # Rutetype
        line_color_re = r'Linjefarge (.*)'  # Linjefarge
        rute_name_re = r'Rute (.*)'  # Rute name
        rute_entry_re = r'([-\d.]+) ([-\d.]+) (\d+) (.+)'  # Rute Data points

        self.rute_entries = []
        self.plottsett = ""
        self.layer = ""
        self.rute_type = ""
        self.rute_color = ""
        self.rute_name = ""
        self.notes_text = ""

        self.warnings = []

        layer_matches = re.findall(plot_layer_re, rute)
        if len(layer_matches) == 1:
            layer_number = int(layer_matches[0])
            self.plottsett = layer_number
            self.layer = plot_layer_names[int(math.log(layer_number, 2))]
        else:
            warn = "Warning, only 1 Layer should be present in a Rute"
            self.warnings.append(warn)

        type_matches = re.findall(rute_type_re, rute)
        if len(type_matches) == 1:
            self.rute_type = type_matches[0]
        else:
            warn = "Warning, only 1 Rute Type should be present in a Rute"
            self.warnings.append(warn)

        color_matches = re.findall(line_color_re, rute)
        if len(color_matches) == 1:
            self.rute_color = color_matches[0]
        else:
            warn = "Warning, only 1 Color Type should be present in a Rute"
            self.warnings.append(warn)

        name_matches = re.findall(rute_name_re, rute)
        if len(name_matches) == 1:
            self.rute_name = name_matches[0]
        else:
            warn = "Warning, only 1 Rute Name should be present in a Rute"
            self.warnings.append(warn)

        rute_entry_matches = re.findall(rute_entry_re, rute)
        for i in rute_entry_matches:
            self.rute_entries.append(RuteEntry(i[0], i[1], i[2], i[3]))

        # Hacky work around to find the notes, a proper RE would be preferred
        # Strips whitespace and checks if last line is a rute entry
        # If not it assumes it is a note
        notes = rute.split("\n")
        while "" in notes:
            notes.remove("")
        if re.match(rute_entry_re, notes[-1]) is None:
            self.notes_text = notes[-1]

    def print_rute(self):
        """Prints a description of the contents of the Rute
        """
        print()
        if self.rute_name != "":
            print("Rute Name: {}".format(self.rute_name))
        if self.rute_type != "":
            print("Rute Type: {}".format(self.rute_type))
        if self.rute_color != "":
            print("Line Color: {}".format(self.rute_color))
        if self.layer != "":
            print("Rute Layer: {} (Converted from Plottsett: {})".format(self.layer, self.plottsett))
        if len(self.rute_entries) > 0:
            print("Rute Entries:")
            print("**")
            for i in self.rute_entries:
                i.print_rute_entry()
                print("**")
        if self.notes_text != "":
            print("Rute Notes: {}".format(self.notes_text))

        print()
        return

    def get_rute_entries(self):
        """Returns the list of identified RuteEntry objects

        :return: the list of identified RuteEntry objects
        :rtype: list
        """
        return self.rute_entries

    def get_plottsett(self):
        """
        :return: the plottsett (Plot Layer) number
        :rtype: int
        """
        return self.plottsett

    def get_layer(self):
        """
        :return: The Layer the Rute uses within Olex.
        :rtype: str
        """
        return self.layer

    def get_rute_type(self):
        """
        :return: The Rute type
        :rtype: str
        """
        return self.rute_type

    def get_rute_color(self):
        """
        :return: The color (in Norwegian) of the Rute when it is displayed in Olex
        :rtype: str
        """
        return self.rute_color

    def get_rute_name(self):
        """
        :return: The Rute name
        :rtype: str
        """
        return self.rute_name

    def get_notes(self):
        """
        :return: Any notes present
        :rtype: str
        """
        return self.notes_text

    def get_warnings(self):
        """
        :return: a list of warnings generated by the Rute
        :rtype: list
        """
        return self.warnings
