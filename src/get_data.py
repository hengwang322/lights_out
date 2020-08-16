"""This script fetches the original Street Lighting Assets data and cleans it. 
"""

import os
import numpy as np
import geopandas as gpd


LIGHT_GEOJSON = 'https://opendata.arcgis.com/datasets/3bda41b12bbc4753b240b4866088080a_0.geojson'


def get_watt(watt_string):
    watt_list = [s for s in watt_string.split('_') if s.isdigit()]
    if len(watt_list) == 0:
        return np.nan
    else:
        return int(watt_list[0])


def clean(df):
    df_clean = df.copy()

    df_clean['lamp_type'] = df_clean['lamp_type'].apply(
        lambda x: np.nan if x == ' ' else x)
    df_clean = df_clean.dropna()

    important_lamp_type = ['MV', 'CFL', 'HPS', 'LED']

    df_clean['lamp_type'] = df_clean['lamp_type'].apply(lambda x: 'OTHER'
                                                        if x not in important_lamp_type
                                                        else x)

    return df_clean


def get_light_data(LIGHT_GEOJSON):
    light = gpd.read_file(LIGHT_GEOJSON)

    light['lon'] = light.geometry.apply(lambda point: point.x)
    light['lat'] = light.geometry.apply(lambda point: point.y)
    light['wattage'] = light.WATT_TYPE.apply(get_watt)

    cols = ['STREET_NAM', 'STREET_TYP', 'LAMP_TYPE', 'lon', 'lat', 'wattage']
    light = light[cols]
    col_name = ['street_name', 'street_type',
                'lamp_type', 'longitude', 'latitude', 'wattage']
    light.columns = col_name

    light = clean(light)

    return light


def main():
    light = get_light_data(LIGHT_GEOJSON)
    OUTPUT = os.path.join('..', 'light.csv')
    light.to_csv(OUTPUT, index=False)


if __name__ == '__main__':
    main()
