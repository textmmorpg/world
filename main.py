from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tqdm
import math
from datetime import datetime
from multiprocessing import Pool
from random import random
import pickle
import cv2

size_x, size_y = 500, 500
radius = 250

print(datetime.now().strftime("%H:%M:%S"))
print("loading noise data")

def noise(x, y, z, i):
    chunk_size = 100
    chunk_i = math.floor(x/chunk_size) + math.floor(y/chunk_size) + math.floor(z/chunk_size)
    with open(f'../noise/noise{i+1}/{chunk_i + z%chunk_size}.pickle', 'rb') as f:
        noise_data = pickle.load(f)

    return noise_data[x%chunk_size][y%chunk_size]

def parallelize_dataframe(df, func, n_cores=6):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

# normalizing range values
update_range = lambda val, old_min, old_max, new_min, new_max: (((val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

biome_color = {
    'ocean': '134074',
    'tundra': '669bbc',
    'boreal forest': '4f772d',
    'grassland': '90a955',
    'temperate rainforest': '31572c',
    'seasonal forest': '606c38',
    'woodland': '283618',
    'tropical rainforest': '132a13',
    'savanna': 'bb9457',
    'desert': 'bb9457',
    'beach': 'e9c46a'
}

def asCartesian(rthetaphi):
    # convert from pixel height to polar coordinate
    theta = rthetaphi[1]
    phi = rthetaphi[2]
    r = rthetaphi[0]

    x = r * math.sin( theta ) * math.cos( phi )
    y = r * math.sin( theta ) * math.sin( phi )
    z = r * math.cos( theta )
    
    x = update_range(x, -math.pi, math.pi, 0, size_x)
    y = update_range(y, -math.pi, math.pi, 0, size_x)
    z = update_range(z, -math.pi, math.pi, 0, size_x)

    return [int(x),int(y),int(z)]

# get closeness to equator
def equator_temp(x: int) -> float:
    """needs to consider negative temps"""
    equator = size_x / 2
    percent = x / equator if x < equator else (size_x - x)/equator
    category = percent * 10
    bonus = category * 3
    return -15 + bonus

def add_beach(biome: str, height: float) -> str:
    if 'forest' in biome and height < 150:
        return 'beach'
    
    return biome

def get_biome(is_land: bool, temperature: float, precipitation: float) -> str:
    # https://upload.wikimedia.org/wikipedia/commons/6/68/Climate_influence_on_terrestrial_biome.svg
    if not is_land:
        return 'ocean'
    
    if temperature < 0:
        return 'tundra'
    
    if temperature < 10 and precipitation > 50:
        return 'boreal forest'
    
    if temperature < 10:
        return 'grassland'

    if temperature < 20 and precipitation > 200:
        return 'temperate rainforest'
    
    if temperature < 20 and precipitation > 100:
        return 'seasonal forest'
    
    if temperature < 20 and precipitation > 50:
        return 'woodland'
    
    if temperature < 20:
        return 'grassland'
    
    if precipitation > 250:
        return 'tropical rainforest'
    
    if precipitation > 50:
        return 'savanna'
    
    return 'desert'

def init_df() -> pd.DataFrame:
    df = pd.DataFrame(
        columns = [
            'x', 
            'y',
            'height',
            'precipitation',
            'temperature',
            'is_land',
            'biome',
            'color'
        ]
    )

    # initialize cells
    print('initializing')
    df['x'] = pd.Series([i for i in range(size_x) for _ in range(size_y)])
    df['y'] = pd.Series([i for _ in range(size_x) for i in range(size_y)])
    return df

def add_3d_coords(df: pd.DataFrame) -> pd.DataFrame:

    print(datetime.now().strftime("%H:%M:%S"))
    print('adding 3D cartesian coordinates')

    df['lat'] = df.apply(lambda row: update_range(row['x'], 0, size_x, 0, math.pi), axis=1)
    df['long'] = df.apply(lambda row: update_range(row['y'], 0, size_x, 0, math.pi * 2), axis=1)
    df['3D'] = df.apply(lambda row: asCartesian([1, row['lat'], row['long']]), axis=1)
    return df

def add_height_noise(df: pd.DataFrame) -> pd.DataFrame:
    # add noise
    print(datetime.now().strftime("%H:%M:%S"))
    print('adding height noise')
    df['height'] = df.apply(lambda row: noise(*row['3D'], i=0), axis=1)
    return df

def add_precipitation_noise(df: pd.DataFrame) -> pd.DataFrame:
    print(datetime.now().strftime("%H:%M:%S"))
    print('adding precipitation noise')
    df['precipitation'] = df.apply(lambda row: noise(*row['3D'], i=1), axis=1)
    return df

def add_temperature_noise(df: pd.DataFrame) -> pd.DataFrame:
    print(datetime.now().strftime("%H:%M:%S"))
    print('adding temperature noise')
    df['temperature'] = df.apply(lambda row: noise(*row['3D'], i=2), axis=1)
    return df

def other_processing(df: pd.DataFrame) -> pd.DataFrame:
    print(datetime.now().strftime("%H:%M:%S"))
    print('normalizing ranges')
    df['height'] = df.apply(lambda row: update_range(row['height'], 0.35, 0.65, -11000, 9000), axis=1)
    df['precipitation'] = df.apply(lambda row: update_range(row['precipitation'], 0.35, 0.65, 0, 500), axis=1)
    df['temperature'] = df.apply(lambda row: update_range(row['temperature'], 0.35, 0.65, -10, 30), axis=1)
    
    print(datetime.now().strftime("%H:%M:%S"))
    print('checking the temperature')
    # update temperature based on latitude
    df['temperature'] = df.apply(lambda row: row['temperature'] + equator_temp(row['x']), axis=1)
    # update temperature based on height
    df['temperature'] = df.apply(lambda row: row['temperature'] - row['height']/2000, axis=1)

    # set is_land
    print(datetime.now().strftime("%H:%M:%S"))
    print('finding land')
    df['is_land'] = df.apply(lambda row: row['height'] > 0, axis=1)

    # set biome
    print(datetime.now().strftime("%H:%M:%S"))
    print('setting biome')
    df["biome"] = df.apply(lambda row: get_biome(row['is_land'], row['temperature'], row['precipitation']), axis=1)

    # add beaches
    print(datetime.now().strftime("%H:%M:%S"))
    print('going to the beach')
    df['biome'] = df.apply(lambda row: add_beach(row['biome'], row['height']), axis=1)

    # set color
    print(datetime.now().strftime("%H:%M:%S"))
    print('setting color')
    df["color"] = df.apply(lambda row: biome_color[row['biome']], axis=1)

    # save
    print(datetime.now().strftime("%H:%M:%S"))
    return df

def run():
    # df = init_df()
    # df = add_3d_coords(df)
    # df.to_pickle('tmp.pickle')

    # df = add_height_noise(df)
    # df.to_pickle('tmp2.pickle')
    # df = add_precipitation_noise(df)
    # df.to_pickle('tmp3.pickle')
    # df = add_temperature_noise(df)
    # df.to_pickle('tmp4.pickle')

    df = pd.read_pickle('tmp4.pickle')
    df = other_processing(df)
    df.to_pickle('biomes.pickle')

    # output results
    df_out = df.drop(['color', '3D', 'x', 'y'], axis=1)
    df_out.to_json('biomes.json', orient='table', index=False)
    
    return df

def write_map(df):
    print('writing image')
    image_data = [[[13,40,74] for _ in range(size_x)] for _ in range(size_y)]
    for _, row in df.iterrows():
        image_data[row['x']][row['y']] = [
            int('0x' + row['color'][0:2], 16),
            int('0x' + row['color'][2:4], 16),
            int('0x' + row['color'][4:6], 16)
        ]

    # write the results to an image
    np_data = np.array(image_data)
    im = Image.fromarray(np_data.astype(np.uint8))
    im.save("./render/client/textures/grid100.jpg")
    print(datetime.now().strftime("%H:%M:%S"))

    print('scaling image')
    img = cv2.imread("./render/client/textures/grid100.jpg", 1)
    ratio = 512/size_x
    large_image = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
    cv2.imwrite("./render/client/textures/grid512.jpg", large_image)


df = run()
# df = pd.read_pickle('biomes.pickle')
write_map(df)
