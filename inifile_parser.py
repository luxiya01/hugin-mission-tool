import os
import re


class IniFileParser:
    post_processing_ini_files = set([
        'OneClick.ini', 'ship.ini', 'utp.ini', 'estimator.ini',
        'cov_matrix.ini', 'preproc.ini'
    ])

    @classmethod
    def parse_ini_files_from_dir(cls, mission_folder: str) -> dict:
        """Parse all ini files from the folder and subfolders under dirpath.
        Each ini file is parsed using the parse_ini_file function.

        Parameters
        ----------
        mission_folder: str
            Path to the mission folder generated by HuginOS, .ini files will be
            searched in the mission_folder and all its subfolders.

        Returns
        -------
        ini_params: dict
            A nested dict of the following form:
                {ini_file_name:
                    {'filepath': filepath,
                    'content': {section_name: {param_name: param_value}}
                    }
                }
        num_ini_files: int
            Number of .ini files found
        """
        ini_files = {}
        num_ini_files = 0
        for (dirpath, _, filenames) in os.walk(mission_folder):
            for filename in filenames:
                if filename.split(
                        '.'
                )[-1] == 'ini' and filename not in cls.post_processing_ini_files:
                    ini_files[filename] = os.path.join(dirpath, filename)
                    num_ini_files += 1

        ini_params = {}
        for filename, filepath in ini_files.items():
            file_content = cls.parse_ini_file(filepath)
            ini_params[filename] = {
                'filepath': filepath,
                'content': file_content
            }
        return ini_params, num_ini_files

    @classmethod
    def parse_ini_file(cls, filepath: str) -> dict:
        """Parse ini files from HuginOS

        Parameters
        ----------
        filename: str
            Path to the .ini file

        Returns
        -------
        ini_params: dict
            A nested dict of the form {section_name: {param_name: param_value}}
        """
        # section name format: [section name]
        section_name_pattern = re.compile(r'\[(.+)\]')
        # param format: paramName = value  # comments-if-any
        param_pattern = re.compile(r'([\w\s_-]+)=([-\.\s\w\d]+)\s*(#.+)*')

        ini_params = {}
        current_section = None
        with open(filepath, 'r', encoding='latin-1') as ini_file:
            for line in ini_file:
                section_name_matches = re.match(section_name_pattern, line)
                param_matches = re.match(param_pattern, line)
                if section_name_matches:
                    current_section = section_name_matches.group(1).strip()
                    ini_params[current_section] = {}
                elif param_matches:
                    param_name = param_matches.group(1).strip()
                    param_value = param_matches.group(2).strip()
                    try:
                        ini_params[current_section][param_name] = param_value
                    except KeyError as e:
                        print(filepath, line)
        return ini_params
