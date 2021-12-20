from dataclasses import dataclass
from geopy.point import Point

class WayPoint:
    #TODO: check tag length limit!
    #TODO: what is Hugin's behavior when we supply both depth and altitude???
    """
    A class used to represent a WayPoint, corresponds to one line in the .mp mission file

    Parameters
    ---
    comment: str, default None
        User defined free text comment associated with the WayPoint. No length limit.
    tag: str, defaultl ''
        User defined free text tag associated with the WayPoint, e.g. 'dive', 'pumpco2o'
        Length limited to WHAT number of chars???
    id_: int
        Automatically assigned ID of the WayPoint in a mission, usually corresponds to the index
        of the WayPoint in the mission.
    depth: float
        Target depth of the WayPoint.
    altitude: float
        Target altitude of the WayPoint.
    depth_mode: #TODO
    point: geopy.point.Point(latitude, longitude, altitude=None)
        Target position (latitude, longitude) of the WayPoint.
    course: float
        Target course (orientation of the AUV relative to North (0 degree)).
    GMo: #TODO
    RPM: #TODO
    Speed: #TODO
    SMo: #TODO
    duration: #TODO
    dist: #TODO
    flag: #TODO
    """
    comment: str
    tag: str
    id_: int
    depth: float
    altitude: float
    point: Point
    course: float
