import numpy as np
from PIL import Image, ImageDraw

def change_dilation(im1, dil, pupil_xyr, iris_xyr):
    # Get input shape:
    im1 = np.array(im1)
    shape = im1.shape
    if len(shape) == 2:
        im1 = np.expand_dims(im1, 2)
    M, N, chanels = im1.shape

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
    pupil_mask = Image.new('L', (N, M), (0))
    draw = ImageDraw.Draw(pupil_mask)
    xp = pupil_xyr[0]
    yp = pupil_xyr[1]
    rp = 0.97*rp2
    draw.ellipse((xp-rp, yp-rp, xp+rp, yp+rp), fill=(255), outline=(0))
    #draw.ellipse((yp-rp, xp-rp, yp+rp, xp+rp), fill=(255), outline=(0))
    pupil_mask = np.array(pupil_mask) > 0

    # Iris mask
    iris_mask = Image.new('L', (N, M), (0))
    draw = ImageDraw.Draw(iris_mask)
    draw.ellipse((xp-ri, yp-ri, xp+ri, yp+ri), fill=(255), outline=(0))
    #draw.ellipse((yp-ri, xp-ri, yp+ri, xp+ri), fill=(255), outline=(0))
    iris_mask = np.array(iris_mask) > 0
    iris_mask[pupil_mask] = 0

    # Sample pixels in the iris
    v, u = np.where(iris_mask)
    xp = u - pupil_xyr[0]
    yp = v - pupil_xyr[1]
    rp = np.sqrt(xp**2 + yp**2)
    th = np.arctan2(yp,xp)
    r = m*(rp-rp2) + rp1
    x = (r*np.cos(th) + pupil_xyr[0]).astype(np.int32)
    y = (r*np.sin(th) + pupil_xyr[1]).astype(np.int32)
    im2[v,u,:] = im1[y,x,:]

    # Sample pixels in the pupil
    v, u = np.where(pupil_mask)
    xp = u - pupil_xyr[0]
    yp = v - pupil_xyr[1]
    rp = np.sqrt(xp**2 + yp**2)
    th = np.arctan2(yp,xp)
    r = rp1*rp/rp2
    x = (r*np.cos(th)+pupil_xyr[0]).astype(np.int32)
    y = (r*np.sin(th)+pupil_xyr[1]).astype(np.int32)
    im2[v,u,:] = im1[y,x,:]

    # Squeeze extra dimension if grayscale
    if chanels == 1:
        im2 = np.squeeze(im2, axis=2)

    return Image.fromarray(im2)
