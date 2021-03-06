# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .modules import os, tk, ttk
from .utilities import translate
from .spinbox import SpinboxFrame


class RCInfo(tk.Toplevel):
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
            self.geometry("1075x400")
        else:
            self.geometry("1065x400")
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
                    if text.startswith("N"):
                        try:
                            value = data[str(i)][text]
                        except KeyError:
                            value = ""
                    else:
                        try:
                            value = data[str(i)][
                                translate(self=self, string=text)
                            ]
                        except KeyError:
                            value = ""
                    if isinstance(widget, ttk.Combobox):
                        widget.configure(state="normal")
                        widget.delete("0", "end")
                        value = translate(
                            self=self,
                            string=value,
                            basic=True
                        )
                        widget.insert("insert", value)
                        widget.configure(state="readonly")
                    else:
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
            else:
                variable = tk.StringVar()
                if os.name == "posix" and index == 2:
                    w = 18
                else:
                    w = 16
                if index in [2, 3]:
                    values = ["", *range(0, 101)]
                elif index == 4:
                    values = ["", "< 1", "2 - 3", "4 - 11", "12 - 50", "> 50"]
                elif index == 5:
                    values = [""] + [f"W{i}" for i in range(1, 7)] \
                        + [f"W{i} - W{i + 1}" for i in range(1, 6)]
                else:
                    values = [""] + [f"R{i}" for i in range(0, 7)] \
                        + [f"R{i} - R{i + 1}" for i in range(0, 6)]
                self.variables.append(variable)
                ttk.Style().map(
                    f"{row}.{index}.TCombobox",
                    fieldbackground=[("readonly", "white")]
                )
                combobox = ttk.Combobox(
                    master=self.frames[index],
                    textvariable=variable,
                    values=values,
                    width=w,
                    height=100,
                    state="readonly",
                    style=f"{row}.{index}.TCombobox",
                    font="Default 10"
                )
                combobox.grid(row=row, column=0, pady=1)
                self.row_order[row].append(combobox)
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
            if os.name == "posix":
                if index in [0, 1]:
                    w = 15
                elif index == 2:
                    w = 20
                else:
                    w = 18
            else:
                w = 15
            frame = tk.Frame(
                master=self.canvas_frame,
                bd=1,
                relief="sunken",
                width=w
            )
            frame.grid(row=0, column=index)
            label = tk.Label(
                master=frame,
                text=text,
                font="Arial 11 bold",
                width=w,
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
            for i, j in enumerate(range(2, 7)):
                if j in [2, 3]:
                    if v[j].get():
                        self.data[str(index)][
                            self.language[f"{8 + i}"][self.selected]
                        ] = int(v[j].get())
                else:
                    if v[j].get():
                        self.data[str(index)][
                            self.language[f"{8 + i}"][self.selected]
                        ] = v[j].get()
            upper = self.data[str(index)][
                self.language["91"][self.selected]
            ]
            lower = self.data[str(index)][
                self.language["92"][self.selected]
            ]
            if lower <= upper:
                upper_greater_than_lower = True
                v[1].spinbox.configure(background="red")
            else:
                upper_greater_than_lower = False
            if lower > self.depth:
                lower_greater_than_depth = True
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
