import numpy as np
from PIL import Image, ImageDraw

def change_dilation(im1, dil, pupil_xyr, iris_xyr):
    # Get input shape:
    im1 = np.array(im1)
    shape = im1.shape
    if len(shape) == 2:
        im1 = np.expand_dims(im1, 2)
    N, M, chanels = im1.shape

    # Get original pupuil and iris radii:
    rp1 = pupil_xyr[2]
    ri = iris_xyr[2]

    # Compute output pupil radius:
    rp2 = dil*ri

    # Slope for lineal transformation:
    m = (ri-rp1)/(ri-rp2)

    # Create putput image:
    im2 = im1.copy()

    # Pupil mask
    pupil_mask = Image.new('L', (M, N), (0))
    draw = ImageDraw.Draw(pupil_mask)
    xp = pupil_xyr[0]
    yp = pupil_xyr[1]
    rp = 0.97*rp2
    draw.ellipse((xp-rp, yp-rp, xp+rp, xp+rp), fill=(255), outline=(0))
    pupil_mask = np.array(pupil_mask) > 0

    # Iris mask
    iris_mask = Image.new('L', (M, N), (0))
    draw = ImageDraw.Draw(iris_mask)
    draw.ellipse((xp-ri, yp-ri, xp+ri, xp+ri), fill=(255), outline=(0))
    iris_mask = np.array(iris_mask) > 0
    iris_mask[pupil_mask] = 0

    # Sample pixels in the iris
    V, U = np.where(iris_mask)
    for u, v in zip(U, V):
        xp = u - pupil_xyr[0]
        yp = v - pupil_xyr[1]
        rp = np.sqrt(xp**2 + yp**2)
        th = np.arctan2(yp,xp)
        r = m*(rp-rp2) + rp1
        x = int(r*np.cos(th) + pupil_xyr[0])
        y = int(r*np.sin(th) + pupil_xyr[1])
        im2[v,u,:] = im1[y,x,:]

    # Sample pixels in the pupil
    V, U = np.where(pupil_mask)
    for u, v in zip(U, V):
        xp = u - pupil_xyr[0]
        yp = v - pupil_xyr[1]
        rp = np.sqrt(xp**2 + yp**2)
        th = np.arctan2(yp,xp)
        r = rp1*rp/rp2
        x = int(r*np.cos(th)+pupil_xyr[0])
        y = int(r*np.sin(th)+pupil_xyr[1])
        im2[v,u,:] = im1[y,x,:]

    # Squeeze extra dimension if grayscale
    if chanels == 1:
        im2 = np.squeeze(im2, axis=2)

    return Image.fromarray(im2)
