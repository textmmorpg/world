from PIL import Image
import numpy as np
from random import random
from perlin_noise import PerlinNoise
import pandas as pd
import matplotlib.pyplot as plt

size_x, size_y = 512, 512
height_noise = PerlinNoise(octaves=3)
temperature_noise = PerlinNoise(octaves=6)
precipitation_noise = PerlinNoise(octaves=6)

def make_df() -> pd.DataFrame:
    df = pd.DataFrame(
        columns = [
            'x', 
            'y',
            'height',
            'precipitation',
            'temperature',
            'is_land',
            'biome',
        ]
    )

    # initialize cells
    print('initializing')
    df['x'] = pd.Series([i for i in range(size_x) for _ in range(size_y)])
    df['y'] = pd.Series([i for _ in range(size_x) for i in range(size_y)])

    # add noise
    print('adding height noise')
    df['height'] = df.apply(lambda row: height_noise([row['x']/size_x, row['y']/size_y]), axis=1)
    print('adding precipitation noise')
    df['precipitation'] = df.apply(lambda row: temperature_noise([row['x']/size_x, row['y']/size_y]), axis=1)
    print('adding temperature noise')
    df['temperature'] = df.apply(lambda row: precipitation_noise([row['x']/size_x, row['y']/size_y]), axis=1)

    # set is_land
    print('setting is_land')
    df['is_land'] = df.apply(lambda row: row['height'] > 0.8, axis=1)

    # save
    df.to_pickle('world_data.pickle')
    return df

df = pd.read_pickle('world_data.pickle')
df.hist(bins=10)
plt.show()

# def get_biome(temperature: float, precipitation: float) -> str:
#     pass

# def add_noise(df: pd.DataFrame) -> pd.DataFrame:
#     """Initialize 2D array of perlin noise for each cell"""
#     for x in range(xpix):
#         for y in range(ypix):

#             height = height_noise([x/xpix, y/ypix])
#             precipitation = precipitation_noise([x/xpix, y/ypix])
#             temperature = temperature_noise([x/xpix, y/ypix])

#             df.append({
#                 'x': x,
#                 'y': y,
#                 'height': height,
#                 'precipitation': precipitation, 
#                 'temperature': temperature,
#                 'is_land': height > 0.08,
#                 'biome': get_biome(temperature, precipitation)
#             }, ignore_index=True)
    
#     return df

# df = add_noise(df)
# df.read_pickle('world_data.pickle')
# df['height', 'precipitation', 'temperature'].hist(bins=10)

# def colorHex(value):
#     """Get a color based on height"""
#     if value < 0:
#         return ['03', '00', '7B'] # deep water
#     elif value < 0.075:
#         return ['66', '63', 'FF'] # shallow water
#     elif value < 0.08:
#         return ['BF', 'BA', '07'] # beach
#     elif value < 0.125:
#         return ['07', 'A8', '04'] # field
#     elif value < 0.175:
#         return ['0B', '5B', '02'] # forest
#     elif value < 0.2:
#         return ['78', '7A', '6B'] # stone
#     else:
#         return ['F8', 'F8', 'F8'] # snowwy mountain top

# Graph perlin noise values to get an idea of the distribution
# plt.hist(noise_vals, bins=20, histtype = 'bar', facecolor = 'blue')
# plt.show()

# write the results to an image
# np_data = np.array(height_map)
# im = Image.fromarray(np_data.astype(np.uint8))
# im.save("./render/client/images/grid512.jpg")
