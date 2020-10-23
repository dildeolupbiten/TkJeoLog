# -*- coding: utf-8 -*-

from .modules import tk


class MsgBox(tk.Toplevel):
    msgbox = []

    def __init__(self, title: str, message: str, level: str, icons: dict):
        super().__init__()
        for i in self.msgbox:
            i.destroy()
        self.geometry("350x100")
        self.title(title)
        self.resizable(width=False, height=False)
        self.icons = icons
        self.level_icon = self.icons[level]["img"]
        self.button_icon = self.icons["ok"]["img"]
        self.frame = tk.Frame(master=self)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.icon_label = tk.Label(
            master=self.frame,
            image=self.level_icon,
        )
        self.icon_label.pack(side="left", expand=True, fill=tk.BOTH)
        self.message_label = tk.Label(
            master=self.frame,
            text=message,
            font="Arial 14 bold",
            anchor="w"
        )
        self.message_label.pack(side="left", expand=True, fill=tk.BOTH)
        self.button = tk.Button(
            master=self,
            image=self.button_icon,
            borderwidth=0,
            highlightthickness=0,
            command=self.destroy,
            activebackground=self["bg"]
        )
        self.button.pack(side="bottom")
        self.msgbox.append(self)
        self.wait_window()
