# -*- coding: utf-8 -*-

from .menu import Menu
from .modules import tk


class Frame(tk.Frame):
    def __init__(self, side: str = "top", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=side, expand=True, fill="both")


class MainWindow(Frame):
    def __init__(
            self,
            language: dict,
            icons: dict,
            images: dict,
            *args, 
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.menu = Menu(
            master=self.master,
            language=language,
            icons=icons,
            images=images,
            main_window=self,
            frame=Frame
        )
