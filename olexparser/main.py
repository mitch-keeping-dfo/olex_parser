import os
import re
import sys
import gpxpy
import olexparser.convert as convert
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


def parsed_turdata_data_to_gpx():
    """Converts the contents of a parsed Turdata file into a GPX string

    :return: a string containing the Turdata file contents as GPX format
    :rtype: gpxpy.gpx.GPX()

    .. todo:: complete gpx conversions
    """
    gpx = gpxpy.gpx.GPX()
    for turdata in tur_data_files_parsed:
        for tur_tur_number in turdata.get_tur_numbers():
            tur_tur = turdata.get_turtur(tur_tur_number)

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
