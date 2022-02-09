import os
import sys

from olexparser.turdata_file import TurDataFile
from olexparser.ruter_file import RuterFile
from olexparser.segment_file import SegmentFile

turdata_file = []
tur_data_files_parsed = []

segment_files = {}
segment_files_no_turtur = []

ruter_file = []
ruter_files_parsed = []

other_files = []

warnings = []

# .. todo: test startstopplogg file, appears to be start/stop times for olex running


def walk_folder(folder):
    """Parse a folder structure and identify OLEX files, including the Ruter file, the Turdata file,
    and segment files

    :param folder: Source folder for Olex files
    :type folder: str
    """
    for (dir_path, dir_names, file_names) in os.walk(folder):
        for filename in file_names:
            if filename == "Turdata":
                turdata_file.append(dir_path + "//" + filename)
            elif filename == "Ruter":
                ruter_file.append(dir_path + "//" + filename)
            elif filename.endswith("_A"):
                segment_files[filename.strip("segment").strip("_A")] = dir_path + "//" + filename
            else:
                other_files.append(dir_path + "//" + filename)
    return


def print_ruters():
    for i in ruter_files_parsed:
        i.print_ruter()
    return


def print_segments():
    for i in segment_files_no_turtur:
        i.print_segment()
    return


def print_turdatas():
    for i in tur_data_files_parsed:
        i.print_turdata()
    return


def print_other():
    if len(other_files) > 0:
        print("Other files found in the folder:")
        for i in other_files:
            print(i)
    return


def print_all():
    print_turdatas()
    print("********************")
    print_segments()
    print("********************")
    print_ruters()
    print("********************")
    print_other()
    print("********************")
    print_warnings()
    return


def print_warnings():
    for i in warnings:
        print(i)
    for turdata in tur_data_files_parsed:
        print(turdata.get_warnings())
    for ruter in ruter_files_parsed:
        print(ruter.get_warnings())
    for seg in segment_files_no_turtur:
        print(seg.get_warnings())
    return


def main():
    if len(sys.argv) < 2:
        usage()
        return

    walk_folder(sys.argv[1])

    if len(turdata_file) != 1:
        warn = "Warning, there should be exactly 1 Tur data file"
        warnings.append(warn)
    for i in turdata_file:
        turdata = TurDataFile(i)
        tur_data_files_parsed.append(turdata)

    if len(ruter_file) != 1:
        warn = "Warning, there should be exactly 1 Ruter file"
        warnings.append(warn)
    for i in ruter_file:
        ruter = RuterFile(i)
        ruter_files_parsed.append(ruter)

    # ..todo:: test associate segment files to tur turs

    for turdatafile in tur_data_files_parsed:
        turnums = turdatafile.get_tur_numbers()
        for turnum in turnums:
            turtur = turdatafile.get_turtur(turnum)
            for seg_num in turtur.get_segment_numbers():
                if seg_num in segment_files.keys():
                    turtur.add_segment(seg_num, SegmentFile(segment_files[seg_num]))
                    segment_files.pop(seg_num)
                else:
                    warn = "Warning, Tur Tur {} expects Segment {}, but it was not found.".format(turnum, seg_num)
                    warnings.append(warn)

    if len(segment_files) > 0:
        for i in segment_files.keys():
            warn = "Warning, Segment at {} is not associated with a Tur Tur".format(segment_files[i])
            warnings.append(warn)
            segment_files_no_turtur.append(SegmentFile(segment_files[i]))
    return


def usage():
    print('Usage: "python ' + sys.argv[0] + ' c:\\path\\to\\olex\\files"')
    return


if __name__ == '__main__':
    main()
    print_all()
    print_warnings()
