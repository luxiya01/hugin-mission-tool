from dataclasses import dataclass
import re


@dataclass
class Flag:
    """
    A class used to represent a Flag in Hugin missions.

    Parameters
    ----------
    name: str
        The name of the flag
    flag: str
        The command/flag used in HuginOS
    comment: str
        The regex comment that this flag corresponds to
    """
    name: str
    flag: str
    comment: str


START_WATER_SAMPLING = Flag(name='start_water_sampling',
                            flag='cmd=9C013C',
                            comment=r'WS ?\d+')
STOP_WATER_SAMPLING = Flag(name='stop_water_sampling',
                           flag='cmd=9C012C',
                           comment='')
