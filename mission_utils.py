import datetime
import pandas as pd
from mission_parser import MissionParser


def convert_mission_file_to_latlon_csv(filename, start_time=None):
    mission = MissionParser.parse_file(filename)
    df = pd.DataFrame()
    df['lat'] = [x.latitude_in_dd for x in mission.mission]
    df['lon'] = [x.longitude_in_dd for x in mission.mission]

    if start_time is not None:
        TIME_FMT = '%Y-%m-%d, %H:%M'
        try:
            start_time = datetime.datetime.strptime(start_time, TIME_FMT)
        except Exception as e:
            print(e)
            return
        df['timestamp'] = mission.compute_mission_timestamps(start_time)
    return df.to_csv(f'{filename.split(".")[0]}.csv', index=False)
