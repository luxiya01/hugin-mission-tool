from enum import Enum
from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta
from numpy import floor


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
class Course:
    """
    A class used to represent the course of a Waypoint. Note that the __repr__ is different
    depending on the bool.

    Parameters
    ----------
    value: float
        The numeric value of the course (0 = north, 180 = south)
    is_computed_automatically: bool
        Indicates whether the course is given by user or computed automatically, this controls
        the __repr__ of the Course object.
    """
    value: float
    is_computed_automatically: bool = False

    def __repr__(self):
        if self.is_computed_automatically:
            val = int(self.value)
            str_val = str(val)
            if val < 100:
                str_val = f'0{str(val)}'
            return f'({str_val})'
        value_repr = f'{self.value:5.1f}'.replace(' ', '0')
        return value_repr


@dataclass
class Duration:
    """
    A class used to represent the duration (in seconds) of a Waypoint.

    Parameters
    ----------
    value: int
        The numeric value of the duration of a Waypoint in seconds.
    is_computed_automatically: bool
        Indicates whether the duration is given by user or computed automatically, this controls
        the __repr__ of the Course object.
    """
    value: int
    is_computed_automatically: bool = False

    def __repr__(self):
        if self.is_computed_automatically:
            str_val = f'({self.value})'
            return f'{str_val:>6s}'
        if not self.value:
            return '     -'
        str_val = str(self.value)
        return f'{str_val:>6s}'


@dataclass
class Distance:
    """
    A class used to represent the distance (in meters) of a Waypoint.

    Parameters
    ----------
    value: int
        The numeric value of the distance required to reach the Waypoint from the previous Waypoint.
    is_computed_automatically: bool
        Indicates whether the distance is given by user or computed automatically, this controls
        the __repr__ of the Course object.
    """
    value: int
    is_computed_automatically: bool = False

    def __repr__(self):
        if self.is_computed_automatically:
            str_val = f'({self.value})'
            return f'{str_val:>7s}'
        if not self.value:
            return '     - '
        str_val = str(self.value)
        return f'{str_val:>6s} '


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
    Course: Course
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
    Dur: Duration
        Duration of the mission line (from the previous WayPoint in the mission file) in seconds.
        Automatically computed duration (in WAYPOINT mode) is given in parenteses().
    Dist: Distance
        Travel distance of the mission line (from the previous WayPoint in the mission file) in
        meters. Automatically computed distance (in WAYPOINT mode) is given in parenteses().
    Flags: str
        Flags and commands.
    original_string_representation: str
        The original string representation of the mission line and the corresponding comments above
        the line (if any).
    """
    No: int = None
    Comment: str = None
    Tag: str = None
    Depth: float = None
    Alt: float = None
    DMo: DepthControlMode = None
    Latitude: str = None
    Longitude: str = None
    Course: Course = None
    GMo: GuidanceMode = None
    RPM: float = None
    Speed: float = None
    SMo: SpeedControlMode = None
    Dur: Duration = None
    Dist: Distance = None
    Flags: str = None

    def repr_given_prev_waypoint(self, prev_waypoint: WayPoint) -> str:
        """Returns the string representation of the Waypoint given the previous waypoint,
        all properties that are equal to the given waypoint will be represented by = in the
        resulting string representation."""
        pass

    def __repr__(self) -> str:
        """Returns the string representation of the WayPoint as a single waypoint"""
        waypoint_str = (
            f':{self.tag_str} {self.Depth:6.1f} {self.Alt:5.1f}  {self.DMo.value} '
            f'{self.latitude_str:>11s} {self.longitude_str:>12s}  {self.Course}  {self.GMo.value}  {self.RPM:4.0f} '
            f'{self.speed_str} {self.SMo.value}  {self.Dur} {self.Dist}')
        if self.Flags:
            waypoint_str = ' '.join([waypoint_str, self.Flags])
        if self.Comment:
            waypoint_str = '\n'.join(['', f'# {self.Comment}', waypoint_str])
        return waypoint_str

    @property
    def tag_str(self) -> str:
        return f'{self.Tag:<8s}'

    @property
    def speed_str(self) -> str:
        if not self.Speed:
            return '  =  '
        return f'{self.Speed:5.2f}'

    @property
    def latitude_str(self) -> str:
        return '-' if not self.Latitude else self.Latitude

    @property
    def longitude_str(self) -> str:
        return '-' if not self.Longitude else self.Longitude

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
        degrees = int(floor(abs(dd)))
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
    meta_info: List[str] = None
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
            mission_time.append(self.mission[0].Dur.value)
            for m in self.mission[1:]:
                mission_time.append(mission_time[-1] + m.Dur.value)
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

    def __repr__(self) -> str:
        meta_info_str = ''.join(self.meta_info)
        mission_str = '\n'.join([str(m) for m in self.mission])
        return ''.join([meta_info_str, mission_str])
