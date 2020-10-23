# -*- coding: utf-8 -*-

from .modules import os, tk
from .messagebox import MsgBox
from .utilities import translate
from .spinbox import SpinboxFrame


class UDInfo(tk.Toplevel):
    def __init__(
            self,
            icons: dict,
            language: dict,
            data: dict,
            texts: list,
            title: str,
            selected: str,
            depth: int,
            wait: bool = True
    ):
        super().__init__()
        if os.name == "posix":
            self.geometry("312x400")
        else:
            self.geometry("350x400")
        self.resizable(width=False, height=False)
        self.icons = icons
        self.language = language
        self.selected = selected
        self.texts = texts
        self.title(title)
        self.depth = depth
        self.top_button_frame = tk.Frame(master=self)
        self.top_button_frame.pack()
        self.add_button = tk.Button(
            master=self.top_button_frame,
            image=self.icons["add"]["img"],
            command=self.add_entry,
            activebackground=self["bg"],
            borderwidth=0,
            highlightthickness=0
        )
        self.add_button.pack(side="left")
        self.remove_button = tk.Button(
            master=self.top_button_frame,
            image=self.icons["remove"]["img"],
            command=self.remove_entry,
            activebackground=self["bg"],
            borderwidth=0,
            highlightthickness=0
        )
        self.remove_button.pack(side="left")
        self.frame = tk.Frame(master=self)
        self.frame.pack(expand=True, fill="both")
        self.y_scrollbar = tk.Scrollbar(
            master=self.frame,
            orient="vertical"
        )
        self.canvas = tk.Canvas(master=self.frame)
        self.canvas_frame = tk.Frame(master=self.canvas)
        self.y_scrollbar.configure(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(expand=True, fill="both", padx=20)
        self.canvas.create_window(
            (4, 4),
            window=self.canvas_frame,
            anchor="nw"
        )
        self.canvas_frame.bind(
            sequence="<Configure>",
            func=lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.row_order = {}
        self.frames = self.create_labels()
        self.variables = []
        if data:
            self.data = data
            for i in range(len(data)):
                self.add_entry()
                for index, text in enumerate(self.texts):
                    widget = self.frames[index].winfo_children()[1:][i]
                    value = data[str(i)][
                        translate(self=self, string=text)
                    ]
                    widget.var.set(value)
        else:
            self.data = {}
        self.ok_button = tk.Button(
            master=self,
            image=self.icons["ok"]["img"],
            command=self.ok_command,
            activebackground=self["bg"],
            borderwidth=0,
            highlightthickness=0
        )
        self.ok_button.pack()
        if wait:
            self.wait_window()
        else:
            self.ok_button.invoke()

    def add_entry(self):
        row = len(self.frames[0].winfo_children())
        self.row_order[row] = []
        for index, text in enumerate(self.texts):
            if index in [0, 1]:
                spinbox = SpinboxFrame(
                    master=self.frames[index],
                    icons=self.icons,
                    language=self.language,
                    selected=self.selected,
                    start=0,
                    end=10000,
                    width=12,
                    step=0.5,
                    data="",
                    grid=True
                )
                spinbox.grid(row=row, column=0)
                self.row_order[row].append(spinbox)
                if index == 0:
                    upper = self.frames[index].winfo_children()
                    if len(upper) >= 3:
                        lower = self.frames[index + 1].winfo_children()
                        previous = lower[len(lower) - 1].var.get()
                        upper[len(upper) - 1].var.set(previous)
        self.canvas.yview_moveto(self.canvas.canvasy(self.canvas.winfo_y()))

    def remove_entry(self):
        try:
            last_row = [*self.row_order.keys()][-1]
        except IndexError:
            return
        if last_row == 0:
            return
        for i in self.row_order[last_row]:
            i.destroy()
        self.row_order.pop(last_row)

    def create_labels(self):
        frames = {}
        self.row_order[0] = []
        for index, text in enumerate(self.texts):
            frame = tk.Frame(
                master=self.canvas_frame,
                bd=1,
                relief="sunken",
                width=15
            )
            frame.grid(row=0, column=index)
            label = tk.Label(
                master=frame,
                text=text,
                font="Arial 11 bold",
                width=15,
            )
            label.grid(row=0, column=0, sticky="nsew")
            frames[index] = frame
            self.row_order[0].append(frames)
        return frames

    def ok_command(self):
        self.data = {}
        invalid_value = False
        upper_greater_than_lower = False
        lower_greater_than_depth = False
        order = {k: v for k, v in self.row_order.items() if k != 0}
        for index, (k, v) in enumerate(order.items()):
            self.data[str(index)] = {}
            for i in range(2):
                try:
                    self.data[str(index)][
                        self.language[f"{91 + i}"][self.selected]
                    ] = float(v[i].var.get())
                except tk.TclError:
                    invalid_value = True
            upper = self.data[str(index)][self.language["91"][self.selected]]
            lower = self.data[str(index)][self.language["92"][self.selected]]
            if lower <= upper:
                upper_greater_than_lower = True
                v[1].spinbox.configure(background="red")
                self.data[str(index)] = {}
            else:
                upper_greater_than_lower = False
            if lower > self.depth:
                lower_greater_than_depth = True
                self.data[str(index)] = {}
                v[1].spinbox.configure(background="red")
        if invalid_value:
            MsgBox(
                title=self.language["81"][self.selected],
                message=self.language["101"][self.selected],
                level="warning",
                icons=self.icons
            )
        elif upper_greater_than_lower:
            MsgBox(
                title=self.language["81"][self.selected],
                message=self.language["102"][self.selected],
                level="warning",
                icons=self.icons
            )
        elif lower_greater_than_depth:
            MsgBox(
                title=self.language["81"][self.selected],
                message=self.language["103"][self.selected],
                level="warning",
                icons=self.icons
            )
        else:
            self.destroy()
