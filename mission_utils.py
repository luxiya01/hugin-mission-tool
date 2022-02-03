import datetime
import pandas as pd
import os
from dataclasses import dataclass
from mission_parser import MissionParser


@dataclass
class Flag:
    """
    A class used to represent a Flag in Hugin missions.

    Parameters
    ----------
    name: str
        The name of the flag
    command: str
        The command/flag used in HuginOS
    explanation: str
        The meaning of the flag in plain text
    """
    name: str
    flag: str
    explanation: str


START_WATER_SAMPLING_COMMENT = 'WS'
START_WATER_SAMPLING_FLAG = Flag(
    name='start_water_sampling',
    flag='cmd=9C013C',
    explanation='Start collecting water sample for one bottle')
STOP_WATER_SAMPLING_FLAG = Flag(
    name='stop_water_sampling',
    flag='cmd=9C012C',
    explanation='Stop collecting water sample for one bottle')
COMMENT_TO_FLAG = {START_WATER_SAMPLING_COMMENT: START_WATER_SAMPLING_FLAG}


def add_start_water_sampling_flag_to_mission(filepath: str):
    add_flag_according_to_comment(
        filepath=filepath,
        comment=START_WATER_SAMPLING_COMMENT,
        flag=COMMENT_TO_FLAG[START_WATER_SAMPLING_COMMENT].flag)

    folder = os.path.dirname(filepath)
    filename = os.path.basename(os.path.normpath(filepath))
    output_filename = f'{filename.split(".")[0]}_ws.mp'
    output_filepath = os.path.join(folder, output_filename)
    with open(output_filepath, 'w') as f:
        f.writelines('\n'.join(modified_mission))


def add_flag_according_to_comment(filepath: str, comment: str, flag: str):
    """Given a mission file, look for lines with the desired comment and add the
    flag specified to the line.

    Parameters
    ----------
    filepath: str
        Path to the .mp file.
    comment: str
        The string comment to look for.
    flag: str
        The string representation of the flag to be added to the mission line under
        the line with the specified comment.

    Returns
    -------
    modified_mission: List[str]
        A list of strings where each one represents one line in the mission plan.
        Compared to the mission plan from the input (parsed from param filepath),
        the output modified_mission adds the desired flag to the mission lines below
        the specified comments.
    """
    comment_str = f'# {comment}'
    add_flag = False
    modified_mission = []
    with open(filepath, 'r') as f:
        lines = [l.strip('\n') for l in f.readlines()]
        for line in lines:
            modified_line = line

            if add_flag:
                # separator is used to align the values in the Flag column
                separator = ' ' if line[-1] == ')' else '  '
                modified_line = separator.join([line, flag])
                add_flag = False
            modified_mission.append(modified_line)

            if comment_str in line:
                add_flag = True
    return modified_mission


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
