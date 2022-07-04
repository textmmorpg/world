from PIL import Image
import numpy as np
from random import random
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

xpix, ypix = 512, 512

data = []
noise_vals = []

def colorHex(value):
    if value < 0:
        return ['03', '00', '7B'] # deep water
    elif value < 0.075:
        return ['66', '63', 'FF'] # shallow water
    else:
        value = value - 0.075 # make lowest value 0
        value *= 10 # between 0 and 1
        value *= 0.5 # reduce max val
        value *= 256 # convert to color range 0 to 256

        # return [str(hex(int(value))).replace('0x','')[:2], '00', '00']

    if value < 25:
        return ['BF', 'BA', '07'] # beach
    elif value < 115:
        return ['07', 'A8', '04'] # field
    elif value < 170:
        return ['0B', '5B', '02'] # forest
    elif value < 225:
        return ['78', '7A', '6B'] # stone
    else:
        return ['F8', 'F8', 'F8'] # snowwy mountain top


def add_noise(data):
    for x in range(xpix):
        data.append([])
        for y in range(ypix):
            data[x].append([])
            
            val = 0.5 * noise1([x/xpix, y/ypix])
            val += 0.25 * noise2([x/xpix, y/ypix])
            val += 0.125 * noise3([x/xpix, y/ypix])
            val += 0.125 * noise4([x/xpix, y/ypix])

            # noise_vals.append(val)
            color = colorHex(val)

            data[x][y] = [
                int('0x' + color[0], base=16),
                int('0x' + color[1], base=16),
                int('0x' + color[2], base=16),
            ]
    
    return data


data = add_noise(data)

# Generate perlin noise normal distributions
# plt.hist(noise_vals, bins=20, histtype = 'bar', facecolor = 'blue')
# plt.show()


np_data = np.array(data)
im = Image.fromarray(np_data.astype(np.uint8))
im.save("./render/client/images/grid512.jpg")
