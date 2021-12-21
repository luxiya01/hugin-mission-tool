from typing import List
from data import WayPoint, DepthControlMode, GuidanceMode, SpeedControlMode

class Mission:
    """
    A class used to represent a Hugin mission.
    Corresponds to the content of one .mp mission file.
    """

    def __init__(self, filename=None):
        self.header = []
        self.mission = []
        self.prev_waypoint = None
        self.filename = filename
        self.header_line_idx = 5

    def parse_file(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            lines = f.readlines()

        self.header = self._parse_line_content(lines[self.header_line_idx], is_header=True)
        
        comment = ''
        for line in lines[self.header_line_idx:]:
            if len(line.strip().split()) == 0:
                continue
            if line[0] == '#':
                comment = line[1:]
            else:
                waypoint = self._parse_waypoint(line, comment=comment)

                # Reset comment and update mission and prev_waypoint
                comment = ''
                self.mission.append(waypoint)
                self.prev_waypoint = waypoint
        return self.mission


    def _parse_line_content(self, line, is_header=False):
        """Parse one line from .mp file"""
        parts = line.strip().split()
        no_, tag = parts[0].split(':')
        if is_header:
            no_ = no_[1:]
        content = [no_, tag]
        content.extend(parts[1:])
        print(content)
        return content


    def _parse_waypoint(self, line, comment=''):
        """Parse one line in the .mp mission file into a WayPoint

        Parameters
        ----------
        line: str
            A string representing the waypoint, corresponds to one line in the .mp file
        comment: str
            A string representing the comment to this waypoint (the line before the WayPoint
            line in the .mp file)

        Returns
        -------
        waypoint
            A WayPoint object.
        """
        content = self._parse_line_content(line)

        waypoint = WayPoint(Comment=comment)
        for attr_name, attr_value in zip(self.header, content):
            attr = self._parse_attr(attr_name, attr_value)
            setattr(waypoint, attr_name, attr)
        print(waypoint)
        return waypoint


    def _parse_attr(self, attr_name, attr_value):
        """Parse a string attribute taken from one line in the .mp file"""
        if attr_value == '=':
            if self.prev_waypoint is not None:
                return getattr(self.prev_waypoint, attr_name)
            return None

        if attr_value == '-':
            return None

        if attr_name == 'No' and attr_value == '':
            print(len(self.mission))
            return len(self.mission)

        if attr_name in ['Tag', 'Latitude', 'Longitude', 'Flags']:
            return attr_value

        if attr_name in ['Course', 'Dur', 'Dist']:
            if attr_value[0] == '(' and attr_value[-1] == ')':
                return float(attr_value[1:-1])
            return float(attr_value)

        if attr_name in ['Depth', 'Alt', 'RPM', 'Speed']:
            return float(attr_value)
        if attr_name == 'DMo':
            return self._parse_mode(attr_value, mode=DepthControlMode)
        if attr_name == 'GMo':
            return self._parse_mode(attr_value, mode=GuidanceMode)
        if attr_name == 'SMo':
            return self._parse_mode(attr_value, mode=SpeedControlMode)


    def _parse_mode(self, attr_value, mode):
        """Return the mode whose value equals the attr_value"""
        for mode_data in mode:
            if attr_value == mode_data.value:
                return mode_data
