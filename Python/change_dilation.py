import numpy as np
from PIL import Image

def change_dilation(im1, dil, pupil_xyr, iris_xyr):
    # Get input shape:
    im1 = np.array(im1)
    shape = im1.shape
    if len(shape) == 2:
        im1 = np.expand_dims(im1, 2)
    N, M, chanels = im1.shape

    # Get color of central pixel:
    if chanels == 3:
        Rpup = im1[int(pupil_xyr[0]), int(pupil_xyr[1]) ,0]
        Gpup = im1[int(pupil_xyr[0]), int(pupil_xyr[1]) ,1]
        Bpup = im1[int(pupil_xyr[0]), int(pupil_xyr[1]) ,2]
        col = np.array([Rpup, Gpup, Bpup])
    else:
        col = im1[int(pupil_xyr[0]), int(pupil_xyr[1])]

    # Get original pupuil and iris radii:
    rp1 = pupil_xyr[2]
    ri = iris_xyr[2]

    # Compute output pupil radius:
    rp2 = dil*ri

    # Slope for lineal transformation:
    m = (ri-rp1)/(ri-rp2)

    # Create putput image:
    im2 = np.zeros((N, M, chanels), dtype=np.uint8)

    # Change dlation level
    for u in range(M):
        for v in range(N):
            xp = u - pupil_xyr[0]
            yp = v - pupil_xyr[1]
            r_aux = xp**2 + yp**2;
            if r_aux <= ri**2 and r_aux >= rp2**2:
                rp = np.sqrt(r_aux)
                th = np.arctan2(yp,xp)
                r = m*(rp-rp2) + rp1
                x = int(r*np.cos(th) + pupil_xyr[0])
                y = int(r*np.sin(th) + pupil_xyr[1])
            elif r_aux < rp2**2:
                rp = np.sqrt(r_aux)
                th = np.arctan2(yp,xp)
                r = rp1*rp/rp2
                x = int(r*np.cos(th)+pupil_xyr[0])
                y = int(r*np.sin(th)+pupil_xyr[1])
            else:
                x = u
                y = v
                r = 2
            if r>0:
                im2[v,u,:] = im1[y,x,:]
            else:
                im2[v,u,:] = col

    return Image.fromarray(im2)
    
