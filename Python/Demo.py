import PySimpleGUI as sg
import imutils.paths as pth
from PIL import ImageTk, Image
from change_dilation import change_dilation

class gui_demo(object):
    def __init__(self, folder, files):
        self.folder = folder
        self.files = files
        self.pupil_xyr = [200.0, 200.0, 51.0]
        self.iris_xyr = [196.0, 210.0, 181.0]
        layout = [
            [sg.Text("Image:"),
             sg.OptionMenu(files, default_value=files[1],size=(35, 1),key="-opt-"),
             sg.Button("Apply",  key="-btn-",size=(10, 1))],
            [sg.Text(" ")],
            [sg.Image(filename=self.folder+self.files[1], key="-img-")],
            [sg.Text(" ")],
            [sg.Text("Dilation Ratio Rp/Ri:")],
            [sg.Slider(range=(0.1, 0.9), resolution=0.01, tick_interval = 0.1, 
             size=(60, 15), orientation='h',
             key="-bar-", enable_events=True)]
        ]
        # Create the window
        self.window = sg.Window("Artificial Dilation", layout, margins=(20, 20), use_default_focus=False)
        self.window.Finalize()
        self.update_image(self.files[1])

    def convert(self, image):
        image = image.resize(self.size)
        return ImageTk.PhotoImage(image=image)

    def update_image(self, image_name):
        # Update Image
        filename = self.folder + image_name
        self.im1 = Image.open(filename)
        self.window["-img-"].update(filename)
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
            if event == "-btn-":
                image_name = values["-opt-"]
                self.update_image(image_name)
            elif event == "-bar-":
                dil = values["-bar-"]
                self.update_dilation(dil)
            elif event == sg.WIN_CLOSED:
                break

        self.window.close()
        return

if __name__ == '__main__':
    folder = '../samples/'
    files = sorted([*pth.list_images(folder)])
    files = [path.split('/')[-1] for path in files]
    gui = gui_demo(folder, files)
    gui.run()
