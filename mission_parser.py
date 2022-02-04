import base64

from data import (Mission, WayPoint, DepthControlMode, GuidanceMode,
                  SpeedControlMode, Course, Duration, Distance)


class MissionParser:
    """A class used to parse Hugin mission .mp files"""
    header_line_idx = 5

    @classmethod
    def parse_upload(cls, filename, content_str):
        """Parse content from dcc.Upload component"""
        chars = base64.b64decode(content_str).decode('utf-8')
        lines = chars.split('\n')
        return cls._parse_content(filename, lines)

    @classmethod
    def parse_file(cls, filename):
        """Parse .mp file"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return cls._parse_content(filename, lines)

    @classmethod
    def _parse_content(cls, filename, lines):
        """Parse string content into a mission. Returns a Mission object."""

        mission = Mission(filename=filename,
                          mission=[],
                          meta_info=lines[:cls.header_line_idx + 2])
        header = cls._parse_line_content(lines[cls.header_line_idx],
                                         is_header=True)
        mission.header = header

        comment = ''
        prev_waypoint = None
        for line in lines[cls.header_line_idx:]:
            if len(line.strip().split()) == 0:
                continue
            if line[0] == '#':
                comment = line[1:].strip()
            else:
                waypoint = cls._parse_waypoint(line,
                                               header,
                                               comment=comment,
                                               prev_waypoint=prev_waypoint)

                # Reset comment and update mission and prev_waypoint
                comment = ''
                mission.mission.append(waypoint)
                prev_waypoint = waypoint
        return mission

    @classmethod
    def _parse_line_content(cls, line, is_header=False):
        """Parse one line from .mp file"""
        parts = line.strip().split()
        no_, tag = parts[0].split(':')
        if is_header:
            no_ = no_[1:]
        content = [no_, tag]
        content.extend(parts[1:])
        return content

    @classmethod
    def _parse_waypoint(cls, line, header, comment='', prev_waypoint=None):
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
        content = cls._parse_line_content(line)

        waypoint = WayPoint(Comment=comment)
        for attr_name, attr_value in zip(header, content):
            attr = cls._parse_attr(attr_name, attr_value, prev_waypoint)
            setattr(waypoint, attr_name, attr)

        # If the waypoint has an explitic latitude and longitude, then it is in WAYPOINT
        # GuidanceMode implicitly according to HuginOS documentation... See WayPoint class
        # docstrings
        if waypoint.Latitude is not None and waypoint.Longitude is not None:
            waypoint.GMo = GuidanceMode.WAYPOINT
        return waypoint

    @classmethod
    def _parse_attr(cls, attr_name, attr_value, prev_waypoint=None):
        """Parse a string attribute taken from one line in the .mp file"""
        if attr_value == '=':
            if prev_waypoint is None:
                return None
            return getattr(prev_waypoint, attr_name)

        if attr_value == '-':
            if attr_name == 'Dur':
                return Duration(value=None, is_computed_automatically=False)
            if attr_name == 'Dist':
                return Distance(value=None, is_computed_automatically=False)
            return None

        if attr_name == 'No' and attr_value == '':
            if prev_waypoint is None:
                return 1
            return prev_waypoint.No + 1

        if attr_name in ['Tag', 'Latitude', 'Longitude', 'Flags']:
            return attr_value

        if attr_name == 'Course':
            if attr_value[0] == '(' and attr_value[-1] == ')':
                return Course(value=float(attr_value[1:-1]),
                              is_computed_automatically=True)
            return Course(value=float(attr_value),
                          is_computed_automatically=False)
        if attr_name == 'Dur':
            if attr_value[0] == '(' and attr_value[-1] == ')':
                return Duration(value=int(attr_value[1:-1]),
                                is_computed_automatically=True)
            return Duration(value=int(attr_value),
                            is_computed_automatically=False)
        if attr_name == 'Dist':
            if attr_value[0] == '(' and attr_value[-1] == ')':
                return Distance(value=int(attr_value[1:-1]),
                                is_computed_automatically=True)
            return Distance(value=int(attr_value),
                            is_computed_automatically=False)

        if attr_name in ['Depth', 'Alt', 'RPM', 'Speed']:
            #TODO: handle knot in Speed!
            return float(attr_value)
        if attr_name == 'DMo':
            return cls._parse_mode(attr_value, mode=DepthControlMode)
        if attr_name == 'GMo':
            return cls._parse_mode(attr_value, mode=GuidanceMode)
        if attr_name == 'SMo':
            return cls._parse_mode(attr_value, mode=SpeedControlMode)
        return None

    @classmethod
    def _parse_mode(cls, attr_value, mode):
        """Return the mode whose value equals the attr_value"""
        for mode_data in mode:
            if attr_value == mode_data.value:
                return mode_data
        return None
