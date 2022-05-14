# Artificial Dilation
This is the repository for the research work: Artificial Pupil Dilation for Data Augmentation in Iris Semantic Segmentation (pending publication)

Our method artificially changes the dilation level of an iris image to any desired level. The dilation level is defined as the ratio between the pupil radius and the iris radius. This method is based on deterministic equations and sampling techniques so it does not requires any training.

The following image illustrates the effects of our data augmentation function. Given the image on the left and its circular segmentation data, the other two images were synthesized. One with a reduced dilation and the other with an increase in dilation.  

![alt text](./assets/Figure1.png?raw=true)

This repository contains two implementations of the artificial-dilation data-augmentation function. One in Python and one in Matlab. Both contain the basic version of the function, as well as interactive GUI demos.

## Python Implementation
### Libraries
The python implementation of the function utilizes only numpy and pillow Image to work.

For the demos and tests, these additional libraries are needed: tqdm, pandas, PySimpleGUI and jupyter notebook.

### Usage
The following python command synthesizes im2 with dilation level dil2 (between 0.1 and 0.8), from im1 with dilation level dil1.

```python
im2 = change_dilation(im1, dil2, pupil_xyr, iris_xyr)
```

The arguments pupil_xyr is the circular segmentation of the pupil in im1, with the format: (xp, yp, rp). Where (xp,yp) is the center of the circle that best fits the pupil and rp is the pupil radius. Likewise, iris_xyr is the circular segmentation of the iris, with the format: (xi, yi, ri).

## Marlab Implementation
