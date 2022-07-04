from PIL import Image
import numpy as np
from random import random

data = []
for x in range(512):
    data.append([])
    for y in range(512):
        data[x].append([])
        data[x][y] = [random()*256,random()*256,random()*256]

np_data = np.array(data)

im = Image.fromarray(np_data.astype(np.uint8))
im.save("./render/client/images/grid512.jpg")
