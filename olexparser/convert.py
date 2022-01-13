import datetime
import math
import pytz


def get_timestamp_str_from_bytes(time_bytes, timezone=pytz.timezone("UTC")):
    """Takes little endian bytes representing a Unix Timestamp integer and returns it as a datetime

    :param time_bytes: little endian bytes representing a Unix Timestamp integer
    :type time_bytes: bytes
    :param timezone: optional Timezone information. Defaults to UTC
    :type timezone: datetime.tzinfo
    :return: :class:`datetime.datetime`
    :rtype: :class:`datetime.datetime`
    """
    return datetime.datetime.fromtimestamp(int.from_bytes(time_bytes, "little"), tz=timezone)


def get_timestamp_str_from_int(time_int, timezone=pytz.timezone("UTC")):
    """Takes an integer and returns it as a datetime

    :param time_int: an int representing a Unix Timestamp
    :type time_int: int
    :param timezone: optional Timezone information. Defaults to UTC
    :type timezone: :class:`datetime.tzinfo`
    :return: :class:`datetime.datetime`
    :rtype: :class:`datetime.datetime`
    """
    return datetime.datetime.fromtimestamp(time_int, tz=timezone)


def get_lat_dmm(lat):
    """Takes an OLEX float and converts it into DMM latitude notation (eg. 51'6.432 N)

    :param lat: An 'Olex float' representing a latitude coordinate.
    :type lat: float

    :return: A latitude coordinate (eg. 51'6.432 N)
    :rtype: str
    """
    lat_d = math.trunc(math.fabs(lat / 60))
    lat_m = math.fabs(lat) - (math.fabs(lat_d) * 60)
    lat_m = str(lat_m)
    lat_m = lat_m[:lat_m.index('.')+4]
    if lat > 0:
        return str(lat_d) + "'" + lat_m + " N"
    else:
        return str(lat_d) + "'" + lat_m + " S"


def get_long_dmm(long):
    """Takes an OLEX float and converts it into DMM longitude notation (e.g. 51'6.432 W)

    :param long: An 'Olex float' representing a longitude coordinate.
    :type long: float

    :return: A longitude coordinate (e.g. 51'6.432 W)
    :rtype: str
    """
    long_d = math.trunc(math.fabs(long / 60))
    long_m = math.fabs(long) - (math.fabs(long_d) * 60)
    long_m = str(long_m)
    long_m = long_m[:long_m.index('.')+4]
    if long > 0:
        return str(long_d) + "'" + long_m + " E"
    else:
        return str(long_d) + "'" + long_m + " W"


def get_lat_or_long_dd(lat_or_long):
    """Takes an OLEX float and converts it into DD notation (e.g. -74.003)

    :param lat_or_long: An 'Olex float' representing either a latitude ot longitude coordinate.
    :type lat_or_long: float

    :return: A DD notation coordinate (e.g. -74.003)
    :rtype: float
    """
    lat_d = math.trunc(math.fabs(lat_or_long) / 60)
    lat_m = (lat_or_long - (lat_d * 60)) / 60
    lat_dd = lat_d + lat_m
    return lat_dd
