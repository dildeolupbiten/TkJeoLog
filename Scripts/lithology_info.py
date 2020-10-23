# -*- coding: utf-8 -*-

from .color import AskColor
from .messagebox import MsgBox
from .modules import os, tk, ttk
from .utilities import translate
from .spinbox import SpinboxFrame


class LithologyInfo(tk.Toplevel):
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
        self.resizable(width=False, height=False)
        if os.name == "posix":
            self.geometry("910x400")
        else:
            self.geometry("965x400")
        self.title(title)
        self.icons = icons
        self.language = language
        self.selected = selected
        self.texts = texts
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
                previous = None
                for index, text in enumerate(self.texts):
                    widget = self.frames[index].winfo_children()[1:][i]
                    value = data[str(i)][
                        translate(self=self, string=text)
                    ]
                    if isinstance(widget, ttk.Combobox):
                        widget.configure(state="normal")
                        widget.delete("0", "end")
                        if "#" not in value:
                            if index == 3:
                                value = translate(
                                    self=self,
                                    string=value,
                                    profile=True
                                )
                            else:
                                value = translate(
                                    self=self,
                                    string=value,
                                    basic=True
                                )
                        widget.insert("insert", value)
                        widget.configure(state="readonly")
                        if index == 2:
                            previous = widget
                        if index == 3:
                            if previous.get() in [
                                "Fine Grained",
                                "İnce Daneli"
                            ]:
                                values = [
                                    v[self.selected]
                                    for v in self.language["126"][
                                        "Fine Grained"
                                    ].values()
                                ]
                                widget.configure(values=values)
                            elif previous.get() in [
                                "Coarse Grained",
                                "İri Daneli"
                            ]:
                                values = [
                                    v[self.selected]
                                    for v in self.language["126"][
                                        "Coarse Grained"
                                    ].values()
                                ]
                                widget.configure(values=values)
                            elif previous.get() in [
                                "Rock",
                                "Kayaç"
                            ]:
                                values = [
                                    v[self.selected]
                                    for v in self.language["126"][
                                        "Rock"
                                    ].values()
                                ]
                                widget.configure(values=values)
                    elif isinstance(widget, SpinboxFrame):
                        widget.var.set(value)
                    elif isinstance(widget, tk.Entry):
                        widget.insert("insert", value)
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
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )
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
            elif index in [2, 3, 4]:
                variable = tk.StringVar()
                if index == 2:
                    w = 13
                    values = [
                        self.language[f"{123 + i}"][self.selected]
                        for i in range(3)
                    ]
                elif index == 3:
                    w = 20
                    values = []
                else:
                    w = 13
                    values = []
                self.variables.append(variable)
                style = ttk.Style()
                if os.name == "nt":
                    style.theme_use('alt')
                style.map(
                    f"{row}.{index}.TCombobox",
                    fieldbackground=[("disabled", "white")]
                )
                combobox = ttk.Combobox(
                    master=self.frames[index],
                    textvariable=variable,
                    values=values,
                    width=w,
                    state="readonly",
                    style=f"{row}.{index}.TCombobox",
                    font="Default 10"
                )
                combobox.grid(row=row, column=0, pady=1)
                self.__bind(combobox=combobox, row=row)
                if index == 4:
                    combobox.configure(
                        postcommand=lambda: self.ask_color(
                            variable=variable, combobox=combobox
                        )
                    )
                self.row_order[row].append(combobox)
            elif index == 5:
                if os.name == "posix":
                    pady = 0
                    width = 15
                else:
                    pady = 2
                    width = 15
                entry = tk.Entry(master=self.frames[index], width=width, font="Default 10")
                entry.grid(row=row, column=0, pady=pady)
                self.row_order[row].append(entry)
        self.canvas.yview_moveto(self.canvas.canvasy(self.canvas.winfo_y()))

    def __bind(self, combobox, row):
        combobox.bind(
            sequence="<<ComboboxSelected>>",
            func=lambda event: self.bind_combobox(combobox, row)
        )

    def bind_combobox(self, combobox, row):
        value = combobox.get()
        if not value:
            ttk.Style().configure(
                combobox.cget("style"),
                fieldbackground="red"
            )
        else:
            ttk.Style().configure(
                combobox.cget("style"),
                fieldbackground="white"
            )
        if value == self.language["123"][self.selected]:
            widgets = self.row_order[row]
            widget = widgets[widgets.index(combobox) + 1]
            widget.configure(
                values=[
                    v[self.selected]
                    for v in self.language["126"]["Fine Grained"].values()
                ]
            )
        elif value == self.language["124"][self.selected]:
            widgets = self.row_order[row]
            widget = widgets[widgets.index(combobox) + 1]
            widget.configure(
                values=[
                    v[self.selected]
                    for v in self.language["126"]["Coarse Grained"].values()
                ]
            )
        elif value == self.language["125"][self.selected]:
            widgets = self.row_order[row]
            widget = widgets[widgets.index(combobox) + 1]
            widget.configure(
                values=[
                    v[self.selected]
                    for v in self.language["126"]["Rock"].values()
                ]
            )

    def remove_entry(self):
        for index, text in enumerate(self.texts):
            widgets = self.frames[index].winfo_children()
            if len(widgets) != 1:
                widgets[-1].destroy()
        self.variables = self.variables[:-2]

    def ask_color(self, variable, combobox):
        variable.set(
            AskColor(
                title=self.language["89"][self.selected],
                image=self.icons["ok"]["img"],
                color_code=self.language["90"][self.selected],
                default_color="#FFFFFF"
            ).color
        )
        if variable.get():
            ttk.Style().configure(
                combobox.cget("style"),
                fieldbackground="white"
            )
        combobox.after(100, lambda: combobox.event_generate("<Escape>"))

    def create_labels(self):
        frames = {}
        for index, text in enumerate(self.texts):
            if index == 3:
                if os.name == "nt":
                    w = 20
                else:
                    w = 27
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
        return frames

    def ok_command(self):
        self.data = {}
        error = False
        for i in range(len(self.frames[0].winfo_children()[1:])):
            self.data[str(i)] = {}
            _upper = None
            _lower = None
            for index, text in enumerate(self.texts):
                widget = self.frames[index].winfo_children()[1:][i]
                if index == 0:
                    try:
                        self.data[str(i)][
                            self.language["91"][self.selected]
                        ] = float(widget.var.get())
                        _upper = widget
                    except tk.TclError:
                        MsgBox(
                            title=self.language["81"][self.selected],
                            message=self.language["101"][self.selected],
                            level="warning",
                            icons=self.icons
                        )
                        return
                elif index == 1:
                    try:
                        self.data[str(i)][
                            self.language["92"][self.selected]
                        ] = float(widget.var.get())
                        _lower = widget
                    except tk.TclError:
                        MsgBox(
                            title=self.language["81"][self.selected],
                            message=self.language["101"][self.selected],
                            level="warning",
                            icons=self.icons
                        )
                        return
                elif index in [2, 3, 4]:
                    if not widget.get():
                        error = True
                        ttk.Style().configure(
                            widget.cget("style"),
                            fieldbackground="red"
                        )
                    else:
                        self.data[str(i)][
                            self.language[f"{91 + index}"][self.selected]
                        ] = widget.get()
                elif index == 5:
                    self.data[str(i)][
                        self.language["130"][self.selected]
                    ] = widget.get()
            upper = self.data[str(i)][self.language["91"][self.selected]]
            lower = self.data[str(i)][self.language["92"][self.selected]]
            if lower <= upper:
                _lower.spinbox.configure(background="red")
                MsgBox(
                    title=self.language["81"][self.selected],
                    message=self.language["102"][self.selected],
                    level="warning",
                    icons=self.icons
                )
                return
            if lower > self.depth:
                _lower.spinbox.configure(background="red")
                MsgBox(
                    title=self.language["81"][self.selected],
                    message=self.language["103"][self.selected],
                    level="warning",
                    icons=self.icons
                )
                return
        if not error:
            self.destroy()
        else:
            MsgBox(
                title=self.language["81"][self.selected],
                message=self.language["101"][self.selected],
                level="warning",
                icons=self.icons
            )
            return
