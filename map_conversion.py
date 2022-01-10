import os
from datetime import datetime
import subprocess
from consts import *
from tqdm import tqdm


def gdalwarp_AMSR2_seaice_concentration(source_file: str, output_file: str):
    output = subprocess.run([
        'gdalwarp', '-s_srs', 'EPSG:3412', '-t_srs', 'EPSG:4326', '-te',
        '-180', '-90', '180', '90', source_file, output_file
    ],
                            capture_output=True)
    print(f'source: {source_file},\n target: {output_file}')
    print(output)


def amsr2_to_hugin_folder():
    amsr2_tif_source = set(x for x in os.listdir(SEA_ICE_CONCENTRATION)
                           if x.split('.')[-1] == 'tif')
    amsr2_tif_target = set(os.listdir(HUGIN_MAPS_AMSR2_SEA_ICE_CONCENTRATION))

    for source in tqdm(amsr2_tif_source):
        if source in amsr2_tif_target:
            continue
        source_file = os.path.join(SEA_ICE_CONCENTRATION, source)
        output_file = os.path.join('./data/AMSR2', source)
        gdalwarp_AMSR2_seaice_concentration(source_file, output_file)


def gdalwarp_MODIS_seaice_image(source_file: str, output_file: str):
    subprocess.run([
        'gdalwarp', '-t_srs', '+proj=longlat +datum=WGS84 +no_defs',
        source_file, output_file
    ])


def seaice_modis_data():
    modis_tif_source = set(x for x in os.listdir(SEA_ICE_IMAGERY)
                           if x.split('.')[-1] == 'tiff')
    modis_tif_target = set(os.listdir(HUGIN_MAPS_MODIS_SEA_ICE_IMAGERY))

    for source in tqdm(modis_tif_source):
        if source in modis_tif_target:
            continue
        source_file = os.path.join(SEA_ICE_IMAGERY, source)
        output_file = os.path.join('./data/MODIS', source)
        gdalwarp_MODIS_seaice_image(source_file, output_file)
