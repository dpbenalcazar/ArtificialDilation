import cv2
import torch
import numpy as np
from PIL import Image, ImageDraw
from torch.utils.data import Dataset

def rand_between(self, min_value, max_value):
    """Generates a random number between 'min_value' and 'max_value'."""
    return (max_value-min_value)*np.random.rand() + min_value

def change_dilation(im1, dil, pupil_xyr, iris_xyr):
    """
    im2 = change_dilation(im1, dil, pupil_xyr, iris_xyr)
    generates image 'im2' with dilation level 'dil'
    from the input image 'im1' with circular segmentation
    data 'pupil_xyr' and 'iris_xyr'.
    """
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

class dilated_iris_dataset(Dataset):
    """Iris Dataset with change in dilation."""

    def __init__(self, segm_file, iris_paths, mask_paths, transform=None):
        """
        Args:
            segm_file : CSV file with segmentation data.
            iris_paths: Paths of iris images.
            mask_paths: Paths of segmentation masks.
            transform : Optional transform to be applied on iris images.
        """
        # Read Segmentation Data
        df = pd.read_csv(segm_file)
        data = df.drop(columns=['ID']).to_numpy()
        pupil_xyr = data[:, :3]
        iris_xyr = data[:, 3:]

        # Input Parameters
        self.pupil_xyr  = pupil_xyr
        self.iris_xyr   = iris_xyr
        self.iris_paths = iris_paths
        self.mask_paths = mask_paths
        self.transform  = transform

        # Albumentations
        self.aug = A.Compose([
            A.Affine(scale=(0.7,1.2), keep_ratio=True,
                    translate_percent=(-0.15, 0.15),
                    rotate=(0,15), cval=(128,128,128), p=0.8,
                    interpolation=cv2.INTER_LINEAR),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.ColorJitter(brightness=0.25, contrast=0.25,
                            saturation=0.1, hue=0.05, p=1),
            A.GaussianBlur(p=0.3),
            A.CLAHE(p=0.3),
            A.RandomRain(p=0.1),
            A.GlassBlur(p=0.1),
            A.MotionBlur(p=0.1)
        ])


    def __len__(self):
        return len(self.iris_paths)

    def __getitem__(self, idx):
        # Open images
        iris = Image.open(self.iris_paths[idx]).convert('RGB')
        mask = Image.open(self.mask_paths[idx]).convert('L')

        # Get segmentation circles
        pupil_xyr = self.pupil_xyr[idx]
        iris_xyr  = self.iris_xyr[idx]

        # Change Dilation
        dil = rand_between(0.2, 0.7)
        iris = change_dilation(iris, dil, pupil_xyr, iris_xyr)
        mask = change_dilation(mask, dil, pupil_xyr, iris_xyr)

        # Data Augmentation
        augmented = self.aug(image=np.array(iris), mask=np.array(mask))

        iris = Image.fromarray(augmented['image'])
        mask = augmented['mask']

        if self.transform:
            iris = self.transform(iris)
            mask = torch.from_numpy(mask).long()

        return iris, mask
