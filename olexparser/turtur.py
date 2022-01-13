from olexparser.segment_file import SegmentFile


class TurTur:
    """
    A Class used to represent a Tur Tur (trip) from the Turdata file.

    Each Tur Tur consists of a Tur Tur number, as well as summaries of the segment files associated to the Tur Tur.

    An example of a Tur Tur from a Turdata file is as follows

        Tur Tur 42

        Segment 197 1818 2986.74 -3246.82 3100.01 -3235.69 1417854557 1417862055

    See :class:`TurTurSegmentSummary<olexparser.turtur_segment_summary.TurTurSegmentSummary>`
    for a description of a segment summary.

    :param tur_num: the Tur Tur number as listed in the Turdata file
    :type tur_num: int
    :param tur_segment_summaries: A list of TurTurSegmentSummaries.
    :type tur_segment_summaries: list

    .. todo:: check that min/max values in summary match min/max in segment file
    """
    def __init__(self, tur_num, tur_segment_summaries):
        """A constructor method for TurTur

        :param tur_num: the Tur Tur number, as listed in the Turdata file
        :type tur_num: int
        :param tur_segment_summaries: A dict of TurTurSegmentSummaries with
                                      key:value == Segment Number:TurTurSegmentSummary.
        :type tur_segment_summaries: dict
        """

        self.tur_num = tur_num
        self.segments_summaries = tur_segment_summaries
        self.segments = {}

        self.warnings = []

        # self.parse_segment_files()
        # self.check_sample_sizes()
        return

    def check_min_max_all(self):
        """
        Checks the min and max values for the latitude, longitude, and time in all the :class:`TurTurSegmentSummary`
        objects against their :class:`SegmentFile`.

        :return: True if all min/max values in Segments match those given in their summary; False otherwise
        :rtype: bool
        """
        same = True
        for seg_num in self.segments_summaries.keys():
            if not self.check_min_max(seg_num):
                # warnings handled in self.check_min_max()
                same = False
        return same

    def check_min_max(self, seg_num):
        """
        .. todo:: check that min/max values in summary match min/max in segment file

        Checks the min and max values for the latitude, longitude, and time in the :class:`TurTurSegmentSummary`
        against the :class:`SegmentFile`.

        :return: True if all min/max values in Segment match those given in the summary; False otherwise
        :rtype: bool
        """
        same = True

        # check if the segment file is associated to the TurTur
        if seg_num in self.segments.keys():

            # get the TurTurSegmentSummary
            seg_sum = self.segments_summaries[seg_num]

            # get the values from the TurTurSegmentSummary
            sum_lat_small = seg_sum.get_lat_small_float()
            sum_long_small = seg_sum.get_long_small_float()
            sum_lat_large = seg_sum.get_lat_large_float()
            sum_long_large = seg_sum.get_long_large_float()
            sum_time_start = seg_sum.get_time_start_int()
            sum_time_end = seg_sum.get_time_end_int()

            seg_entries = self.segments[seg_num].get_seg_entries()

            # convert to list so we can use subscripting
            values_list = list(seg_entries.values())

            # set initial values
            first_value = values_list[0]
            largest_lat = first_value.get_lat_float()
            smallest_lat = first_value.get_lat_float()
            largest_long = first_value.get_long_float()
            smallest_long = first_value.get_long_float()
            largest_time = first_value.get_timestamp_int()
            smallest_time = first_value.get_timestamp_int()

            # get min/max values in segment
            for entry in values_list[1:]:
                if entry.get_lat_float() > largest_lat:
                    largest_lat = entry.get_lat_float()
                if entry.get_lat_float() < smallest_lat:
                    smallest_lat = entry.get_lat_float()
                if entry.get_long_float() > largest_long:
                    largest_long = entry.get_long_float()
                if entry.get_long_float() < smallest_long:
                    smallest_long = entry.get_long_float()
                if entry.get_timestamp_int() > largest_time:
                    largest_time = entry.get_timestamp_int()
                if entry.get_timestamp_int < smallest_time:
                    smallest_time = entry.get_timestamp_int()

            if smallest_lat != sum_lat_small:
                warn = "Warning, TurTur {} Segment {}: the summary has the smallest latitude value as {}, the " \
                       "actual smallest value is {}".format(self.tur_num, seg_num, sum_lat_small, smallest_lat)
                self.warnings.append(warn)
                same = False

            if smallest_long != sum_long_small:
                warn = "Warning, TurTur {} Segment {}: the summary has the smallest longitude value as {}, the " \
                       "actual smallest value is {}".format(self.tur_num, seg_num, sum_long_small, smallest_long)
                self.warnings.append(warn)
                same = False

            if largest_lat != sum_lat_large:
                warn = "Warning, TurTur {} Segment {}: the summary has the largest latitude value as {}, the " \
                       "actual largest value is {}".format(self.tur_num, seg_num, sum_lat_large, largest_lat)
                self.warnings.append(warn)
                same = False

            if largest_long != sum_long_large:
                warn = "Warning, TurTur {} Segment {}: the summary has the largest longitude value as {}, the " \
                       "actual longitude value is {}".format(self.tur_num, seg_num, sum_long_large, largest_long)
                self.warnings.append(warn)
                same = False

            if largest_time != sum_time_end:
                warn = "Warning, TurTur {} Segment {}: the summary has the largest time value as {}, the " \
                       "actual largest time is {}".format(self.tur_num, seg_num, sum_time_end, largest_time)
                self.warnings.append(warn)
                same = False

            if smallest_time != sum_time_start:
                warn = "Warning, TurTur {} Segment {}: the summary has the smallest time value as {}, the " \
                       "actual smallest time is {}".format(self.tur_num, seg_num, sum_time_start, smallest_time)
                self.warnings.append(warn)
                same = False

        else:
            warn = "Warning, Segment {} not associated with TurTur {}. Either the file does not exist or it wasn't " \
                   "added to the TurTur object.".format(seg_num, self.tur_num)
            self.warnings.append(warn)
            same = False

        return same

    def add_segment(self, seg_num, segment):
        """
        Adds :class:`SegmentFile<olexparser.segment_file.SegmentFile>` to the TurTur.

        Generates a warning if a SegmentFile with seg_num is already associated to the TurTur.

        :param seg_num: A number identifying the related Segment filename. i.e. if the segment number is 83 the
                        filename will be "segment83_A".
        :type seg_num: int
        :param segment: a :class:`SegmentFile<olexparser.segment_file.SegmentFile>`
        :type segment: SegmentFile
        """
        if seg_num in self.segments.keys():
            warn = "Warning, Segment {} already associated to Tur Tur {}".format(seg_num, self.tur_num)
            self.warnings.append(warn)
        else:
            self.segments[seg_num] = segment
        return

    def check_sample_sizes(self):
        """
        A method for checking if given size of the segment files in summaries is the same as the actual size on disk.

        Adds a warning if different.
        """
        for seg_num in self.segments_summaries.keys():
            if not self.check_sample_size(seg_num):
                warn = "Warning, expected size of Segment {} differs from actual size".format(seg_num)
                self.warnings.append(warn)

        return

    def check_sample_size(self, seg_num):
        """
        Checks the expected size of the :class:`SegmentFile`, based on the :class:`TurTurSegmentSummary`, against the
        actual size of the :class:`SegmentFile` on disk.
        :param seg_num: the Segment Number to check
        :type seg_num: int
        :return: True if expected and actual sizes are the same, False otherwise
        :rtype: bool
        """
        expected_size = self.segments_summaries[seg_num].get_entries_num() * 16
        actual_size = self.segments[seg_num].get_size()
        if actual_size != expected_size:
            return False
        return True

    def get_segment_numbers(self):
        """
        :return: The segment numbers of every :class:`SegmentFile<olexparser.segment_file.SegmentFile>` associated
                 to the TurTur
        :rtype: list
        """
        return self.segments.keys()

    def get_segment(self, seg_num):
        """
        :param seg_num: The segment number of the :class:`SegmentFile<olexparser.segment_file.SegmentFile>`
        :return: The :class:`SegmentFile<olexparser.segment_file.SegmentFile>` with the provided segment number.
                 Returns None if no SegmentFile with seg_number is associated to the TurTur
        :rtype: SegmentFile, None
        """
        if seg_num in self.segments.keys():
            return self.segments[seg_num]
        else:
            return None

    def get_tur_num(self):
        """ Returns the Tur Tur Number

        :return: the Tur Tur Number
        :rtype: int
        """

        return self.tur_num

    def get_segment_summaries(self):
        """ Returns a list of Segment Summaries

            :return: a list of TurTurSegmentSummary objects representing each segment summary identified in the Tur Tur.
            :rtype: list
            """

        return self.segments_summaries.copy()

    def print_turtur(self):
        """Prints a description of the contents of the TurTur

        """
        print("*****")
        print("Tur Tur Number: {}".format(self.tur_num))
        if len(self.segments_summaries) > 0:
            for i in self.segments_summaries:
                i.print_segment_summary()
        else:
            print("No Segment Summaries found for this Tur Tur.")
        print("*****")
        return

    def __str__(self):
        """A description of the contents of the TurTur

        :return A description of the contents of the TurTur
        :rtype: str
        """

        s = "\nTur Tur Number: {}".format(self.tur_num)
        if len(self.segments_summaries) > 0:
            for i in self.segments_summaries:
                s = s + i.__str__()
        else:
            s = s + "\nNo Segment Summaries found for this Tur Tur."
        return s

    def get_warnings(self):
        """
        :return: a list of warnings generated by the TurTur, and it's child objects
        :rtype: list
        """
        warn = self.warnings.copy()
        for seg_sum in self.segments_summaries:
            warn.extend(seg_sum.get_warnings())
        for seg in self.segments.values():
            warn.extend(seg.get_warnings())
        return warn
