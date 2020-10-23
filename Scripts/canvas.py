# -*- coding: utf-8 -*-

from .modules import tk, arange, ImageTk
from .utilities import get_en, merge_images, reformat


class Canvas(tk.Canvas):
    def __init__(
            self,
            language: dict,
            selected: str,
            sheet_number: str,
            casing_pipe_info: dict,
            project_and_company_info: dict,
            lithology_info: dict,
            rc_info: dict,
            spt_info: dict,
            ud_info: dict,
            pressuremeter_info: dict,
            lugeon_info: dict,
            images: dict,
            depth: int,
            side: str = "top",
            limit: bool = False,
            y_limit: int = 22,
            m_start: int = 1,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.language = language
        self.selected = selected
        self.sheet_number = sheet_number
        self.depth = depth
        self.casing_pipe_info = casing_pipe_info
        self.project_and_company_info = project_and_company_info
        self.lithology_info = lithology_info
        self.rc_info = rc_info
        self.spt_info = spt_info
        self.ud_info = ud_info
        self.pressuremeter_info = pressuremeter_info
        self.lugeon_info = lugeon_info
        self.images = images
        self.frame = tk.Frame(master=self)
        self.y_scrollbar = tk.Scrollbar(
            master=self.master,
            orient="vertical",
            command=self.yview
        )
        self.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")
        self.pack(side=side, expand=True, fill=tk.BOTH)
        self.create_window((4, 4), window=self.frame, anchor="nw")
        self.frame.bind(
            sequence="<Configure>",
            func=lambda event: self.configure(
                scrollregion=self.bbox("all")
            )
        )
        self.x_start = 2
        self.x_end = 593
        self.y_start = 2
        self.y_end = (self.y_start + 25) * 31
        self.create_frame_lines()
        self.create_project_information_lines()
        self.create_log_information_lines(y_limit=y_limit, m_start=m_start)
        self.create_rock_evaluation_lines(limit=limit)
        self.create_texts(limit=limit)
        self.create_rock_evaluation_units(limit=limit)
        self.xview_moveto(0)
        self.yview_moveto(0)

    def create_frame_lines(self):
        # For x lines of the frame
        for i in [self.y_start, self.y_end]:
            self.line_object(
                x1=self.x_start,
                x2=self.x_end,
                y1=i,
                y2=i
            )
        # For y lines of the frame
        for i in [self.x_start, self.x_end]:
            self.line_object(
                x1=i,
                x2=i,
                y1=self.y_start,
                y2=self.y_end
            )

    def create_project_information_lines(self):
        y = self.y_start + 25
        # For x lines of the project information
        for i in [y, y * 7.5]:
            self.line_object(
                x1=self.x_start,
                y1=i,
                x2=self.x_end,
                y2=i
            )

    def create_log_information_lines(
            self,
            y_limit: int = 22,
            m_start: int = 1
    ):
        x = (self.x_end - self.x_start) / 25
        y = self.y_start + 25
        # points = []
        # for x line of the log information and units
        for i in range(2):
            self.line_object(
                x1=self.x_start,
                y1=y * (11 + i),
                x2=self.x_end,
                y2=y * (11 + i)
            )
        # For y lines of the log information
        for i in [
            *[x * j for j in range(1, 6)],
            *[x * j for j in range(11, 12)],
            12 * 23.92,
            *[x * (18 + j) for j in range(7)]
        ]:
            self.line_object(
                x1=self.x_start + i,
                y1=y * 7.5,
                x2=self.x_start + i,
                y2=y * y_limit
            )
        # For x line of standard penetration
        self.line_object(
            x1=self.x_start + x * 5,
            y1=y * 9.5,
            x2=self.x_start + x * 11,
            y2=y * 9.5
        )
        # For y line of the standard penetration
        self.line_object(
            x1=self.x_start + x * 8,
            y1=y * 9.5,
            x2=self.x_start + x * 8,
            y2=y * y_limit
        )
        # For y line of the blow count
        for i in range(6, 8):
            self.line_object(
                x1=self.x_start + x * i,
                y1=y * 11,
                x2=self.x_start + x * i,
                y2=y * y_limit
            )
        # For y line of the graph
        x_start_graph = self.x_start + x * 8
        x_end_graph = self.x_start + x * 11
        x_interval = (x * 3) / 6
        for i in arange(
                x_start_graph + x_interval,
                x_end_graph - x_interval,
                x_interval
        ):
            self.line_object(
                x1=i,
                y1=y * 12,
                x2=i,
                y2=y * y_limit
            )
        # For x line of the metrics
        end = 0
        count = m_start - 1
        points = []
        for i in range(1, 2000):
            count += 0.01
            if (12 + i / 100) > y_limit:
                break
            if round(count, 2) == float(self.depth):
                end = y * (12 + i / 100)
            if i % 100 == 0:
                self.line_object(
                    x1=self.x_start,
                    y1=y * (12 + i / 100),
                    x2=self.x_start + 5,
                    y2=y * (12 + i / 100)
                )
                # For the text of the metrics
                if y * (12 + i / 100) != y * y_limit:
                    self.text_object(
                        x=self.x_start + 5,
                        y=y * (12 + i / 100),
                        text=str(m_start),
                        font="Arial 6 bold",
                        anchor="w"
                    )
                m_start += 1
            elif i % 10 == 0:
                # For the lines of milimeters.
                self.line_object(
                    x1=self.x_start,
                    y1=y * (12 + i / 100),
                    x2=self.x_start + 2.5,
                    y2=y * (12 + i / 100)
                )
            # For the lithology lines
            for index, (key, value) in enumerate(
                    self.lithology_info.items()
            ):
                upper = value[self.language["91"][self.selected]]
                lower = value[self.language["92"][self.selected]]
                ground_type = value[self.language["93"][self.selected]]
                profile = value[self.language["94"][self.selected]]
                color = value[self.language["95"][self.selected]]
                description = value[self.language["130"][self.selected]]
                if round(count, 2) == upper + 0.1:
                    mid_y = (
                        (12 + i / 100) + (12 + i / 100 + lower - upper)
                    ) / 2
                    # For the profile and description texts
                    if lower - upper >= 1.5:
                        pos = (12 + i / 100)
                    else:
                        pos = 2.5
                    for item in [[profile, 0], [description, 10]]:
                        if len(item[0]) > 30:
                            if item[0] == profile:
                                text = reformat(item[0].upper())
                                font = "Arial 6 bold"
                            else:
                                text = reformat(item[0])
                                font = "Arial 6"
                            c = 0
                            for substring in text:
                                self.text_object(
                                    x=self.x_start + x * 15,
                                    y=y * mid_y - pos + c + item[1],
                                    text=substring,
                                    font=font,
                                    anchor="center"
                                )
                                c += 7.5
                        else:
                            if item[0] == profile:
                                text = item[0].upper()
                                font = "Arial 6 bold"
                            else:
                                text = item[0]
                                font = "Arial 6"
                            self.text_object(
                                x=self.x_start + x * 15,
                                y=y * mid_y - pos + item[1],
                                text=text,
                                font=font,
                                anchor="center"
                            )
                    # For the lithology image
                    for k, v in self.images[
                        get_en(self, ground_type)
                    ].items():
                        if get_en(self, profile, profile=True) == v["name"]:
                            image = ImageTk.PhotoImage(
                                merge_images(
                                    img=v["path"],
                                    start=upper,
                                    end=lower,
                                    color=color
                                )
                            )
                            self.image_object(
                                image=image,
                                x=self.x_start + x * 11 + 0.5,
                                y=y * (12 + i / 100) - 1.7,
                                name=f"image{upper}",
                                anchor="nw"
                            )
                # For the line objects of the lithology
                if (
                        round(count, 2) == lower
                        and
                        y * (12 + i / 100) != y * y_limit
                        and
                        lower != self.depth
                ):
                    self.line_object(
                        x1=self.x_start + x * 11,
                        y1=y * (12 + i / 100),
                        x2=self.x_start + x * 16.5,
                        y2=y * (12 + i / 100)
                    )
                    self.text_object(
                        x=self.x_start + x * 16.5 + 5,
                        y=y * (12 + i / 100),
                        text=f"{lower} m.",
                        font="Arial 6 bold",
                        anchor="w"
                    )
            obj_text = {}
            obj_line = {}
            # For the lines and texts of Casing Pipe
            for info in [
                [self.casing_pipe_info, 4],
                [self.pressuremeter_info, 23],
                [self.lugeon_info, 24]
            ]:
                for index, (key, value) in enumerate(
                        info[0].items()
                ):
                    upper = value[self.language["91"][self.selected]]
                    lower = value[self.language["92"][self.selected]]
                    mid = (upper + lower) / 2
                    if round(count, 2) == upper and upper != 0:
                        self.line_object(
                            x1=self.x_start + x * info[1],
                            y1=y * (12 + i / 100),
                            x2=self.x_start + x * (info[1] + 1),
                            y2=y * (12 + i / 100)
                        )
                    elif round(count, 2) == lower:
                        self.line_object(
                            x1=self.x_start + x * info[1],
                            y1=y * (12 + i / 100),
                            x2=self.x_start + x * (info[1] + 1),
                            y2=y * (12 + i / 100)
                        )
                    elif round(count, 2) == mid:
                        if info[1] == 23:
                            text = f"Pr-{index + 1}"
                        elif info[1] == 24:
                            text = f"PD-{index + 1}"
                        else:
                            text = f"{upper} m. - {lower} m."
                        self.text_object(
                            x=self.x_start + x *
                            ((info[1] + info[1] + 1) / 2),
                            y=y * (12 + i / 100),
                            text=text,
                            anchor="center",
                            font="Arial 6 bold",
                            angle=90
                        )
            # For the lines and texts of RC
            for index, (key, value) in enumerate(
                    self.rc_info.items()
            ):
                upper = value[self.language["91"][self.selected]]
                lower = value[self.language["92"][self.selected]]
                if 1.5 > round(lower - upper, 2) >= 1.05:
                    if lower - 1.05 in obj_line:
                        _upper = lower - 1.05
                    else:
                        _upper = upper
                elif 1.05 > round(lower - upper, 1) >= 0.6:
                    if lower - 0.6 in obj_line:
                        _upper = lower - 0.6
                    else:
                        _upper = upper
                elif 3 > round(lower - upper, 2) >= 2.55:
                    if lower - 2.55 in obj_line:
                        _upper = lower - 2.55
                    else:
                        _upper = upper
                elif 2.55 > round(lower - upper, 1) >= 2.1:
                    if lower - 2.1 in obj_line:
                        _upper = lower - 2.1
                    else:
                        _upper = upper
                else:
                    _upper = upper
                mid = (upper + lower) / 2
                if self.language["8"][self.selected] in value:
                    recovery = value[self.language["8"][self.selected]]
                else:
                    recovery = ""
                if self.language["9"][self.selected] in value:
                    rqd = value[self.language["9"][self.selected]]
                else:
                    rqd = ""
                if self.language["10"][self.selected] in value:
                    fracture = value[self.language["10"][self.selected]]
                else:
                    fracture = ""
                if self.language["11"][self.selected] in value:
                    weathering = value[self.language["11"][self.selected]]
                else:
                    weathering = ""
                if self.language["12"][self.selected] in value:
                    strength = value[self.language["12"][self.selected]]
                else:
                    strength = ""
                # For the lines of rc evaluation
                if round(count, 2) in [_upper, lower]:
                    if round(count, 2) not in obj_line:
                        o = self.line_object(
                            x1=self.x_start + x * 18,
                            y1=y * (12 + i / 100),
                            x2=self.x_start + x * 23,
                            y2=y * (12 + i / 100)
                        )
                        obj_line[round(count, 2)] = o
                # For the texts of rc evaluation
                if round(count, 2) in [round((_upper + lower) / 2, 2)]:
                    if y_limit - round(12 + i / 100, 1) < 0.5:
                        p = 7.5
                    else:
                        p = 0
                    for _, __ in enumerate(
                            [
                                recovery,
                                rqd,
                                fracture,
                                weathering,
                                strength
                            ]
                    ):
                        if _ in [0, 1]:
                            text = __
                        else:
                            text = __.replace(" - ", "\n")
                        self.text_object(
                            x=self.x_start + x * (18.5 + _),
                            y=y * (12 + i / 100) - p,
                            text=text,
                            anchor="center",
                            font="Arial 6 bold",
                        )
                # For the lines and texts of the meters of
                # rc sample.
                if round(count, 2) in [_upper, lower]:
                    # For the lines of the meters of rc sample
                    for _ in [[1, 2], [3, 4]]:
                        if (round(count, 2), *_) not in obj_line:
                            o = self.line_object(
                                x1=self.x_start + x * _[0],
                                y1=y * (12 + i / 100),
                                x2=self.x_start + x * _[1],
                                y2=y * (12 + i / 100)
                            )
                            obj_line[(round(count, 2), *_)] = o
                    # For the texts of the meters of rc sample
                    o = self.text_object(
                        x=self.x_start + x * 2.5,
                        y=y * (12 + i / 100),
                        text=f"{round(count, 2)}",
                        anchor="center",
                        font="Arial 6 bold"
                    )
                    if round(count, 2) in obj_text:
                        self.delete(obj_text[round(count, 2)])
                    obj_text[round(count, 2)] = o
                # For the texts of rc sample name and sample no
                if round(count, 2) == round(mid, 2):
                    if y_limit - round(12 + i / 100, 1) < 0.5:
                        p = 7.5
                    else:
                        p = 0
                    for n in [[3.5, "RC"], [1.5, f"{index + 1}"]]:
                        self.text_object(
                            x=self.x_start + x * n[0],
                            y=y * (12 + i / 100) - p,
                            text=n[1],
                            anchor="center",
                            font="Arial 6 bold"
                        )
            # For the lines and texts of SPT
            for index, (key, value) in enumerate(
                    self.spt_info.items()
            ):
                upper = value[self.language["91"][self.selected]]
                lower = value[self.language["92"][self.selected]]
                if lower - upper < 0.45:
                    _lower = upper + 0.45
                else:
                    _lower = lower
                # For the texts and lines of meters of the spt samples
                if round(count, 2) in [_lower, upper]:
                    if upper in obj_text:
                        self.delete(obj_text[upper])
                        obj_text.pop(upper)
                    if _lower in obj_text:
                        self.delete(obj_text[_lower])
                        obj_text.pop(_lower)
                    if round(count, 2) == _lower:
                        text = lower
                    else:
                        text = upper
                    # For the texts of the meters of spt samples
                    o = self.text_object(
                        x=self.x_start + x * 2.5,
                        y=y * (12 + i / 100),
                        text=f"{text}",
                        anchor="center",
                        font="Arial 6 bold"
                    )
                    obj_text[round(count, 2)] = o
                    # For the lines of the meters of spt samples
                    for n in [[1, 2], [3, 4], [5, 8], [5, 8]]:
                        if n in [[1, 2], [3, 4]]:
                            if (round(count, 2), *n) not in obj_line:
                                o = self.line_object(
                                    x1=self.x_start + x * n[0],
                                    y1=y * (12 + i / 100),
                                    x2=self.x_start + x * n[1],
                                    y2=y * (12 + i / 100)
                                )
                                obj_line[(round(count, 2), *n)] = o
                        else:
                            self.line_object(
                                x1=self.x_start + x * n[0],
                                y1=y * (12 + i / 100),
                                x2=self.x_start + x * n[1],
                                y2=y * (12 + i / 100)
                            )
                # For the texts of spt sample name, sample no,
                # blow counts; for the point of the n30 value
                # and lines between different n30 values.
                if round(count, 2) == upper:
                    mid = (
                        y * (12 + i / 100)
                        + y * (12 + i / 100 + 0.45)
                    ) / 2
                    # For the texts of spt sample name and sample no
                    for n in [[0, index + 1], [2, "SPT"]]:
                        self.text_object(
                            x=self.x_start + x * (1.5 + n[0]),
                            y=mid,
                            text=f"{n[1]}",
                            anchor="center",
                            font="Arial 6 bold"
                        )
                    # For the text of blow counts
                    if "N15" in value:
                        spt_n = value["N30"] + value["N45"]
                        for _, __ in enumerate(
                                [value["N15"], value["N30"], value["N45"]]
                        ):
                            self.text_object(
                                x=self.x_start + x * (5.5 + _),
                                y=mid,
                                text=f"{__}",
                                anchor="center",
                                font="Arial 6 bold"
                            )
                    else:
                        if self.language["117"][self.selected] in value:
                            refusal = value[
                                self.language["117"][self.selected]
                            ]
                            n = 0
                        elif self.language["118"][self.selected] in value:
                            refusal = value[
                                self.language["118"][self.selected]
                            ]
                            n = 1
                        else:
                            refusal = value[
                                self.language["119"][self.selected]
                            ]
                            n = 2
                        self.text_object(
                            x=self.x_start + x * (5.5 + n),
                            y=mid,
                            text=f"50/{refusal}",
                            anchor="center",
                            font="Arial 6 bold"
                        )
                        spt_n = 55
                    spt_x = self.x_start + x * 8 + 1.25 * spt_n - 2
                    # An oval object for the spt_n value.
                    self.oval_object(
                        x=spt_x,
                        y=mid,
                    )
                    points.append((spt_x, mid))
                    # For the line between different n30 values.
                    for _, __ in enumerate(points):
                        if _ != len(points) - 1:
                            p1 = points[_]
                            p2 = points[_ + 1]
                            self.line_object(
                                x1=p1[0],
                                y1=p1[1],
                                x2=p2[0],
                                y2=p2[1],
                                fill="red",
                                width=2
                            )
            # For the lines and texts of UD
            for index, (key, value) in enumerate(
                    self.ud_info.items()
            ):
                upper = value[self.language["91"][self.selected]]
                lower = value[self.language["92"][self.selected]]
                # For the texts and lines of meters of the ud samples
                if round(count, 2) in [lower, upper]:
                    if upper in obj_text:
                        self.delete(obj_text[upper])
                        obj_text.pop(upper)
                    if lower in obj_text:
                        self.delete(obj_text[lower])
                        obj_text.pop(lower)
                    # For the texts of the meters of ud samples
                    if round(count, 2) == upper:
                        text = upper
                    else:
                        text = lower
                    self.text_object(
                        x=self.x_start + x * 2.5,
                        y=y * (12 + i / 100),
                        text=f"{text}",
                        anchor="center",
                        font="Arial 6 bold"
                    )
                    # For the lines of the meters of ud samples
                    for n in [[1, 2], [3, 4]]:
                        if (round(count, 2), *n) not in obj_line:
                            o = self.line_object(
                                x1=self.x_start + x * n[0],
                                y1=y * (12 + i / 100),
                                x2=self.x_start + x * n[1],
                                y2=y * (12 + i / 100)
                            )
                            obj_line[(round(count, 2), *n)] = o
                # For the texts of ud sample name and sample no
                if round(count, 2) == round((upper + lower) / 2, 2):
                    for n in [[0, index + 1], [2, "UD"]]:
                        self.text_object(
                            x=self.x_start + x * (1.5 + n[0]),
                            y=y * (12 + i / 100),
                            text=f"{n[1]}",
                            anchor="center",
                            font="Arial 6 bold"
                        )
        # For the line that shows the borehole end
        splitted = self.sheet_number.split(" / ")
        if splitted[0] == splitted[1]:
            self.depth = float(self.depth)
            self.line_object(
                x1=self.x_start + x * 11,
                y1=end,
                x2=self.x_start + x * 18,
                y2=end
            )
            # For the text of the borehole end
            if 12 + self.depth != y_limit:
                text = self.language['80'][self.selected]
                self.text_object(
                    x=self.x_start + x * 15,
                    y=end + 10,
                    text=f"{text}: {self.depth} m.",
                    font="Arial 7 bold",
                    anchor="center"
                )

    def create_rock_evaluation_lines(self, limit: bool = False):
        if limit:
            return
        x = (self.x_end - self.x_start) / 4
        y = self.y_start + 25
        # For x lines of the rock evaluation
        for i in [
            *[y * j for j in range(22, 25)],
            *[y * j for j in range(27, 29)]
        ]:
            self.line_object(
                x1=self.x_start,
                y1=i,
                x2=self.x_end,
                y2=i
            )
        # For y lines of the rock evaluation
        for i in [self.x_start + x * j for j in range(1, 4)]:
            self.line_object(
                x1=i,
                y1=y * 23,
                x2=i,
                y2=self.y_end
            )

    def create_texts(self, limit: bool = False):
        x_interval = (self.x_end - self.x_start) / 25
        y = self.y_start + 25
        for index, (k, v) in enumerate(self.language.items()):
            if index < 5:
                # For the texts of DEPTH, SAMPLE NO, SAMPLE DEPTH,
                # SAMPLE TYPE and CASING PIPE
                x = self.x_start + 12.5 + (x_interval * index)
                if len(v[self.selected]) > 10:
                    text = v[self.selected].replace(" ", "\n")
                else:
                    text = v[self.selected]
                self.text_object(
                    x=x,
                    y=y * 9.5,
                    text=text,
                    angle=90,
                    anchor="center",
                    font="Arial 7 bold"
                )
                if index in [1, 3]:
                    continue
                else:
                    self.text_object(
                        x=x,
                        y=y * 11.5,
                        text="m",
                        angle=0,
                        anchor="center",
                        font="Arial 7 bold"
                    )
            elif index == 5:
                # For the text of STANDARD PENETRATION TEST
                count = 0
                x = self.x_start + (x_interval * 8)
                for i in v[self.selected].split(" "):
                    self.text_object(
                        x=x,
                        y=y * (8.25 + count),
                        text=i,
                        angle=0,
                        anchor="center",
                        font="Arial 7 bold"
                    )
                    count += 0.5
                # For the texts of the units of BLOW COUNTS
                x = self.x_start + x_interval * 4.5
                for i in range(1, 4):
                    self.text_object(
                        x=x + (i * x_interval),
                        y=y * 11.5,
                        text=f"N{i * 15}",
                        angle=0,
                        anchor="center",
                        font="Arial 7 bold"
                    )
                # For the texts of the numbers of N30 GRAPH
                x = self.x_start + x_interval * 8.5
                for i in range(5):
                    self.text_object(
                        x=x + x_interval * i / 2,
                        y=y * 11.5,
                        text=f"{(i + 1) * 10}",
                        angle=0,
                        anchor="center",
                        font="Arial 7 bold"
                    )
            elif index == 6:
                # For the text of LITHOLOGY
                x = self.x_start + 12.5 * 10.5 + (x_interval * index)
                self.text_object(
                    x=x,
                    y=y * 9.5,
                    text=v[self.selected],
                    angle=90,
                    anchor="center",
                    font="Arial 7 bold"
                )
            elif index == 7:
                # For the text of GROUND DESCRIPTION
                x = self.x_start + 12.5 * 15 + (x_interval * index)
                count = 0
                for i in v[self.selected].split(" "):
                    self.text_object(
                        x=x,
                        y=y * (9 + count),
                        text=i,
                        angle=0,
                        anchor="center",
                        font="Arial 7 bold"
                    )
                    count += 0.5
            elif 7 < index < 15:
                # For the texts of CAROT RECOVERY, RQD, WEATHERING,
                # STRENGTH, PRESSUREMETER TEST and LUGEON TEST
                x = self.x_start + 12.5 * 20 + (x_interval * index)
                if len(v[self.selected]) > 10:
                    text = v[self.selected].replace(" ", "\n")
                else:
                    text = v[self.selected]
                if index == 13:
                    pad = 9.3
                else:
                    pad = 9.5
                self.text_object(
                    x=x,
                    y=y * pad,
                    text=text,
                    angle=90,
                    anchor="center",
                    font="Arial 7 bold"
                )
                # For the texts of the units of CAROT RECOVERY
                # and RQD
                if index in [8, 9]:
                    self.text_object(
                        x=x,
                        y=y * 11.5,
                        text="%",
                        angle=0,
                        anchor="center",
                        font="Arial 7 bold"
                    )
            elif 14 < index < 32:
                # For the texts of PROJECT NAME, LOCATION, GROUND ELEVATION,
                # BOREHOLE DEPTH, COORDINATE Y (E-W), COORDINATE X (N-S),
                # STATION, OFFSET, BOREHOLE NO, SHEET NO, DRILL RIG,
                # DRILL METHOD, DRILLER, ENGINEER, DATE STARTED and
                # DATE FINISHED
                if index < 23:
                    k = 5
                    n = 15
                else:
                    k = 350
                    n = 23
                x = self.x_start + k
                for i, j, m in zip(
                        [0, 105],
                        [v[self.selected], ":"],
                        [7, 8]
                ):
                    self.text_object(
                        x=x + i,
                        y=y * 0.60 * (index - n) + 55,
                        text=j,
                        angle=0,
                        anchor="w",
                        font=f"Arial {m} bold"
                    )
                    if index == 24 and j == ":":
                        self.text_object(
                            x=x + i + 10,
                            y=y * 0.60 * (index - n) + 55,
                            text=self.sheet_number,
                            angle=0,
                            anchor="w",
                            font=f"Arial 7"
                        )
                    if index == 18 and j == ":":
                        self.text_object(
                            x=x + i + 10,
                            y=y * 0.60 * (index - n) + 55,
                            text=f"{self.depth} m.",
                            angle=0,
                            anchor="w",
                            font=f"Arial 7"
                        )
                    if index not in [18, 24] and j == ":":
                        text = ""
                        for key, value in self.language.items():
                            for _k in value.keys():
                                try:
                                    text = self.project_and_company_info[
                                        f"{self.language[f'{index}'][_k]}"
                                    ]
                                except KeyError:
                                    pass
                        self.text_object(
                            x=x + i + 10,
                            y=y * 0.60 * (index - n) + 55,
                            text=text,
                            angle=0,
                            anchor="w",
                            font=f"Arial 7"
                        )
            elif index == 32:
                # For the text of BORING LOG
                x = (self.x_end - self.x_start) / 2 - 40
                self.text_object(
                    x=x,
                    y=y + 10,
                    text=v[self.selected],
                    angle=0,
                    anchor="w",
                    font="Arial 10 bold"
                )
            elif 32 < index < 35:
                # For the texts of BLOW COUNT, GRAPH N30 and
                # SOIL - ROCK EVALUATION
                x = self.x_start + 125 + (x_interval * (index - 33) * 3)
                self.text_object(
                    x=x,
                    y=y * 10.25,
                    text=v[self.selected],
                    angle=0,
                    anchor="w",
                    font="Arial 6 bold"
                )
            elif index == 35 and not limit:
                # For the texts of FINE GRAINED, COARSE GRAINED,
                # RQD, CRACKS, WEATHERING, STENGTH, ABBREVIATIONS and
                # REMARKS
                for i, j, m, o in zip(
                        [8.5, 2, 8.5, 15, 21, 2.2, 8.5, 14.2, 21.2],
                        [
                            *[
                                self.language[f"{35 + n}"][self.selected]
                                for n in range(3)
                            ],
                            "RQD",
                            self.language["38"][self.selected],
                            self.language["11"][self.selected],
                            self.language["12"][self.selected],
                            self.language["39"][self.selected],
                            self.language["40"][self.selected]
                        ],
                        [22.5, *[23.5] * 4, *[27.5] * 4],
                        [10, *[7] * 8]
                ):
                    x = self.x_start + x_interval * i
                    self.text_object(
                        x=x,
                        y=y * m,
                        text=j,
                        angle=0,
                        anchor="w",
                        font=f"Arial {o} bold"
                    )
                    if i == 21.2:
                        # For the text value of REMARKS
                        if self.language["40"][self.selected] in \
                                self.project_and_company_info:
                            remarks = "\n".join(
                                reformat(
                                    self.project_and_company_info[
                                        self.language["40"][self.selected]
                                    ]
                                )
                            )
                            self.text_object(
                                x=x - 50,
                                y=y * m + 25,
                                text=remarks,
                                angle=0,
                                anchor="nw",
                                font=f"Arial 6"
                            )
            elif index == 131:
                # For the text of COMPANY NAME
                x = (self.x_end - self.x_start) / 2
                if self.language["131"][self.selected] in \
                        self.project_and_company_info:
                    self.text_object(
                        x=x,
                        y=y - 12.5,
                        text=self.project_and_company_info[
                            self.language["131"][self.selected]
                        ],
                        angle=0,
                        anchor="center",
                        font=f"Arial 11 bold"
                    )

    def create_rock_evaluation_units(self, limit: bool = False):
        if limit:
            return
        y1 = self.y_start + 25 * 26.3
        y2 = self.y_start + 25 * 30.6
        units = (
            tuple("N30 :" for _ in range(6)),
            tuple("N30 :" for _ in range(5)),
            (
                "0 - 25 % :",
                "25 - 50 % :",
                "50 - 75 % :",
                "75 - 90 % :",
                "90 - 100 % :"
            ),
            (
                "< 1 :",
                "2 - 3 :",
                "4 - 11 :",
                "12 - 50 :",
                "> 50 :"
            ),
            tuple(f"W{_} :" for _ in range(1, 7)),
            tuple(f"R{_} :" for _ in range(0, 7)),
            ("UD :", "RC :", "SPT :", "Pr :", "PD :")
        )
        count = 0
        fine_grained = (
            "0 - 2", "3 - 4", "5 - 8", "9 - 15", "16 - 30", "> 30"
        )
        coarse_grained = (
            "0 - 4", "5 - 10", "11 - 30", "31 - 50", "> 50"
        )
        for index, unit in enumerate(units):
            if index < 4:
                ind = index
                y = y1
                anchor = "w"
                num = 147
                if index in [0, 1]:
                    pad = 70
                elif index in [2, 3]:
                    pad = 17
                    anchor = "e"
                    if index == 2:
                        num = 170
                    else:
                        num = 157
                else:
                    pad = 40
            else:
                y = y2
                ind = index - 4
                if index == 6:
                    anchor = "e"
                    num = 157
                    pad = 20
                else:
                    anchor = "w"
                    num = 147
                    pad = 40
            for i, j in enumerate(unit):
                # For the texts of the units of
                # Rock - Soil Evaluation
                self.text_object(
                    x=self.x_start + 10 + (ind * num),
                    y=y + (i * 10),
                    text=j,
                    angle=0,
                    anchor=anchor,
                    font="Arial 7 bold"
                )
                if count < 6:
                    self.text_object(
                        x=self.x_start + pad - 8 + (ind * num),
                        y=y + (i * 10),
                        text=fine_grained[i],
                        angle=0,
                        anchor="e",
                        font="Arial 6 bold"
                    )
                elif 5 < count < 11:
                    self.text_object(
                        x=self.x_start + pad - 8 + (ind * num),
                        y=y + (i * 10),
                        text=coarse_grained[i],
                        angle=0,
                        anchor="e",
                        font="Arial 6 bold"
                    )
                self.text_object(
                    x=self.x_start + pad + (ind * num),
                    y=y + (i * 10),
                    text=self.language[f"{41 + count}"][self.selected],
                    angle=0,
                    anchor="w",
                    font="Arial 6 bold"
                )
                count += 1

    def line_object(
            self,
            x1: float,
            y1: float,
            x2: float,
            y2: float,
            width: int = 1,
            fill: str = "black",
    ):
        return self.create_line(
            (x1, y1, x2, y2),
            width=width,
            fill=fill,
        )

    def text_object(
            self,
            x: float,
            y: float,
            text: str,
            width: int = 0,
            font: str = "Arial 9",
            fill: str = "black",
            anchor: str = "e",
            angle: int = 0
    ):
        return self.create_text(
            (x, y),
            text=text,
            width=width,
            font=font,
            fill=fill,
            anchor=anchor,
            angle=angle
        )

    def image_object(
            self,
            image,
            x: float,
            y: float,
            name: str,
            anchor: str = "w"
    ):
        globals()[f"image{name}"] = image
        self.create_image(
            (x, y),
            image=image,
            anchor=anchor
        )

    def oval_object(
            self,
            x: float = .0,
            y: float = .0,
    ):
        return self.create_oval(
            x - 2,
            y - 2,
            x + 2,
            y + 2,
            fill="red"
        )
