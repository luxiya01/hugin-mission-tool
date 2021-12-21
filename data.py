from enum import Enum
from dataclasses import dataclass
from geopy.point import Point
from typing import List

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
        Target latitude of the WayPoint.
    Longitude: str
        Target longitude of the WayPoint.
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

    def get_position(self) -> Point:
        """Returns the target point (latitude, longitude, altitude) of the WayPoint"""
        #TODO: compute target altitude
        return Point(latitude=self.Latitude, longitude=self.Longitude, altitude=None)


@dataclass
class Mission:
    """
    A class used to represent a Hugin mission.
    Corresponds to the content of one .mp mission file.
    """
    filename: str = None
    header: List[str] = None
    mission:  List[WayPoint] = None

    @property
    def length(self):
        """Returns the length of the mission (number of WayPoints)"""
        return 0 if not self.mission else len(self.mission)
