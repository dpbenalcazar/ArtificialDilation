from PIL import Image
import PySimpleGUI as sg
import imutils.paths as pth
from change_dilation import change_dilation

class gui_demo(object):
    def __init__(self, files):
        self.files = files
        layout = [
            [sg.Text("Image:"),
             sg.OptionMenu(files, default_value=files[1],size=(35, 1),key="-opt-"),
             sg.Button("Apply",  key="-btn-",size=(10, 1))],
            [sg.Text(" ")],
            [sg.Image(filename="../samples/LVL.png", key="-img-")],
            [sg.Text(" ")],
            [sg.Text("Dilation Ratio Rp/Ri:")],
            [sg.Slider(range=(0.1, 0.9),resolution=0.01,size=(60, 15),orientation='h',key="-bar-",enable_events=True)]
        ]
        # Create the window
        self.window = sg.Window("Artificial Dilation", layout, margins=(20, 20), use_default_focus=False)
        self.window.Finalize()

    def update_image(self, image_name):
        self.window["-img-"].update(filename="../samples/"+image_name)
        return

    def update_dilation(self, dil):
        return

    def run(self):

        # Create an event loop
        while True:
            event, values = self.window.read()
            if event == "-btn-":
                image_name = values["-opt-"]
                self.update_image(image_name)
            elif event == "-bar-":
                dil = values["-opt-"]
                self.update_dilation(dil)
            elif event == sg.WIN_CLOSED:
                break

        self.window.close()
        return

if __name__ == '__main__':
    files = sorted([*pth.list_images('../samples')])
    files = [path.split('/')[-1] for path in files]
    gui = gui_demo(files)
    gui.run()
