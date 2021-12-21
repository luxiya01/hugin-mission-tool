from enum import Enum
from dataclasses import dataclass
from geopy.point import Point

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
    ---
    line_number: int
        Line number, i.e. the index of the WayPoint in the mission.
    comment: str, default None
        User defined free text comment associated with the WayPoint. No length limit.
    tag: str, defaultl None
        User defined free text tag associated with the WayPoint, e.g. 'dive', 'pumpco2o'
        Used to tag all payload and mission data. Length limited to 8 chars.
    depth: float
        Target depth (m below surface) of the WayPoint.
        Used if DMo is one of (DEPTH - D, STEEPDEPTH - S, TRAJECTORY - T).
    altitude: float
        Target altitude (m above the sea floor) of the WayPoint.
        Use if DMo is (ALTITUDE - A). Interpreted as minimum altitude in other DMo.
    depth_control_mode: DepthControlMode Enum
        Indicates the depth control mode.
    point: geopy.point.Point(latitude, longitude, altitude=None)
        Target position (latitude, longitude) of the WayPoint.
    course: float
        Target course/heading (orientation of the AUV relative to North (0 degree)).
        Automatically computed heading, as opposed to user-specified heading, is given in
        parenteses().
    guidance_mode: GuidanceMode Enum
        Indicates the guidance mode. Note that (WAYPOINT - W) is automatically selected if
        there is a waypoint position and no GuidanceMode is given.
    rpm: float
        Revolutions per minute for propulsion motor. Use if SMo is (RPM - R).
    speed: float
        Speed in m/s; or in knots if the value is followed by a 'k'.
        Used if SMo is (SPEED - S).
    speed_control_mode: SpeedControlMode Enum
        Indicates the speed control mode.
    duration: float
        Duration of the mission line (from the previous WayPoint in the mission file) in seconds.
        Automatically computed duration (in WAYPOINT mode) is given in parenteses().
    distance: float
        Travel distance of the mission line (from the previous WayPoint in the mission file) in
        meters. Automatically computed distance (in WAYPOINT mode) is given in parenteses().
    flag: str
        Flags and commands.
    """
    line_number: int
    comment: str
    tag: str
    depth: float
    altitude: float
    depth_control_mode: DepthControlMode
    point: Point
    course: float
    guidance_mode: GuidanceMode
    rpm: float
    speed: float
    speed_control_mode: SpeedControlMode
    duration: float
    distance: float
    flag: str
