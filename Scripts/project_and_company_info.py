# -*- coding: utf-8 -*-

from .modules import tk
from .utilities import translate


class ProjectAndCompanyInfo(tk.Toplevel):
    def __init__(
            self,
            icons: dict,
            language: dict,
            data: dict,
            texts: list,
            title: str,
            selected: str,
            wait: bool = True
    ):
        super().__init__()
        self.resizable(width=False, height=False)
        self.title(title)
        self.language = language
        self.selected = selected
        self.widgets = self.create_entries(texts=texts)
        if data:
            self.data = data
            for k, v in self.widgets.items():
                v.insert("insert", data[translate(self, k)])
        else:
            self.data = {}
        self.button = tk.Button(
            master=self,
            image=icons["ok"]["img"],
            command=self.get_data,
            activebackground=self["bg"],
            borderwidth=0,
            highlightthickness=0
        )
        self.button.pack()
        if wait:
            self.wait_window()
        else:
            self.button.invoke()

    def create_entries(self, texts: list):
        widgets = {}
        frame = tk.Frame(master=self)
        frame.pack()
        for i, j in enumerate(texts):
            label = tk.Label(master=frame, text=j, font="Arial 11 bold")
            label.grid(row=i, column=0, sticky="w")
            entry = tk.Entry(master=frame, width=50)
            entry.grid(row=i, column=1, sticky="w")
            widgets[j] = entry
        return widgets

    def get_data(self):
        self.data = {k: v.get() for k, v in self.widgets.items()}
        self.destroy()
