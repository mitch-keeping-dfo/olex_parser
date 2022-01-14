import os
from olexparser.segment_entry import SegmentEntry


class SegmentFile:
    """
    A Class representing a Segment file.

    A Segment file consists of a number of 16 byte entries.
    See :class:`olexparser.segment_entry.SegmentEntry` for a description of a segment entry.

    :param file_path: the full file path of the Segment file
    :type file_path: str
    """

    def __init__(self, file_path):
        """A constructor method for the SegmentFile class.

        :param file_path: the full file path of the Segment file
        :type file_path: str
        """
        self.seg_num = 0
        self.seg_entries = {}
        self.full_path = file_path
        self.file_size = 0

        self.warnings = []

        # parse the segment file
        self.parse_segment_file()

        return

    def __str__(self):
        """A string which describes the contents of SegmentEntry

        :return: A string which describes the contents of SegmentEntry
        :rtype: str
        """

        s = "\nSegment filepath: {}".format(self.full_path)
        s = s + "\nSegment number: {}".format(self.seg_num)
        s = s + "\nSegment file size: {}".format(self.file_size)
        if len(self.seg_entries.keys()) > 0:
            for i in self.seg_entries.keys():
                s = s + "\nSegment Entry at offset {} contains:".format(i)
                s = s + self.seg_entries[i].__str__()
        else:
            s = s + "\nNo Segment entries found in this Segment."

        return s

    def get_warnings(self):
        """
        :return: a list of warnings generated by the SegmentFile, and it's child objects
        :rtype: list
        """
        warn = self.warnings.copy()
        for seg_sum in self.seg_entries.values():
            warn.extend(seg_sum.get_warnings())
        return warn

    def print_segment(self):
        """Prints the contents of the segment file"""
        print("**********")
        print("Segment filepath: {}".format(self.full_path))
        print("Segment number: {}".format(self.seg_num))
        print("Segment file size: {}".format(self.file_size))
        if len(self.seg_entries.keys()) > 0:
            for i in self.seg_entries.keys():
                print()
                print("Segment Entry at offset {} contains:".format(i))
                self.seg_entries[i].print_segment_entry()
        else:
            print("No Segment entries found in this Segment.")
        print("**********")
        return

    def parse_segment_file(self):
        """ Internal method which parses the segment file.

        parse_segment_file reads the segment file as a binary stream and creates a SegmentEntry object
        for each 16 byte line in the file. A warning is generated if the file is not divisible by 16,
        and the remaining bytes are ignored.

        See :class:`SegmentEntry<olexparser.segment_entry.SegmentEntry>` for a description of a segment entry.
        """

        if os.path.isfile(self.full_path):
            self.seg_num = int(os.path.basename(self.full_path).strip("_A").strip("segment"))
            self.file_size = os.path.getsize(self.full_path)

            try:
                with open(self.full_path, 'rb') as f:
                    data = f.read()
                size_diff = self.file_size % 16
                if size_diff != 0:
                    warn = "Warning, file size of Segment {} not divisible by 16. May not be valid Segment file or " \
                           "corrupt. The last {} bytes will not be parsed.".format(self.seg_num, size_diff)
                    self.warnings.append(warn)
                    data = data[:-size_diff]
                offset = 0
                while offset < len(data):
                    self.seg_entries[offset] = SegmentEntry(data[offset:offset+16])
                    offset += 16
            except Exception as e:
                self.warnings.append(e)
                pass

        else:
            warn = "Warning, Segment {0} is not a file".format(self.full_path)
            self.warnings.append(warn)
        return

    def get_size(self):
        """Returns the file size in bytes.

        :return: the size of the file (in bytes)
        :rtype: int
        """
        return self.file_size

    def get_seg_num(self):
        """Returns the segment number.

        :return: The segment number
        :rtype: int
        """
        return self.seg_num

    def get_seg_entries(self):
        """Returns the dictionary of SegmentEntry objects with key:value - file_offset:SegmentEntry

        :return: the dictionary of SegmentEntry objects with key:value - file_offset:SegmentEntry
        :rtype: dict
        """
        return self.seg_entries.copy()

    def get_full_path(self):
        """Returns the full file path for the segment file.

        :return: the full file path of the segment file.
        :rtype: str
        """
        return self.full_path

    def to_gpx(self):
        """
        .. todo: add gpx conversion to SegmentFile
        :return:
        """
        return