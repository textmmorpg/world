from PIL import Image
import numpy as np
from random import random
from perlin_noise import PerlinNoise
import pandas as pd
import matplotlib.pyplot as plt

size_x, size_y = 512, 512
height_noise = PerlinNoise(octaves=6)
temperature_noise = PerlinNoise(octaves=6)
precipitation_noise = PerlinNoise(octaves=6)

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

    # normalizing range values
    update_range = lambda val, old_min, old_max, new_min, new_max: (((val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

    print('normalizing ranges')
    df['height'] = df.apply(lambda row: update_range(row['height'], -0.7, 0.7, -11000, 9000), axis=1)
    df['precipitation'] = df.apply(lambda row: update_range(row['precipitation'], -0.7, 0.7, 0, 500), axis=1)
    df['temperature'] = df.apply(lambda row: update_range(row['temperature'], -0.7, 0.7, -10, 30), axis=1)

    # set is_land
    print('setting is_land')
    df['is_land'] = df.apply(lambda row: row['height'] > 0, axis=1)

    # save
    df.to_pickle('world_data.pickle')
    return df

# df = init_df()
df = pd.read_pickle('world_data.pickle')
df["biome"] = df.apply(lambda row: get_biome(row['is_land'], row['temperature'], row['precipitation']), axis=1)

print(df[df['is_land']].biome.value_counts())
plt.show()

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

# write the results to an image
# np_data = np.array(height_map)
# im = Image.fromarray(np_data.astype(np.uint8))
# im.save("./render/client/images/grid512.jpg")
