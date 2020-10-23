# -*- coding: utf-8 -*-

from .modules import tk
from .frame import MainWindow
from .utilities import load_json, create_image_files, load_defaults


def main():
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("TkJeoLog")
    width = 610
    height = int(root.winfo_screenheight() * 0.8)
    images = {
        "Fine Grained": create_image_files(path="Images/Fine Grained"),
        "Coarse Grained": create_image_files(path="Images/Coarse Grained"),
        "Rock": create_image_files(path="Images/Rock")
    }
    icons = create_image_files(path="Icons")
    load_defaults()
    MainWindow(
        master=root,
        width=width,
        height=height,
        language=load_json(filename="Settings/language.json"),
        icons=icons,
        images=images
    )
    root.mainloop()
