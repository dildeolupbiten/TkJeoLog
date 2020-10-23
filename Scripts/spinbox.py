# -*- coding: utf-8 -*-

from .modules import tk
from .messagebox import MsgBox


class Label(tk.Label):
    def __init__(self, side: str = "left", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=side)


class Spinbox(tk.Spinbox):
    def __init__(
            self,
            start: int,
            end: int,
            step: float,
            width: int = 5,
            side: str = "left",
            var: tk.DoubleVar = .0,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pack(side=side, expand=True, fill=tk.BOTH)
        self["increment"] = step
        self["textvariable"] = var
        self["from"] = start
        self["to"] = end
        self["width"] = width
        self.update()


class SpinboxFrame(tk.Frame):
    def __init__(
            self,
            icons: dict,
            language: dict,
            selected: str,
            start: int,
            end: int,
            step: float,
            data: str,
            text: str = "",
            width: int = 5,
            grid: bool = False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.icons = icons
        self.language = language
        self.selected = selected
        if not grid:
            self.pack()
        self.label = Label(master=self, text=text, font="Arial 11 bold")
        self.var = tk.DoubleVar()
        if data:
            self.var.set(data)
        self.spinbox = Spinbox(
            master=self,
            var=self.var,
            start=start,
            end=end,
            step=step,
            width=width
        )
        self.configuration()
        self.bindings()

    def configuration(self):
        self.spinbox.configure(command=self.control)

    def bindings(self):
        self.spinbox.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.control()
        )

    def control(self):
        try:
            float(self.var.get())
            self.spinbox.configure(bg="white")
        except tk.TclError:
            self.spinbox.configure(bg="red")
            MsgBox(
                title=self.language["81"][self.selected],
                message=self.language["101"][self.selected],
                level="warning",
                icons=self.icons
            )
