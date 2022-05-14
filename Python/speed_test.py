import time
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm

from change_dilation_v2 import change_dilation

# Open input image
im1 = Image.open('../samples/S1008R02.png')

# Read segmentation data
df = pd.read_csv('../samples/segm.csv')
files = list(df["ID"])
data = df.drop(columns=['ID']).to_numpy()

# Select segmentation data
pupil_xyr = data[2, 0:3]
iris_xyr  = data[2, 3:6]

# Input dilation
dil1 = pupil_xyr[2]/iris_xyr[2]

# Output set of 100 dilation levels
dil2_set = np.linspace(0.1, 0.8, 100)

# Measure time for 100 images
t0 = time.time()
for dil2 in tqdm(dil2_set):
    im2 = change_dilation(im1, dil2, pupil_xyr, iris_xyr)
dt = time.time()-t0

# Print results
print('\nTest results: ')
print('  -- Image size: {}'.format(im1.size))
print('  -- Time for 100 predictions: {:0.3f} s'.format(dt))
print('  -- Average time per image: {:0.3f} ms'.format(10*dt))
print('  -- Speed: {:0.1f} images per second'.format(100/dt))
