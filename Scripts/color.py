# -*- coding: utf-8 -*-

from .utilities import rgb
from .modules import tk, ImageTk


class Button(tk.Frame):
    def __init__(
            self, image: ImageTk.PhotoImage,
            side: str,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pack(side=side)
        self.ok = tk.Button(
            master=self,
            image=image,
            activebackground=self["bg"],
            borderwidth=0,
            highlightthickness=0
        )
        self.ok.pack()


class Label(tk.Label):
    def __init__(self, side: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=side)


class Entry(tk.Entry):
    def __init__(self, side: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=side)


class Frame(tk.Frame):
    def __init__(self, side: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=side)


class Spinbox(tk.Spinbox):
    def __init__(
            self,
            side: str = "",
            var: tk.IntVar = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pack(side=side)
        self["increment"] = 1
        self["textvariable"] = var
        self["from"] = 0
        self["to"] = 255
        self["width"] = 3


class Scale(tk.Scale):
    def __init__(
            self,
            side: str = "",
            var: tk.IntVar = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pack(side=side)
        self.var = var
        self["orient"] = tk.HORIZONTAL
        self["length"] = 200
        self["sliderlength"] = 15
        self["digits"] = 1
        self["resolution"] = 1
        self["variable"] = self.var
        self["from"] = 0
        self["to"] = 255
        self["showvalue"] = False
        self["bg"] = "white"


class SpinboxScale(tk.Frame):
    def __init__(self, text: str = "", color: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack()
        self.label = Label(master=self, side="left", text=text, fg=color)
        self.var = tk.IntVar()
        self.spinbox = Spinbox(master=self, side="left", var=self.var)
        self.scale = Scale(master=self, side="left", var=self.var)


class AskColor(tk.Toplevel):
    def __init__(
            self,
            title: str,
            image: ImageTk.PhotoImage,
            color_code: str,
            default_color: str,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.resizable(width=False, height=False)
        self.title(title)
        self.default_color = default_color
        self.color = ""
        self.red = SpinboxScale(master=self, text="R", color="#ff0000")
        self.red.var.set(int(default_color[1:3], 16))
        self.green = SpinboxScale(master=self, text="G", color="#00ff00")
        self.green.var.set(int(default_color[3:5], 16))
        self.blue = SpinboxScale(master=self, text="B", color="#0000ff")
        self.blue.var.set(int(default_color[5:], 16))
        self.rgb_code = Label(master=self, text=color_code, side="top")
        self.code = [
            self.red.var.get(), 
            self.green.var.get(), 
            self.blue.var.get()
        ]
        self.entry = Entry(master=self, width=8, side="top")
        self.entry.insert("insert", self.default_color.lower())
        self.buttons = Button(master=self, side="bottom", image=image)
        self.buttons.ok["command"] = self.ok_command
        self.frame = Frame(
            master=self,
            bd=1,
            relief="sunken",
            side="top",
            width=100,
            height=100,
            bg=self.default_color
        )
        self.configurations()
        self.bindings()
        self.wait_window()

    def configurations(self):
        self.red.scale.configure(
            command=lambda var, index=0:
            self.change_code(index=index, var=self.red.var)
        )
        self.green.scale.configure(
            command=lambda var, index=1:
            self.change_code(index=index, var=self.green.var)
        )
        self.blue.scale.configure(
            command=lambda var, index=2:
            self.change_code(index=index, var=self.blue.var)
        )
        self.red.spinbox.configure(
            command=lambda: self.change_code(index=0, var=self.red.var)
        )
        self.green.spinbox.configure(
            command=lambda: self.change_code(index=1, var=self.green.var)
        )
        self.blue.spinbox.configure(
            command=lambda: self.change_code(index=2, var=self.blue.var)
        )

    def bindings(self):
        self.red.spinbox.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.change_code(index=0, var=self.red.var)
        )
        self.green.spinbox.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.change_code(index=1, var=self.green.var)
        )
        self.blue.spinbox.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.change_code(index=2, var=self.blue.var)
        )

    def change_code(self, index: int = 0, var: tk.IntVar = None):
        self.code[index] = var.get()
        self.entry.delete(0, tk.END)
        self.entry.insert("insert", rgb(*self.code))
        self.frame.configure(bg=rgb(*self.code))

    def ok_command(self):
        self.color = self.entry.get()
        self.destroy()
