from enum import Enum
from dataclasses import dataclass
from geopy import distance
from geopy.point import Point
from typing import List
from datetime import datetime, timedelta
from numpy import floor, ceil, arctan2, rad2deg


class DepthControlMode(Enum):
    """An Enum representing the depth control mode"""
    DEPTH = 'D'
    STEEPCONTROL = 'S'
    TRAJECTORY = 'T'
    ALTITUDE = 'A'
    DEADBANDALTITUDE = 'B'


class GuidanceMode(Enum):
    """An Enum representing the guidance control mode"""
    WAYPOINT = 'W'
    PIPELINETRACKING = 'P'
    COURSE = 'C'
    HEADING = 'H'
    CIRCLE = 'S'


class SpeedControlMode(Enum):
    """An Enum representing the speed control mode"""
    RPM = 'R'
    SPEED = 'S'


@dataclass
class WayPoint:
    """
    A class used to represent a WayPoint, corresponds to one line in the .mp mission file

    Parameters
    ----------
    No: int = None
        Line number of the WayPoint in the .mp file
    Comment: str = ''
        User defined free text comment associated with the WayPoint. No length limit.
    Tag: str
        User defined free text tag associated with the WayPoint, e.g. 'dive', 'pumpco2o'
        Used to tag all payload and mission data. Length limited to 8 chars.
    Depth: float
        Target depth (m below surface) of the WayPoint.
        Used if DMo is one of (DEPTH - D, STEEPDEPTH - S, TRAJECTORY - T).
    Alt: float
        Target altitude (m above the sea floor) of the WayPoint.
        Use if DMo is (ALTITUDE - A). Interpreted as minimum altitude in other DMo.
    DMo: DepthControlMode Enum
        Indicates the depth control mode.
    Latitude: str
        Target latitude of the WayPoint, given in DDM (degrees decimal minutes)
    Longitude: str
        Target longitude of the WayPoint, given in DDM (degrees decimal minutes).
    Course: float
        Target course/heading (orientation of the AUV relative to North (0 degree)).
        Automatically computed heading, as opposed to user-specified heading, is given in
        parenteses().
    GMo: GuidanceMode Enum
        Indicates the guidance mode. Note that (WAYPOINT - W) is automatically selected if
        there is a waypoint position and no GuidanceMode is given.
    RPM: float
        Revolutions per minute for propulsion motor. Use if SMo is (RPM - R).
    Speed: float
        Speed in m/s; or in knots if the value is followed by a 'k'.
        Used if SMo is (SPEED - S).
    SMo: SpeedControlMode Enum
        Indicates the speed control mode.
    Dur: float
        Duration of the mission line (from the previous WayPoint in the mission file) in seconds.
        Automatically computed duration (in WAYPOINT mode) is given in parenteses().
    Dist: float
        Travel distance of the mission line (from the previous WayPoint in the mission file) in
        meters. Automatically computed distance (in WAYPOINT mode) is given in parenteses().
    Flags: str
        Flags and commands.
    """
    No: int = None
    Comment: str = None
    Tag: str = None
    Depth: float = None
    Alt: float = None
    DMo: DepthControlMode = None
    Latitude: str = None
    Longitude: str = None
    Course: float = None
    GMo: GuidanceMode = None
    RPM: float = None
    Speed: float = None
    SMo: SpeedControlMode = None
    Dur: float = None
    Dist: float = None
    Flags: str = None

    @property
    def position(self) -> Point:
        """Returns the target point (latitude, longitude, altitude) of the WayPoint"""
        #TODO: compute target altitude
        return Point(latitude=self.latitude_in_dd,
                     longitude=self.longitude_in_dd,
                     altitude=None)

    @property
    def latitude_in_dd(self) -> float:
        """Returns the target latitude in degrees decimal"""
        return WayPoint.degree_minutes_to_degree_decimals(self.Latitude)

    @property
    def longitude_in_dd(self) -> float:
        """Returns the target longitude in degrees decimal"""
        return WayPoint.degree_minutes_to_degree_decimals(self.Longitude)

    @classmethod
    def degree_minutes_to_degree_decimals(cls, ddm_str: str) -> float:
        """Convert a DDM string to DD format. Used to convert longitude and latitude"""
        if ddm_str is None:
            return None
        degrees, minutes_str = ddm_str.split(':')
        degrees_dd = int(degrees) + float(minutes_str[:-1]) / 60

        direction = minutes_str[-1]
        if direction in ('S', 'W'):
            degrees_dd *= -1
        return degrees_dd

    @classmethod
    def degree_decimals_to_degree_minutes(cls, dd: float, is_lat=True) -> str:
        """Convert a DD float to DDM string"""
        degrees = floor(abs(dd))
        minutes = (abs(dd) - degrees) * 60

        minutes_str = f'{minutes:.4f}'
        # pad 0 if minutes < 10
        if minutes < 10:
            minutes_str = f'0{minutes:.4f}'

        direction = ''
        if is_lat:
            direction = 'N' if dd > 0 else 'S'
        else:
            direction = 'E' if dd > 0 else 'W'
        return f'{degrees}:{minutes_str}{direction}'


@dataclass
class Mission:
    """
    A class used to represent a Hugin mission.
    Corresponds to the content of one .mp mission file.
    """
    filename: str = None
    header: List[str] = None
    #TODO: compute longitude and latitude from other waypoint data when they show up as None
    mission: List[WayPoint] = None

    @property
    def length(self) -> int:
        """Returns the length of the mission (number of WayPoints)"""
        return 0 if not self.mission else len(self.mission)

    @property
    def cumulative_mission_time(self) -> List[float]:
        """Returns the cumulative time at each mission WayPoint in seconds"""
        mission_time = []  #cumulative time reaching the first WayPoint
        if self.mission is not None:
            mission_time.append(self.mission[0].Dur)
            for m in self.mission[1:]:
                mission_time.append(mission_time[-1] + m.Dur)
        return mission_time

    def compute_mission_timestamps(self,
                                   start_time: datetime = None
                                   ) -> List[datetime]:
        """Given a mission start_time, returns a list of datetime where timestamps[i]
        corresponds to the datetime when the ith WayPoint will be reached."""
        if not start_time:
            start_time = datetime.now()
        timestamps = [
            start_time + timedelta(seconds=t)
            for t in self.cumulative_mission_time
        ]
        return timestamps

    def add_waypoint(self,
                     lat: float,
                     lon: float,
                     index: int,
                     comment='',
                     tag='',
                     flags='') -> None:
        """Add a Waypoint by giving a new (Lat, Lon) value, the waypoint will be added behind
        the exisiting Waypoint with index. If No is None, append the new waypoint to the end of
        the mission. Note that this method assumes that the vehicle is in speed control mode,
        i.e. it computes the Duration based on the Distance and the current speed."""
        prev_waypoint = self.mission[index]
        new_lat_str = WayPoint.degree_decimals_to_degree_minutes(lat)
        new_lon_str = WayPoint.degree_decimals_to_degree_minutes(lon)

        dst_latlon = (lat, lon)
        src_latlon = (prev_waypoint.latitude_in_dd,
                      prev_waypoint.longitude_in_dd)
        distance_in_m = distance.distance(dst_latlon, src_latlon).km * 1000
        # Compute duration
        current_speed = prev_waypoint.Speed
        duration = ceil(distance_in_m / current_speed)
        # Compute course
        #TODO: debug compute course!
        course = 0  #Mission.compute_course(src_latlon, dst_latlon)

        new_waypoint = WayPoint(No=index,
                                Comment=comment,
                                Tag=tag,
                                Depth=prev_waypoint.Depth,
                                Alt=prev_waypoint.Altitude,
                                DMo=prev_waypoint.DMo,
                                Latitude=new_lat_str,
                                Longitude=new_lon_str,
                                Course=course,
                                GMo=prev_waypoint.GMo,
                                RPM=prev_waypoint.RPM,
                                Speed=prev_waypoint.Speed,
                                SMo=prev_waypoint.SMo,
                                Dur=duration,
                                Dist=distance_in_m,
                                Flags=flags)
        self.mission.insert(index, new_waypoint)
        self._increment_waypoint_No(insert_index=index)

    def _increment_waypoint_No(self, insert_index: int) -> None:
        for waypoint in self.mission[insert_index + 1:]:
            waypoint.No += 1

    @classmethod
    def compute_course(
        cls, src_latlon: (float, float), dst_latlon: (float, float)) -> float:
        """Assumes src_latlon and dst_latlon are given in (latitude, longitude).
        Return the course in degrees."""
        #TODO: debug compute_course method!
        adjacent_src_dst = distance.distance((dst_latlon[0], src_latlon[1]),
                                             src_latlon).km
        if adjacent_src_dst == 0:
            return 0

        hypothenus_src_dst = distance.distance(
            dst_latlon, (dst_latlon[0], src_latlon[1])).km
        course_in_rad = arctan2(hypothenus_src_dst, adjacent_src_dst)
        course_in_degree = rad2deg(course_in_rad)
        return course_in_degree
