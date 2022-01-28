import re


def parse_ini_file(filepath: str) -> dict:
    """Parse ini files from HuginOS

    Parameters
    ----------
    filename: str
        Path to the .ini file

    Returns
    -------
    ini_params
        A nested dict of the form {section_name: {param_name: param_value}}
    """
    #TODO: store param values in the appropriate type (e.g. int, float) instead of all str

    # section name format: [section name]
    section_name_pattern = re.compile(r'\[(.+)\]')
    # param format: paramName = value  # comments-if-any
    param_pattern = re.compile(r'([\w\s_-]+)=([\s\w\d]+)\s*(#.+)*')

    ini_params = {}
    current_section = None
    with open(filepath, 'r', encoding='utf-8') as ini_file:
        for line in ini_file:
            section_name_matches = re.match(section_name_pattern, line)
            param_matches = re.match(param_pattern, line)
            if section_name_matches:
                current_section = section_name_matches.group(1).strip()
                ini_params[current_section] = {}
            elif param_matches:
                param_name = param_matches.group(1).strip()
                param_value = param_matches.group(2).strip()
                ini_params[current_section][param_name] = param_value
    return ini_params
