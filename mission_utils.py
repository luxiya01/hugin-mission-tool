import datetime
import pandas as pd
import os
import re
from mission_parser import MissionParser
from data import Mission, WayPoint
from flags import START_WATER_SAMPLING, STOP_WATER_SAMPLING
from utils import utc_time_str_to_unixtime


def get_lat_lon_depth_from_vehicle_ctd(
        vehicle_ctd: pd.DataFrame,
        unixtime: float,
        max_time_diff: float = 60) -> (float, float, float):
    """Given a vehicle_ctd dataframe, a target unix time and an allowed max_time_diff,
    return the (lat, lon, depth) tuple from the vehicle_ctd at the first timestamp greater
    than the target unix time.

    Parameters
    ----------
    vehicle_ctd: pd.DataFrame
        The Pandas DataFrame constructed from the VehicleCTD.txt
        This is the value returned by the function vehicle_ctd_to_df
    unixtime: float
        The target unix time
    max_time_diff: float
        The maximum allowed time difference between the returned vehicle_ctd value and the
        target unixtime (in seconds)

    Returns
    -------
    lat: float
    lon: float
    depth: float
    """
    results = vehicle_ctd[vehicle_ctd.unixtime > unixtime]
    if len(results) <= 0:
        return
    idx = results.index[0]
    ctd_time = vehicle_ctd.loc[idx, 'unixtime']
    if abs(unixtime - ctd_time) > max_time_diff:
        return
    return (vehicle_ctd.loc[idx, 'lat'], vehicle_ctd.loc[idx, 'lon'],
            vehicle_ctd.loc[idx, 'depth'])


def vehicle_ctd_to_df(vehicle_ctd_path: str) -> pd.DataFrame:
    """Given the path to the VehicleCTD.txt file from a Hugin mission, return
    a pandas DataFrame from the file.

    Parameters
    ----------
    vehicle_ctd_path: str
        Path to the vehicle ctd file.
        This file is found at mission_folder/env/ctd/VehicleCTD.txt

    Returns
    -------
    vehicle_ctd: pd.DataFrame
        A Pandas DataFrame containing the VehicleCTD data.
    """
    vehicle_ctd_cols = [
        'unixtime', 'lat', 'lon', 'depth', 'sound_speed', 'temperature',
        'salinity', 'conductivity', 'pressure', 'time_quality',
        'position_quality', 'validity_bitmap'
    ]
    vehicle_ctd = pd.read_csv(vehicle_ctd_path,
                              sep='\t',
                              names=vehicle_ctd_cols)
    return vehicle_ctd


def parse_cp_events(cp_event_path: str) -> pd.DataFrame:
    """Given path the CP-Events.txt file in a Hugin mission folder,
    return a DataFrame with information on when each line in the mission
    plan was completed. When parsing the CP-Events.txt, the time that mission
    line i is read is used as the time that mission line (i-1) is completed.

    Parameters
    ----------
    cp_event_path: str
        Path to the CP-Events.txt
        This file is found at mission_folder/cp/EventLog/CP-Events.txt

    df: pd.DataFrame
        A pandas dataframe with the following columns:
            [name, waypoint_nr, time_str (UTC), unixtime]
    """
    mission_line_timestamps = []
    cp_time_fmt = '%Y.%m.%d %H:%M:%S'
    cp_line_pattern = re.compile(
        r'(\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}).\d{6}\s+([\w\s\(\)]+):\s+([\w\s]+):\s+(.+)'
    )
    mission_plan_read_pattern = re.compile(r'Mission plan read (\d*)')
    nose_released_pattern = re.compile('Nose released')
    with open(cp_event_path, 'r', encoding='utf-8') as cp_event_file:
        cp_events = cp_event_file.readlines()
    for i, line in enumerate(cp_events):
        line = line.strip()
        parsed_line = re.match(cp_line_pattern, line)

        # The first few lines of the CP-Events.txt has a different format and can be ignored
        if not parsed_line:
            continue

        time_str = parsed_line.group(1)
        unixtime = utc_time_str_to_unixtime(time_str=time_str,
                                            time_fmt=cp_time_fmt)
        event_details = parsed_line.group(4)
        mission_plan_read_match = re.search(mission_plan_read_pattern,
                                            event_details)

        if mission_plan_read_match:
            mission_line_read = int(mission_plan_read_match.group(1))
            if mission_line_read > 2:
                mission_line_reached = mission_line_read - 1
                mission_line_timestamps.append([
                    f'Waypoint number {mission_line_reached}',
                    mission_line_reached, time_str, unixtime
                ])
            continue

        nose_released_match = re.search(nose_released_pattern, event_details)
        if nose_released_match:
            mission_line_timestamps.append(
                ['recovery_start', -1, time_str, unixtime])

        if i == (len(cp_events) - 1):
            mission_line_timestamps.append(
                ['recovery_ends', -1, time_str, unixtime])
    df = pd.DataFrame(
        mission_line_timestamps,
        columns=['name', 'waypoint_nr', 'time_str (UTC)', 'unixtime'])
    return df


def parse_water_sample_locations_and_time(mission_folder: str,
                                          save: bool = True) -> pd.DataFrame:
    pass


def parse_mission_data_for_waypoint_locations_and_time(mission_folder: str,
                                                       save: bool = True
                                                       ) -> pd.DataFrame:
    """Given the path to the mission_folder containing all Hugin data from a mission,
    parse the time and location reaching each waypoints based on the following info:
        - mission plan: mission_folder/mission.mp
        - CP (control processor) events: mission_folder/cp/EventLog/CP-Events.txt
        - Hugin's CTD data: mission_folder/env/ctd/VehicleCTD.txt

    Parameters
    ----------
    mission_folder: str
        Path to the folder containing Hugin mission data
    save: Bool
        If true, the resulting pd.DataFrame will be stored to the current directory, i.e.
        the directory where the script is run, under the name mission_folder.csv

    Returns
    -------
    mission_data: pd.DataFrame
        A dataframe containing the following information for each waypoint:
        [waypoint_nr, lat_from_mp, lon_from_mp, timestamp (UTC), unixtime, lat_from_vehicle_ctd,
        lon_from_vehicle_ctd, depth_from_vehicle_ctd]
    """
    mission_data = []

    # Load mission plan
    mp_path = os.path.join(mission_folder, 'mission.mp')
    mission_plan = MissionParser.parse_file(mp_path)

    # Load vehicleCTD
    vehicle_ctd_path = os.path.join(mission_folder, 'env/ctd/VehicleCTD.txt')
    vehicle_ctd = vehicle_ctd_to_df(vehicle_ctd_path)

    # Parse CP-Events
    cp_event_path = os.path.join(mission_folder, 'cp/EventLog/CP-Events.txt')
    cp_event_df = parse_cp_events(cp_event_path)

    for row_idx, (name, waypoint_nr, time_str,
                  unixtime) in cp_event_df.iterrows():
        ctd_vals = get_lat_lon_depth_from_vehicle_ctd(vehicle_ctd, unixtime)
        if not ctd_vals:
            mission_data.append([
                name, waypoint_nr, time_str, unixtime, '', '', '', '', '', '',
                '', '', ''
            ])
            continue
        ctd_lat, ctd_lon, ctd_depth = ctd_vals

        if waypoint_nr:
            reached_waypoint = mission_plan.mission[waypoint_nr - 1]
            mission_data.append([
                name, waypoint_nr, time_str, unixtime,
                reached_waypoint.latitude_in_dd,
                reached_waypoint.longitude_in_dd, reached_waypoint.Latitude,
                reached_waypoint.Longitude, ctd_lat, ctd_lon, ctd_depth,
                WayPoint.degree_decimals_to_degree_minutes(ctd_lat,
                                                           is_lat=True),
                WayPoint.degree_decimals_to_degree_minutes(ctd_lon,
                                                           is_lat=False)
            ])
        else:
            mission_data.append([
                name, waypoint_nr, time_str, unixtime, '', '', '', '', ctd_lat,
                ctd_lon, ctd_depth,
                WayPoint.degree_decimals_to_degree_minutes(ctd_lat,
                                                           is_lat=True),
                WayPoint.degree_decimals_to_degree_minutes(ctd_lon,
                                                           is_lat=False)
            ])

    df = pd.DataFrame(mission_data,
                      columns=[
                          'name', 'waypoint_nr', 'timestamp (UTC)', 'unixtime',
                          'lat_from_mp', 'lon_from_mp', 'lat_from_mp_dm',
                          'lon_from_mp_dm', 'lat_from_vehicle_ctd',
                          'lon_from_vehicle_ctd', 'depth_from_vehicle_ctd',
                          'lat_from_vehicle_ctd_dm', 'lon_from_vehicle_ctd_dm'
                      ])
    if save:
        mission_name = os.path.basename(os.path.normpath(mission_folder))
        df.to_csv(f'{mission_name}.csv', index=False)
    return df


def add_water_sampling_commands(filepath: str) -> (Mission, str):
    """Given the filepath to a mission plan, add START_WATER_SAMPLING flag to all
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
    ws_pattern = re.compile(START_WATER_SAMPLING.comment)
    mission = MissionParser.parse_file(filepath)
    for i in range(mission.length - 1):
        waypoint = mission.mission[i]
        if re.search(ws_pattern, waypoint.Comment):
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
    #TODO: add test for convert_mission_file_to_latlon_csv!
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
