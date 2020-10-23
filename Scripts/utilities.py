# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .modules import (
    os, tk, load, dump, urlopen, URLError,
    Popen, Image, ImageTk, ImageOps, ConfigParser,
    PdfFileMerger, askopenfilename, asksaveasfilename
)


def load_config():
    config = ConfigParser()
    config.read("Settings/defaults.ini")
    return config["LANGUAGE"]["selected"]


def load_json(filename: str):
    with open(filename, encoding="utf-8") as file:
        return load(file)


def load_defaults(selected: str = ""):
    if os.path.exists("Settings/defaults.ini"):
        return
    config = ConfigParser()
    with open("Settings/defaults.ini", "w") as f:
        config["LANGUAGE"] = {
            "selected": "en" if not selected else selected
        }
        config.write(f)


def check_language(self, string: str):
    for k, v in self.language.items():
        if k != "126":
            if string == v["en"]:
                return "en"
            elif string == v["tr"]:
                return "tr"


def get_en(self, string: str, profile: bool = False):
    if profile:
        for key in self.language["126"]:
            for v in self.language["126"][key].values():
                for k in v:
                    if string == v[k]:
                        return v["en"]
    else:
        for v in self.language.values():
            for k in v:
                if string == v[k]:
                    return v["en"]


def translate(self, string: str, basic: bool = False, profile: bool = False):
    if basic:
        for v in self.language.values():
            for k in v:
                if string == v[k]:
                    return v[self.selected]
    if profile:
        for key in self.language["126"]:
            for v in self.language["126"][key].values():
                for k in v:
                    if string == v[k]:
                        return v[self.selected]
    language = ""
    for keys, values in self.data.items():
        if isinstance(values, dict):
            for k, v in values.items():
                language = check_language(self=self, string=k)
                break
            break
        else:
            language = check_language(self=self, string=keys)
            break
    for v in self.language.values():
        for k in v:
            if string == v[k]:
                if check_language(self, string) != language:
                    return v[language]
                else:
                    return v[k]
    else:
        return string


def reformat(string: str):
    result = ""
    while True:
        if len(string) < 30:
            result += string.strip()
            return result.split("\n")
        try:
            index = string[:30].rindex(" ")
        except ValueError:
            return string
        result += string[:index].strip() + "\n"
        string = string[index:]


def create_image_files(path: str):
    return {
        int(i[:3]) if path in "Images" else i[:-4]: {
            "name": i[4:-4].replace("_", " ").title(),
            "path": os.path.join(os.getcwd(), path, i),
            "img": ImageTk.PhotoImage(
                file=os.path.join(os.getcwd(), path, i)
            )
        }
        for i in sorted(os.listdir(os.path.join(os.getcwd(), path)))
    }


def merge_images(img: str, start: int, end: int, color: str):
    diff = end - start
    height = 27
    width = 26
    img = Image.open(img).crop(
        (0, 0, width, int(height * diff))
    ).convert(mode="L")
    return ImageOps.colorize(img, black="black", white=color)


def export(self, msgbox, canvas_list, file_list, pdf_merger, filename):
    for canvas, file in zip(canvas_list, file_list):
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        canvas.postscript(
            file=f"{file}.ps",
            colormode="color",
            height=842,
            width=595
        )
        gs = os.path.join(os.getcwd(), "Ghostscript", "lib", "ps2pdf")
        os.system(f"{gs} {file}.ps {file}.pdf")
        os.remove(f"{file}.ps")
        pdf_merger.append(f"{file}.pdf")
    pdf_merger.write(f"{filename}")
    pdf_merger.close()
    for file in file_list:
        os.remove(f"{file}.pdf")
    msgbox(
        title=self.language["83"][self.selected],
        message=self.language["84"][self.selected],
        level="info",
        icons=self.icons
    )


def export_canvas(self, msgbox, canvas_list, file_list, frame_list):
    if not canvas_list:
        msgbox(
            title=self.language["81"][self.selected],
            message=self.language["85"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    filename = asksaveasfilename(
        filetypes=[(self.language["146"][self.selected], "*.pdf")],
        initialdir=os.getcwd()
    )
    if filename:
        if not filename.endswith(".pdf"):
            filename = filename + ".pdf"
        pdf_merger = PdfFileMerger()
        for i in range(len(frame_list)):
            self.after(
                100 * (i + 1),
                lambda: back_and_next(
                    self=self,
                    limit=len(canvas_list) - 1,
                    step=1
                )
            )
        self.after(
            100 * len(frame_list),
            lambda: export(
                self=self,
                msgbox=msgbox,
                canvas_list=canvas_list,
                file_list=file_list,
                pdf_merger=pdf_merger,
                filename=filename
            )
        )


def edit_lithology_values(self):
    save = {}
    values = []
    for index, (key, value) in enumerate(self.lithology_info.items()):
        upper = value[self.language["91"][self.selected]]
        lower = value[self.language["92"][self.selected]]
        ground_type = value[self.language["93"][self.selected]]
        profile = value[self.language["94"][self.selected]]
        color = value[self.language["95"][self.selected]]
        description = value[self.language["130"][self.selected]]
        limits = range(10, 10000, 19)
        for i, limit in enumerate(limits):
            if lower > limit > upper:
                if upper not in values:
                    save[len(save)] = {
                        self.language["91"][self.selected]: upper,
                        self.language["92"][self.selected]: limit,
                        self.language["93"][self.selected]: ground_type,
                        self.language["94"][self.selected]: profile,
                        self.language["95"][self.selected]: color,
                        self.language["130"][self.selected]: description
                    }
                    values.append(upper)
                if lower > limits[i + 1]:
                    _lower = limits[i + 1]
                else:
                    _lower = lower
                if limit not in values:
                    save[len(save)] = {
                        self.language["91"][self.selected]: limit,
                        self.language["92"][self.selected]: _lower,
                        self.language["93"][self.selected]: ground_type,
                        self.language["94"][self.selected]: profile,
                        self.language["95"][self.selected]: color,
                        self.language["130"][self.selected]: description
                    }
                    values.append(limit)
        if upper not in values:
            save[len(save)] = value
    return save


def display(
        self,
        msgbox,
        canvas,
        casing_pipe_info,
        project_and_company_info,
        lithology_info,
        rc_info,
        spt_info,
        ud_info,
        pressuremeter_info,
        lugeon_info
):
    if float(self.depth) <= 0:
        msgbox(
            title=self.language["81"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    if self.previous != self.selected:
        self.previous = self.selected
        self.casing_pipe_info = casing_pipe_info(
            icons=self.icons,
            texts=[
                self.language[f"{91 + i}"][self.selected]
                for i in range(2)
            ],
            title=self.language["140"][self.selected],
            data=self.casing_pipe_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
        self.project_and_company_info = project_and_company_info(
            icons=self.icons,
            texts=[self.language["131"][self.selected]] + [
                self.language[f"{15 + i}"][self.selected]
                for i in range(17)
                if i not in [9, 3]
            ] + [self.language["40"][self.selected]],
            title=self.language["88"][self.selected],
            data=self.project_and_company_info,
            language=self.language,
            selected=self.selected,
            wait=False
        ).data
        self.lithology_info = lithology_info(
            icons=self.icons,
            texts=[
                self.language["91"][self.selected],
                self.language["92"][self.selected],
                self.language["93"][self.selected],
                self.language["94"][self.selected],
                self.language["95"][self.selected],
                self.language["130"][self.selected]
            ],
            title=self.language["96"][self.selected],
            data=self.lithology_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
        lithology_info = edit_lithology_values(self=self)
        self.rc_info = rc_info(
            icons=self.icons,
            texts=[
                      self.language[f"{91 + i}"][self.selected]
                      for i in range(2)
                  ] + [
                      self.language[f"{8 + i}"][self.selected]
                      for i in range(5)
                  ],
            title=self.language["120"][self.selected],
            data=self.rc_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
        self.spt_info = spt_info(
            icons=self.icons,
            texts=[
                      self.language[f"{91 + i}"][self.selected]
                      for i in range(2)
                  ] + [
                      "N15",
                      f'{self.language["117"][self.selected]}',
                      "N30",
                      f'{self.language["118"][self.selected]}',
                      "N45",
                      f'{self.language["119"][self.selected]}'
                  ],
            title=self.language["116"][self.selected],
            data=self.spt_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
        self.ud_info = ud_info(
            icons=self.icons,
            texts=[
                self.language[f"{91 + i}"][self.selected]
                for i in range(2)
            ],
            title=self.language["120"][self.selected],
            data=self.ud_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
        self.pressuremeter_info = pressuremeter_info(
            icons=self.icons,
            texts=[
                self.language[f"{91 + i}"][self.selected]
                for i in range(2)
            ],
            title=self.language["143"][self.selected],
            data=self.pressuremeter_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
        self.lugeon_info = lugeon_info(
            icons=self.icons,
            texts=[
                self.language[f"{91 + i}"][self.selected]
                for i in range(2)
            ],
            title=self.language["145"][self.selected],
            data=self.lugeon_info,
            language=self.language,
            selected=self.selected,
            depth=self.depth,
            wait=False
        ).data
    else:
        lithology_info = edit_lithology_values(self=self)
    self.index = 0
    for i in self.frame_list:
        i.destroy()
    if self.button_frame:
        self.button_frame.destroy()
    self.frame_list = []
    self.canvas_list = []
    self.file_list = []
    number = sheet_number(self)
    for i in range(number):
        frame = self.frame(master=self.main_window)
        if i == 0:
            _canvas = canvas(
                master=frame,
                width=595,
                height=self.main_window["height"] - 48,
                language=self.language,
                selected=self.selected,
                sheet_number=f"1 / {number}",
                depth=self.depth,
                casing_pipe_info=self.casing_pipe_info,
                project_and_company_info=self.project_and_company_info,
                lithology_info=lithology_info,
                rc_info=self.rc_info,
                spt_info=self.spt_info,
                ud_info=self.ud_info,
                pressuremeter_info=self.pressuremeter_info,
                lugeon_info=self.lugeon_info,
                images=self.images
            )
        else:
            _canvas = canvas(
                master=frame,
                width=595,
                height=self.main_window["height"] - 48,
                language=self.language,
                selected=self.selected,
                limit=True,
                y_limit=31,
                m_start=11 + ((i - 1) * 19),
                sheet_number=f"{i + 1} / {number}",
                depth=self.depth,
                casing_pipe_info=self.casing_pipe_info,
                project_and_company_info=self.project_and_company_info,
                lithology_info=lithology_info,
                rc_info=self.rc_info,
                spt_info=self.spt_info,
                ud_info=self.ud_info,
                pressuremeter_info=self.pressuremeter_info,
                lugeon_info=self.lugeon_info,
                images=self.images
            )
        self.frame_list.append(frame)
        self.canvas_list.append(_canvas)
        self.file_list.append(f"output{i}")
        if i != 0:
            frame.pack_forget()
    self.button_frame = self.frame(master=self.main_window)
    self.button_frame.pack(side="bottom")
    self.label = tk.Label(
        master=self.button_frame,
        text=f"1 / {number}"
    )
    self.label.pack(side="bottom")
    back_button = tk.Button(
        master=self.button_frame,
        image=self.icons["back"]["img"],
        highlightthickness=0,
        borderwidth=0,
        activebackground=self["bg"],
        command=lambda: back_and_next(
            self=self,
            limit=0,
            step=-1
        )
    )
    back_button.pack(side="left")
    next_button = tk.Button(
        master=self.button_frame,
        image=self.icons["next"]["img"],
        highlightthickness=0,
        borderwidth=0,
        activebackground=self["bg"],
        command=lambda: back_and_next(
            self=self,
            limit=len(self.canvas_list) - 1,
            step=1
        )
    )
    next_button.pack(side="right")


def create_spinbox(self, spinbox_frame, msgbox):
    toplevel = tk.Toplevel()
    toplevel.geometry("250x50")
    toplevel.resizable(width=False, height=False)
    toplevel.title(self.language["86"][self.selected])
    self.spinbox = spinbox_frame(
        master=toplevel,
        icons=self.icons,
        language=self.language,
        selected=self.selected,
        text=self.language["87"][self.selected],
        data=self.depth,
        start=0,
        end=10000,
        step=0.5
    )
    button = tk.Button(
        master=toplevel,
        image=self.icons["ok"]["img"],
        borderwidth=0,
        highlightthickness=0,
        activebackground=self["bg"],
        command=lambda: get_spinbox_value(
            self=self,
            master=toplevel,
            spinbox=self.spinbox,
            msgbox=msgbox
        )
    )
    button.pack()


def get_spinbox_value(self, spinbox, master, msgbox):
    try:
        self.depth = spinbox.var.get()
        master.destroy()
    except tk.TclError:
        msgbox(
            title=self.language["81"][self.selected],
            message=self.language["101"][self.selected],
            level="warning",
            icons=self.icons
        )


def create_project_and_company_info(self, project_and_company_info):
    self.project_and_company_info = project_and_company_info(
        icons=self.icons,
        texts=[self.language["131"][self.selected]] + [
            self.language[f"{15 + i}"][self.selected]
            for i in range(17)
            if i not in [9, 3]
        ] + [self.language["40"][self.selected]],
        title=self.language["88"][self.selected],
        data=self.project_and_company_info,
        language=self.language,
        selected=self.selected
    ).data


def create_lithology_info(self, lithology_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.lithology_info = lithology_info(
        icons=self.icons,
        texts=[
            self.language["91"][self.selected],
            self.language["92"][self.selected],
            self.language["93"][self.selected],
            self.language["94"][self.selected],
            self.language["95"][self.selected],
            self.language["130"][self.selected]
        ],
        title=self.language["96"][self.selected],
        data=self.lithology_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def create_rc_info(self, rc_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.rc_info = rc_info(
        icons=self.icons,
        texts=[
            self.language[f"{91 + i}"][self.selected]
            for i in range(2)
        ] + [
            self.language[f"{8 + i}"][self.selected]
            for i in range(5)
        ],
        title=self.language["121"][self.selected],
        data=self.rc_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def create_spt_info(self, spt_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.spt_info = spt_info(
        icons=self.icons,
        texts=[
            self.language[f"{91 + i}"][self.selected]
            for i in range(2)
        ] + [
            "N15",
            f'{self.language["117"][self.selected]}',
            "N30",
            f'{self.language["118"][self.selected]}',
            "N45",
            f'{self.language["119"][self.selected]}'
        ],
        title=self.language["116"][self.selected],
        data=self.spt_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def create_ud_info(self, ud_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.ud_info = ud_info(
        icons=self.icons,
        texts=[
            self.language[f"{91 + i}"][self.selected]
            for i in range(2)
        ],
        title=self.language["120"][self.selected],
        data=self.ud_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def create_pressuremeter_info(self, pressuremeter_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.pressuremeter_info = pressuremeter_info(
        icons=self.icons,
        texts=[
            self.language[f"{91 + i}"][self.selected]
            for i in range(2)
        ],
        title=self.language["143"][self.selected],
        data=self.pressuremeter_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def create_lugeon_info(self, lugeon_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.lugeon_info = lugeon_info(
        icons=self.icons,
        texts=[
            self.language[f"{91 + i}"][self.selected]
            for i in range(2)
        ],
        title=self.language["145"][self.selected],
        data=self.lugeon_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def create_casing_pipe_info(self, casing_pipe_info, msgbox):
    if not self.depth:
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["82"][self.selected],
            level="warning",
            icons=self.icons
        )
        return
    self.casing_pipe_info = casing_pipe_info(
        icons=self.icons,
        texts=[
            self.language[f"{91 + i}"][self.selected]
            for i in range(2)
        ],
        title=self.language["140"][self.selected],
        data=self.casing_pipe_info,
        language=self.language,
        selected=self.selected,
        depth=self.depth
    ).data


def save_project(self, msgbox):
    data = {
        self.language["97"][self.selected]: self.selected,
        self.language["98"][self.selected]: self.depth,
        self.language["141"][self.selected]: self.casing_pipe_info,
        self.language["99"][self.selected]: self.project_and_company_info,
        self.language["100"][self.selected]: self.lithology_info,
        self.language["122"][self.selected]: {
            "RC": self.rc_info,
            "SPT": self.spt_info,
            "UD": self.ud_info,
            "Pr": self.pressuremeter_info,
            "PD": self.lugeon_info
        },
    }
    filename = asksaveasfilename(
        filetypes=[(self.language["127"][self.selected], "*.json")],
        initialdir=os.path.join(".", "Projects")
    )
    if filename:
        if not filename.endswith(".json"):
            filename = filename + ".json"
        with open(filename, "w", encoding="utf-8") as f:
            dump(data, f, indent=4, ensure_ascii=False)
        msgbox(
            title=self.language["83"][self.selected],
            message=self.language["128"][self.selected],
            level="info",
            icons=self.icons
        )


def open_project(self, msgbox):
    filename = askopenfilename(
        filetypes=[(self.language["127"][self.selected], "*.json")],
        initialdir=os.path.join(".", "Projects")
    )
    if filename:
        project = load_json(filename=filename)
        try:
            self.selected = project["LANGUAGE"]
            self.depth = project["DEPTH (m)"]
            self.casing_pipe_info = project[
                "CASING PIPE INFORMATION"
            ]
            self.project_and_company_info = project[
                "PROJECT AND COMPANY INFORMATION"
            ]
            self.lithology_info = project["LITHOLOGY INFORMATION"]
            self.rc_info = project["SAMPLE INFORMATION"]["RC"]
            self.spt_info = project["SAMPLE INFORMATION"]["SPT"]
            self.ud_info = project["SAMPLE INFORMATION"]["UD"]
            self.pressuremeter_info = project["SAMPLE INFORMATION"]["Pr"]
            self.lugeon_info = project["SAMPLE INFORMATION"]["PD"]
            self.change_language(language=project["LANGUAGE"])
        except KeyError:
            self.selected = project["DİL"]
            self.depth = project["DERİNLİK (m)"]
            self.casing_pipe_info = project[
                "MUHAFAZA BORUSU BİLGİSİ"
            ]
            self.project_and_company_info = project[
                "PROJE VE ŞİRKET BİLGİLERİ"
            ]
            self.lithology_info = project["LİTOLOJİ BİLGİLERİ"]
            self.rc_info = project["ÖRNEK BİLGİLERİ"]["RC"]
            self.spt_info = project["ÖRNEK BİLGİLERİ"]["SPT"]
            self.ud_info = project["ÖRNEK BİLGİLERİ"]["UD"]
            self.pressuremeter_info = project["ÖRNEK BİLGİLERİ"]["Pr"]
            self.lugeon_info = project["ÖRNEK BİLGİLERİ"]["PD"]
            self.change_language(language=project["DİL"])
        filename = os.path.split(filename)[-1]
        msgbox(
            title=self.language["83"][self.selected],
            message=f'{filename} {self.language["129"][self.selected]}',
            level="info",
            icons=self.icons
        )


def close_project(self, frame_list):
    if self.button_frame:
        self.button_frame.destroy()
    for i in frame_list:
        i.destroy()
    self.depth = 0
    self.casing_pipe_info = {}
    self.project_and_company_info = {}
    self.lithology_info = {}
    self.rc_info = {}
    self.spt_info = {}
    self.ud_info = {}
    self.pressuremeter_info = {}
    self.lugeon_info = {}


def sheet_number(self):
    step = 19
    count = 1
    for i in range(10, 20000, step):
        count += 1
        if float(self.depth) <= 10:
            return 1
        elif i < float(self.depth) < i + step:
            return count
        elif i == float(self.depth) and i != 10:
            return count - 1


def back_and_next(self, limit, step):
    if self.index != limit:
        self.frame_list[self.index].pack_forget()
        self.index += step
        self.frame_list[self.index].pack()
        self.label.configure(
            text=f"{self.index + 1} / {len(self.frame_list)}"
        )


def rgb(r: int = 0, g: int = 0, b: int = 0):
    return "#" + "".join(hex(i)[2:].zfill(2) for i in (r, g, b))


def check_update(language, selected, icons):
    try:
        new = urlopen(
            "https://raw.githubusercontent.com/dildeolupbiten"
            "/TkJeoLog/master/README.md"
        ).read().decode()
    except URLError:
        MsgBox(
            title=language["81"][selected],
            message=language["149"][selected],
            level="warning",
            icons=icons
        )
        return
    with open("README.md", "r", encoding="utf-8") as f:
        old = f.read()[:-1]
    if new != old:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new)
    try:
        scripts = load(
            urlopen(
                url=f"https://api.github.com/repos/dildeolupbiten/"
                    f"TkJeoLog/contents/Scripts?ref=master"
            )
        )
    except URLError:
        MsgBox(
            title=language["81"][selected],
            message=language["149"][selected],
            level="warning",
            icons=icons
        )
        return
    update = False
    for i in scripts:
        try:
            file = urlopen(i["download_url"]).read().decode()
        except URLError:
            MsgBox(
                title=language["81"][selected],
                message=language["149"][selected],
                level="warning",
                icons=icons
            )
            return
        if i["name"] not in os.listdir("Scripts"):
            update = True
            with open(f"Scripts/{i['name']}", "w", encoding="utf-8") as f:
                f.write(file)
        else:
            with open(f"Scripts/{i['name']}", "r", encoding="utf-8") as f:
                if file != f.read():
                    update = True
                    with open(
                            f"Scripts/{i['name']}",
                            "w",
                            encoding="utf-8"
                    ) as g:
                        g.write(file)
    if update:
        MsgBox(
            title=language["83"][selected],
            message=language["150"][selected],
            level="info",
            icons=icons
        )
        if os.name == "posix":
            Popen(["python3", "run.py"])
            os.kill(os.getpid(), __import__("signal").SIGKILL)
        elif os.name == "nt":
            Popen(["python", "run.py"])
            os.system(f"TASKKILL /F /PID {os.getpid()}")
    else:
        MsgBox(
            title=language["83"][selected],
            message=language["151"][selected],
            level="info",
            icons=icons
        )
