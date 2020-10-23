# -*- coding: utf-8 -*-

from .modules import tk
from .ud_info import UDInfo
from .messagebox import MsgBox


class CasingPipeInfo(UDInfo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
