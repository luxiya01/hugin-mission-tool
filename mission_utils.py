import datetime
import pandas as pd
import os
from dataclasses import dataclass
from mission_parser import MissionParser
from data import Mission

#TODO: add tests for this module!


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
    explanation: str
        The comment that this flag corresponds to
    """
    name: str
    flag: str
    comment: str


START_WATER_SAMPLING = Flag(name='start_water_sampling',
                            flag='cmd=9C013C',
                            comment='WS')
STOP_WATER_SAMPLING = Flag(name='stop_water_sampling',
                           flag='cmd=9C012C',
                           comment='')


def add_water_sampling_commands(filepath: str) -> (Mission, str):
    """Given a filepath to a mission plan, add START_WATER_SAMPLING flag to all
    waypoints with a comment that starts with WS and add STOP_WATER_SAMPLING to
    the waypoint that directly follows the START_WATER_SAMPLING flag.

    Parameters
    ----------
    filepath: str
        Path to the .mp mission file.

    Returns
    -------
    mission: Mission
        The modified mission object with START_WATER_SAMPLING and STOP_WATER_SAMPLING
        flags added to the desired lines. The modified mission plan is writtten back
        to the input folder with _ws appended to the filename.
    output_filepath: str
        The output filepath (where the modified mission plan is written back to).
    """
    mission = MissionParser.parse_file(filepath)
    for i in range(mission.length - 1):
        waypoint = mission.mission[i]
        if START_WATER_SAMPLING.comment in waypoint.Comment:
            waypoint.Flags = START_WATER_SAMPLING.flag
            mission.mission[i + 1].Flags = STOP_WATER_SAMPLING.flag

    folder = os.path.dirname(filepath)
    filename = os.path.basename(os.path.normpath(filepath))
    output_filename = f'{filename.split(".")[0]}_ws.mp'
    output_filepath = os.path.join(folder, output_filename)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.writelines(str(mission))
    return mission, output_filepath


def convert_mission_file_to_latlon_csv(
        filepath: str,
        start_time=None,
        remove_rendezvous=False) -> pd.DataFrame:
    """Convert a mission file into a csv file with lat, lon and (if start_time is not
    None) timestamp for the time completing each line. WayPoints without explicit lat,
    lon values will be removed.

    Parameters
    ----------
    filepath: str
        Path to the .mp mission file.
    start_time: str, default=None
        Datetime represented in %Y-%m-%d %H:%M, used to compute the time reaching
        each waypoint.
    remove_rendezvous: bool, default=False
        If set to True, all WayPoints with "rendezvous" as their Flags will be removed
        prior to conversion to .csv file.

    Returns
    -------
    df: pd.DataFrame
        A pandas dataframe containing lat, lon and (if start_time is not
        None) timestamp of the time this waypoint is completed. The dataframe is
        also stored as a .csv using the same filepath as the input filepath parameter.
    """
    mission = MissionParser.parse_file(filepath).mission
    if remove_rendezvous:
        mission = [m for m in mission if m.Flags != 'rendezvous']
    df = pd.DataFrame()
    df['lat'] = [x.latitude_in_dd for x in mission]
    df['lon'] = [x.longitude_in_dd for x in mission]

    # Remove WayPoints without (lat, lon)
    df = df[~df.lat.isna() & ~df.lon.isna()]

    if start_time is not None:
        TIME_FMT = '%Y-%m-%d %H:%M'
        try:
            start_time = datetime.datetime.strptime(start_time, TIME_FMT)
        except Exception as e:
            print(e)
            return
        df['timestamp'] = mission.compute_mission_timestamps(start_time)
    df.to_csv(f'{filepath.split(".")[0]}.csv', index=False)
    return df
