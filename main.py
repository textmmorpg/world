from PIL import Image
import numpy as np
from random import random
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

xpix, ypix = 512, 512

min = 1
data = []
for x in range(xpix):
    data.append([])
    for y in range(ypix):
        data[x].append([])
        val = 0.5 * noise1([x/xpix, y/ypix])
        val += 0.25 * noise2([x/xpix, y/ypix])
        val += 0.125 * noise3([x/xpix, y/ypix])
        val += 0.125 * noise4([x/xpix, y/ypix])
        val += 0.3

        if val < min:
            min = val
        print(min)

        data[x][y] = [
            val*256,val*256,val*256
        ]

np_data = np.array(data)
im = Image.fromarray(np_data.astype(np.uint8))
im.save("./render/client/images/grid512.jpg")
