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

        :param tur_num: the Tur Tur number as listed in the Turdata file
        :type tur_num: int
        :param tur_segment_summaries: A list of TurTurSegmentSummaries.
        :type tur_segment_summaries: list
        """

        self.tur_num = tur_num
        self.segments_summaries = tur_segment_summaries
        self.segments = {}

        self.warnings = []

        # self.parse_segment_files()
        # self.check_sample_sizes()
        return

    def add_segment(self, seg_num, segment):
        """
        Adds :class:`SegmentFile<olexparser.segment_file.SegmentFile>` to the TurTur.

        Generates a warning if a SegmentFile with seg_num is already associated to the TurTur.

        :param seg_num: A number identifying the related Segment filename. ie. if the segment number is 83 the
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
        A method for checking if given size of the segment file in summary is the same as the actual size on disk.

        Adds a warning if different.
        """
        for summary in self.segments_summaries:
            seg_num = summary.get_seg_num()
            segment = self.segments[seg_num]
            expected_size = summary.get_entries_num() * 16
            actual_size = segment.get_size()
            if segment.get_size() != expected_size:
                warn = "Warning, Tur Tur expects Segment {} to have file size {}, actual size is {}".format(
                    seg_num, expected_size, actual_size)
                self.warnings.append(warn)
        return

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
        :return: a list of warnings generated by the TurTur and it's child objects
        :rtype: list
        """
        warn = self.warnings.copy()
        for seg_sum in self.segments_summaries:
            warn.extend(seg_sum.get_warnings())
        for seg in self.segments.values():
            warn.extend(seg.get_warnings())
        return warn
