# Artificial Dilation
This is the repository for the research work: Artificial Pupil Dilation for Data Augmentation in Iris Semantic Segmentation (pending publication)

Our method artificially changes the dilation level of an iris image to any desired level. The dilation level is defined as the ratio between the pupil radius and the iris radius. This method is based on deterministic equations and sampling techniques so it doesn't require any training.

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

The arguments pupil_xyr is the circular segmentation of the pupil in im1, with the format: (xp, yp, rp). Where (xp, yp) is the center of the circle that best fits the pupil and rp is the pupil radius. Likewise, iris_xyr is the circular segmentation of the iris, with the format: (xi, yi, ri).

The script speed_test.py evaluates the processing time of the function when synthesizing 100 images:

```bash
cd Python/
python speed_test.py
```

## Marlab Implementation
### Usage
The Matlab implementation requires Matlab's Image Processing Toolbox to work.

The command is identical to the python implementation with the same arguments.

```matlab
im2 = change_dilation(im1, dil2, pupil_xyr, iris_xyr);
```

### Manual Segmentation
You can segment your own images manually using the script: Matlab/Manual_Segmentation.m

Change the input and output paths to your own iris dataset, and run the program to start segmenting the pupil and iris of each image. Fist click with the mouse four points on the pupil/iris boundary and then click 4 other points in the iris/sclera boundary. Therefore, you must perform 8 consecutive clicks per image. Te program will compute the best fitting circles for the pupil and the iris, and display the results in a new figure. After that, the next image to be segmented will be automatically presented for you to click 8 more times. After the final image has been segmented, the program will save all segmentation data in a single CSV file.

## Demos
Interactive demos are offered with this repository, in which the user can change the dilation level of provided images using a slide bar.

![alt text](./assets/GUIs.png?raw=true)

The following command runs the python´s demo. Moving the slide bar will automatically generate a new iris image with the selected dilation level and display it. To switch images, first select the desired image with the scroll element on top and then press the Apply button.

```bash
cd Python/
python Demo.py
```

The Matlab demo was programmed as a Matlab App. First change directories to the folder named Matlab/ and then execute the following command. The slide bar will change the dilation level in real time, and the scrol element will switch automatically to the desired image.

```matlab
Demo.mlapp
```

## Cite
Publication pending ...
