import re

import gpxpy

from olexparser import convert
from olexparser.turtur_segment_summary import TurTurSegmentSummary
from olexparser.turtur import TurTur


class TurDataFile:
    """
    A Class used to represent a Turdata file.

    The Turdata file consists of a collection of Tur Turs (Trips).

    See :class:`TurTur<olexparser.turtur.TurTur>` for a description of a Tur Tur.

    :param full_path: The full path and filename for the Turdata file
    :type full_path: str
    """

    def __init__(self, full_path):
        """A constructor method for the TurDataFile

        :param full_path: the full path and filename for the Turdata file
        :type full_path: str
        """

        self.full_path = full_path
        self.tur_turs = {}

        self.warnings = []

        # Parse the Turdata file
        self.read_tur_data_file()
        return

    def get_full_path(self):
        """Returns the full path of the TurData file

        :return: the full path of the TurData file
        :rtype: str
        """
        return self.full_path

    def get_tur_numbers(self):
        """Returns the keys from the dictionary of Tur Turs

        :return: the keys from the dictionary of Tur Turs
        :rtype: dict_keys
        """
        return self.tur_turs.keys()

    def read_tur_data_file(self):
        """Reads the Turdata file and identifies individual Tur Turs (Trips).

        The entire file is read and regular expressions are used to identify Tur Turs in the file.
        A TurTur object is created for each Tur Tur. It contains the Tur Tur number and a list of segment summaries.
        The TurTur object added to the dict tur_turs with it's Tur Tur number as the key.
        """

        # Regular expressions used to identify process Tur Turs
        tur_tur_re = r'Tur Tur[^T]*'
        tur_num_re = r'Tur Tur \d*'
        tur_segment_summary_re = r'Segment (\d*) (\d*) ([-\d.]*) ([-\d.]*) ([-\d.]*) ([-\d.]*) (\d*) (\d*)'

        # Read the Turdata file
        try:
            with open(self.full_path, 'r') as f:
                tur_file = f.read()
        except Exception as error:
            self.warnings.append(error)
            return

        # Find all Tur Turs
        tur_matches = re.findall(tur_tur_re, tur_file, re.DOTALL)

        # Create a TurTur object for each identified Tur Tur
        for i in tur_matches:

            # Determine the Tur Tur Number
            tur_num = int(re.match(tur_num_re, i).group().strip("Tur Tur "))

            # Identify all the Segments in the Tur Tur
            segment_summaries = re.findall(tur_segment_summary_re, i)

            # Create a TurTurSegmentSummary for each identified segment summary
            tur_segment_summaries = {}
            for summary in segment_summaries:
                seg_num = int(summary[0])
                num_entries = int(summary[1])
                smallest_lat = float(summary[2])
                smallest_long = float(summary[3])
                largest_lat = float(summary[4])
                largest_long = float(summary[5])
                smallest_time = int(summary[6])
                largest_time = int(summary[7])

                tur_segment_summaries[seg_num] = TurTurSegmentSummary(seg_num, num_entries, smallest_lat, smallest_long,
                                                                      largest_lat, largest_long, smallest_time,
                                                                      largest_time)

            # add the TurTur to the tur_turs dict
            self.tur_turs[tur_num] = TurTur(tur_num, tur_segment_summaries)

        return

    def get_turtur(self, number):
        """Returns the TurTur object identified by the Tur Tur number

        :param number: The Tur Tur number to retrieve.
        :type number: int
        :return: the TurTur object identified by the Tur Tur number.
        :rtype: olexparser.turtur.TurTur
        """

        return self.tur_turs[number]

    def __str__(self):
        """String representation of the TurData file class
        :return: String representation of the TurData file class
        :rtype: str

        """

        s = "\nTurdata filepath: {}".format(self.full_path)

        if len(self.tur_turs.keys()) > 0:
            for i in self.tur_turs.keys():
                s = s + self.tur_turs[i].__str__()
        else:
            s = s + "\nNo Tur Turs found in the this Turdata file."
        return s

    def print_turdata(self):
        """Prints a description of the contents of the TurDataFile"""
        print()
        print("**********")
        print("Turdata filepath: {}".format(self.full_path))
        if len(self.tur_turs.keys()) > 0:
            for i in self.tur_turs.keys():
                self.tur_turs[i].print_turtur()
        else:
            print("No Tur Turs found in the this Turdata file.")
        print("**********")
        print()
        return

    def get_warnings(self):
        """
        :return: a list of warnings generated by the TurDataFile, and it's child objects
        :rtype: list
        """
        warn = self.warnings.copy()
        for turtur in self.tur_turs.values():
            warn.extend(turtur.get_warnings())
        return warn

    def to_gpx(self):
        """
        :return: The data from the :class:`TurDataFile` as a gpxpy.gpx.GPX object
        :rtype: :class:`gpxpy.gpx.GPX`
        """
        gpx = gpxpy.gpx.GPX()
        for tur_tur_number in self.get_tur_numbers():
            tur_tur = self.get_turtur(tur_tur_number)

            trip = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(trip)

            trip.name = "Tur Tur {}".format(tur_tur_number)
            gpx_track_segment = gpxpy.gpx.GPXTrackSegment()
            trip.segments.append(gpx_track_segment)
            segments_summaries = tur_tur.get_segment_summaries()
            for summary in segments_summaries:
                start_lat = convert.get_lat_or_long_dd(summary.get_lat_start_float())
                start_long = convert.get_lat_or_long_dd(summary.get_long_start_float())
                start_time = convert.get_timestamp_str_from_int(summary.get_time_start_int())
                start_comment = "Segment {} start values".format(summary.get_seg_num())
                start_point = gpxpy.gpx.GPXTrackPoint(start_lat, start_long, time=start_time, comment=start_comment)

                stop_lat = convert.get_lat_or_long_dd(summary.get_lat_end_float())
                stop_long = convert.get_lat_or_long_dd(summary.get_long_end_float())
                stop_time = convert.get_timestamp_str_from_int(summary.get_time_end_int())
                stop_comment = "Segment {} stop values".format(summary.get_seg_num())
                stop_point = gpxpy.gpx.GPXTrackPoint(stop_lat, stop_long, time=stop_time, comment=stop_comment)

                gpx_track_segment.points.append(start_point)
                gpx_track_segment.points.append(stop_point)
        return gpx
