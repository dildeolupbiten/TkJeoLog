# -*- coding: utf-8 -*-

from .modules import tk, open_new


class About(tk.Toplevel):
    def __init__(self, language: dict, selected: str):
        super().__init__()
        self.resizable(width=False, height=False)
        self.language = language
        self.selected = selected
        self.version = "1.0.1"
        self.name = "TkJeoLog"
        self.build_date = "08.06.2020"
        self.update_date = "23.10.2020"
        self.developed_by = "Tanberk Celalettin Kutlu"
        self.contact = "tckutlu@gmail.com"
        self.top_frame = tk.Frame(
            master=self,
            bd="2",
            relief="groove"
        )
        self.top_frame.pack(fill="both")
        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.pack(fill="both")
        self.title = tk.Label(
            master=self.top_frame,
            text=self.name,
            font="Arial 25"
        )
        self.title.pack()
        for index, i in enumerate([134, 135, 152, 136, 137]):
            label = tk.Label(
                master=self.bottom_frame,
                text=self.language[f"{i}"][self.selected],
                font="Arial 12",
                fg="red"
            )
            label.grid(row=index, column=0, sticky="w")
            double_dot = tk.Label(
                master=self.bottom_frame,
                text=":",
                font="Arial 12",
                fg="red"
            )
            double_dot.grid(row=index, column=1, sticky="w")
        for i, j in enumerate(
                (
                    self.version,
                    self.build_date,
                    self.update_date,
                    self.developed_by,
                    self.contact
                )
        ):
            if j == self.contact:
                info = tk.Label(
                    master=self.bottom_frame,
                    text=j,
                    font="Arial 12",
                    fg="blue",
                    cursor="hand2"
                )
                url2 = "mailto://tckutlu@gmail.com"
                info.bind(
                    "<Button-1>",
                    lambda event: open_new(url2))
            else:
                info = tk.Label(
                    master=self.bottom_frame,
                    text=j,
                    font="Arial 12"
                )
            info.grid(row=i, column=2, sticky="w")
        desc = tk.Label(
            master=self,
            text=self.language["138"][self.selected],
            font="Arial 10 italic"
        )
        desc.pack()
