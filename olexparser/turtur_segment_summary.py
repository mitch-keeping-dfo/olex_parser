import olexparser.convert as convert


class TurTurSegmentSummary:
    """
    A Class representing a Tur Tur Segment Summary.

    Each Tur Tur in the Turdata file lists 1 or more segment files associated to it.
    A summary of the segment file is also stored in the Turdata file.

    .. note::
       These summaries may contain the only remaining data as the actual segment file may be empty.

       Further analysis is needed to determine how a segment file becomes empty (0 bytes).

    Each Segment Summary contains the following:

        1. The segment number.
        2. The number of 16 byte entries in the segment file.
        3. The smallest latitude value found in the file.
        4. The smallest longitude value found in the file.
        5. The largest latitude value found in the file.
        6. The largest longitude value found in the file.
        7. The smallest unix timestamp value found in the file.
        8. The largest unix timestamp value found in the file.

    :param seg_num: A number identifying the related Segment filename. ie. if the segment number is 83 the filename
                    will be "segment83_A".
    :type seg_num: int
    :param num_entries: The number of entries in the segment file. Each entry is 16 bytes in length. This number
                        can be used to determine the expected file size of the segment.
    :type num_entries: int
    :param smallest_lat: An "Olex float" containing the smallest Latitude position in the segment file.
    :type smallest_lat: float
    :param smallest_long: An "Olex float" containing the smallest Latitude position in the segment file.
    :type smallest_long: float
    :param largest_lat:  An "Olex float" containing the largest Latitude position in the segment file.
    :type largest_lat: float
    :param largest_long: An "Olex float" containing the largest Longitude position in the segment file.
    :type largest_long: float
    :param smallest_time: A Unix Timestamp of the first entry in the segment file.
    :type smallest_time: int
    :param largest_time: A Unix Timestamp of the last entry in the segment file.
    :type largest_time: int

    .. todo:: Determine how a segment file becomes 0 bytes
    """

    def __init__(self, seg_num, num_entries, smallest_lat, smallest_long, largest_lat, largest_long, smallest_time,
                 largest_time):
        """A constructor method for the TurTurSegmentSummary.

        :param seg_num: A number identifying the related Segment filename. ie. if the segment number is 83 the
                        filename will be "segment83_A".
        :type seg_num: int
        :param num_entries: The number of entries in the segment file. Each entry is 16 bytes in length. This number
                            can be used to determine the expected file size of the segment.
        :type num_entries: int
        :param smallest_lat: An "Olex float" containing the smallest Latitude position in the segment file.
        :type smallest_lat: float
        :param smallest_long: An "Olex float" containing the smallest Latitude position in the segment file.
        :type smallest_long: float
        :param largest_lat:  An "Olex float" containing the largest Latitude position in the segment file.
        :type largest_lat: float
        :param largest_long: An "Olex float" containing the largest Longitude position in the segment file.
        :type largest_long: float
        :param smallest_time: A Unix Timestamp of the first entry in the segment file.
        :type smallest_time: int
        :param largest_time: A Unix Timestamp of the last entry in the segment file.
        :type largest_time: int
        """
        self.warnings = []

        self.seg_num = seg_num
        self.num_entries = num_entries
        self.smallest_lat = smallest_lat
        self.smallest_long = smallest_long
        self.largest_lat = largest_lat
        self.largest_long = largest_long
        self.smallest_time = smallest_time
        self.largest_time = largest_time

        return

    def __str__(self):
        """A description of the contents of the TurTurSegmentSummary.

        :return: A description of the contents of the TurTurSegmentSummary
        :rtype: str
        """

        s = "\nSegment number: {}".format(self.seg_num)
        s = s + "\nNumber of entries in the segment file: {}".format(self.num_entries)
        s = s + "\nSmallest Latitude float: {}  Starting Latitude coordinate: {}".format(
            self.smallest_lat, convert.get_lat_dmm(self.smallest_lat))
        s = s + "\nSmallest Longitude float: {}  Starting Longitude coordinate: {}".format(
            self.smallest_long, convert.get_long_dmm(self.smallest_long))
        s = s + "\nLargest Latitude float: {}  End Latitude coordinate: {}".format(
            self.largest_lat, convert.get_lat_dmm(self.largest_lat))
        s = s + "\nLargest Longitude float: {}  End Longitude coordinate: {}".format(
            self.largest_long, convert.get_long_dmm(self.largest_long))
        s = s + "\nSmallest Unix Timestamp: {} Starting time UTC: {}".format(
            self.smallest_time, convert.get_timestamp_str_from_int(self.smallest_time))
        s = s + "\nLargest Unix Timestamp: {} End time UTC: {}".format(
            self.largest_time, convert.get_timestamp_str_from_int(self.largest_time))
        return s

    def get_warnings(self):
        """
        :return: a list of warnings generated by the TurTurSegmentSummary
        :rtype: list
        """
        return self.warnings.copy()

    def print_segment_summary(self):
        """Prints a description of the contents of the TurTurSegmentSummary.
        """
        print()
        print("Segment number: {}".format(self.seg_num))
        print("Number of entries in the segment file: {}".format(self.num_entries))
        print("Smallest Latitude float: {}  Starting Latitude coordinate: {}".format(
            self.smallest_lat, convert.get_lat_dmm(self.smallest_lat)))
        print("Smallest Longitude float: {}  Starting Longitude coordinate: {}".format(
            self.smallest_long, convert.get_long_dmm(self.smallest_long)))
        print("Largest Latitude float: {}  End Latitude coordinate: {}".format(
            self.largest_lat, convert.get_lat_dmm(self.largest_lat)))
        print("Largest Longitude float: {}  End Longitude coordinate: {}".format(
            self.largest_long, convert.get_long_dmm(self.largest_long)))
        print("Smallest Unix Timestamp: {} Starting time UTC: {}".format(
            self.smallest_time, convert.get_timestamp_str_from_int(self.smallest_time)))
        print("Largest Unix Timestamp: {} End time UTC: {}".format(
            self.largest_time, convert.get_timestamp_str_from_int(self.largest_time)))
        print()
        return

    def get_seg_num(self):
        """
        :return: the segment number
        :rtype: int
        """

        return self.seg_num

    def get_entries_num(self):
        """
        :return: the number of entries in the segment file
        :rtype: int
        """
        return self.num_entries

    def get_lat_start_float(self):
        """
        :return: the "OLEX" float representing smallest latitude value
        :rtype: float
        """
        return self.smallest_lat

    def get_long_start_float(self):
        """
        :return: the the "OLEX" float representing smallest longitude value
        :rtype: float
        """
        return self.smallest_long

    def get_lat_end_float(self):
        """
       :return: the the "OLEX" float representing largest latitude value
       :rtype: float
        """
        return self.largest_lat

    def get_long_end_float(self):
        """
        :return: the the "OLEX" float representing the largest longitude value
        :rtype: float
        """
        return self.largest_long

    def get_time_start_int(self):
        """
        :return: the Unix Timestamp integer representing the smallest time value.
        :rtype: int
        """
        return self.smallest_time

    def get_time_end_int(self):
        """
        :return: the Unix Timestamp integer representing the largest time value.
        :rtype: int
        """
        return self.largest_time
