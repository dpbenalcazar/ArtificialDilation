import numpy as np
import pandas as pd
import PySimpleGUI as sg
from PIL import ImageTk, Image
from change_dilation_v2 import change_dilation

class gui_demo(object):
    def __init__(self, folder, files, data):
        self.folder = folder
        self.files = files
        self.data = data
        self.ind = 1
        self.pupil_xyr = self.data[self.ind, 0:3]
        self.iris_xyr  = self.data[self.ind, 3:6]
        layout = [
            [sg.Text("Image:"),
             sg.OptionMenu(files, default_value=self.files[self.ind],size=(35, 1),key="-opt-"),
             sg.Button("Apply",  key="-btn-",size=(10, 1))],
            [sg.Text(" ")],
            [sg.Image(filename=self.folder+self.files[self.ind], key="-img-")],
            [sg.Text(" ")],
            [sg.Text("Dilation Ratio Rp/Ri:")],
            [sg.Slider(range=(0.1, 0.9), resolution=0.01, tick_interval = 0.1,
             size=(60, 15), orientation='h',
             key="-bar-", enable_events=True)]
        ]
        # Create the window
        self.window = sg.Window("Artificial Dilation", layout, margins=(20, 20), use_default_focus=False)
        self.window.Finalize()
        self.update_image(self.files[self.ind])

    def convert(self, image):
        image = image.resize(self.size)
        return ImageTk.PhotoImage(image=image)

    def update_image(self, image_name):
        # Update Image
        filename = self.folder + image_name
        self.im1 = Image.open(filename)
        self.window["-img-"].update(filename)
        # Get dilation data
        self.ind = self.files.index(image_name)
        self.pupil_xyr = self.data[self.ind, 0:3]
        self.iris_xyr  = self.data[self.ind, 3:6]
        # Update slide bar
        dil = self.pupil_xyr[2]/self.iris_xyr[2]
        self.window["-bar-"].update(dil)
        return

    def update_dilation(self, dil):
        filename = "../assets/tmp.png"
        im2 = change_dilation(self.im1, dil, self.pupil_xyr, self.iris_xyr)
        im2.save(filename)
        self.window["-img-"].update(filename)
        return

    def run(self):
        # Create an event loop
        while True:
            event, values = self.window.read()

            # Apply buton was pressed
            if event == "-btn-":
                image_name = values["-opt-"]
                self.update_image(image_name)

            # Slid bar changed value
            elif event == "-bar-":
                dil = values["-bar-"]
                self.update_dilation(dil)

            # Window was closed
            elif event == sg.WIN_CLOSED:
                break

        self.window.close()
        return

if __name__ == '__main__':
    # Samples' folder
    folder = '../samples/'

    # Read segmentation data
    df = pd.read_csv(folder + 'segm.csv')
    files = list(df["ID"])
    data = df.drop(columns=['ID']).to_numpy()

    # Start demo GIU
    gui = gui_demo(folder, files, data)
    gui.run()
