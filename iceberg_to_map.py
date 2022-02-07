import sys
from geopy import distance


def text_to_geopoint(lat_lon_str):
    lat_str, lon_str = lat_lon_str.strip().split('\t')
    lat = float(lat_str[:-1])
    lon = float(lon_str[:-1])
    if lat_str[-1] == 'S':
        lat = -lat
    if lon_str[-1] == 'W':
        lon = -lon
    return (lat, lon)


def compute_distance_in_meters(prev_point, current_point):
    return distance.distance(current_point, prev_point).km * 1000


def convert_icefront_to_huginos_format_based_on_distance(filename):
    distance_threshold = 25
    data = []
    prev_point = None
    current_point = None

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            prev_point = current_point
            current_point = text_to_geopoint(line)
            if not prev_point:
                data.append(''.join([line.strip(), '\t10']))
            elif compute_distance_in_meters(
                    prev_point, current_point) > distance_threshold:
                data.append(''.join([line.strip(), '\t10']))
            else:
                data.append(''.join([line.strip(), '\t15']))
    write_to_map_file(filename, data)


def write_to_map_file(filename, data):
    output_file = f'{filename.split(".")[0]}.map'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(data))


def generate_hugin_line(line, val):
    return ''.join([line.strip(), f'\t{val}'])


def generate_hugin_line_start_point(line):
    return generate_hugin_line(line, 10)


def generate_hugin_line_end_point(line):
    return generate_hugin_line(line, 15)


def generate_hugin_line_red_point(line):
    return generate_hugin_line(line, 0)


def convert_automated_icebergs_to_hugin_points(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(''.join([line.strip(), '\t0']))
    write_to_map_file(filename, data)


def convert_handdrawn_icebergs_to_hugin_lines_and_points(filename):
    start_line = True
    end_point = None
    data = []
    data_points = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == '':
                data.append(end_point)
                start_line = True
                continue
            if start_line:
                current_line = generate_hugin_line_start_point(line)
                #Update end point used to close the loop
                end_point = generate_hugin_line_end_point(line)
            else:
                current_line = generate_hugin_line_end_point(line)
            data.append(current_line)
            data_points.append(generate_hugin_line_red_point(line))
            # Reset startline
            start_line = False
    # Append data_points to data list
    data.extend(data_points)
    # Write data to file
    write_to_map_file(filename, data)
