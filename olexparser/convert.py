import datetime
import math


def get_timestamp_str_from_bytes(time_bytes):
    """Takes little endian bytes representing a Unix Timestamp integer and returns it as a datetime string

    :param time_bytes: little endian bytes representing a Unix Timestamp integer
    :type time_bytes: bytes

    :return: a Datetime
    :rtype: datetime.datetime
    """
    return datetime.datetime.fromtimestamp(int.from_bytes(time_bytes, "little"))


def get_timestamp_str_from_int(time_int):
    """Takes an integer and returns it as a datetime string

    :param time_int: an int representing a Unix Timestamp
    :type time_int: int

    :return: a Datetime
    :rtype: datetime.datetime
    """
    return datetime.datetime.fromtimestamp(time_int)


def get_lat_dmm(lat):
    """Takes an OLEX float and converts it into DMM latitude notation (eg. 51'6.432 N)

    :param lat: An 'Olex float' representing a latitude coordinate.
    :type lat: float

    :return: A latitude coordinate (eg. 51'6.432 N)
    :rtype: str
    """
    lat_d = math.trunc(math.fabs(lat / 60))
    lat_m = math.fabs(lat) - (math.fabs(lat_d) * 60)
    if lat > 0:
        return str(lat_d) + "'" + str(lat_m) + " N"
    else:
        return str(lat_d) + "'" + str(lat_m) + " S"


def get_long_dmm(long):
    """Takes an OLEX float and converts it into DMM longitude notation (eg. 51'6.432 W)

    :param long: An 'Olex float' representing a longitude coordinate.
    :type long: float

    :return: A longitude coordinate (eg. 51'6.432 W)
    :rtype: str
    """
    long_d = math.trunc(math.fabs(long / 60))
    long_m = math.fabs(long) - (math.fabs(long_d) * 60)
    if long > 0:
        return str(long_d) + "'" + str(long_m) + " E"
    else:
        return str(long_d) + "'" + str(long_m) + " W"


def get_lat_or_long_dd(lat_or_long):
    """Takes an OLEX float and converts it into DD notation (eg. -74.003)

    :param lat_or_long: An 'Olex float' representing either a latitude ot longitude coordinate.
    :type lat_or_long: float

    :return: A DD notation coordinate (eg. -74.003)
    :rtype: float
    """
    lat_d = math.trunc(math.fabs(lat_or_long) / 60)
    lat_m = (lat_or_long - (lat_d * 60)) / 60
    lat_dd = lat_d + lat_m
    return lat_dd

