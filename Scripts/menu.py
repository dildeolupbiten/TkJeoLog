# -*- coding: utf-8 -*-

from .modules import tk
from .about import About
from .canvas import Canvas
from .rc_info import RCInfo
from .ud_info import UDInfo
from .spt_info import SPTInfo
from .messagebox import MsgBox
from .spinbox import SpinboxFrame
from .lugeon_info import LugeonInfo
from .lithology_info import LithologyInfo
from .casing_pipe_info import CasingPipeInfo
from .pressuremeter_info import PressuremeterInfo
from .project_and_company_info import ProjectAndCompanyInfo
from .utilities import (
    export_canvas, display, create_spinbox, create_project_and_company_info,
    create_lithology_info, create_rc_info, create_spt_info, create_ud_info,
    create_pressuremeter_info, create_lugeon_info, create_casing_pipe_info,
    save_project, open_project, close_project, load_config, load_defaults,
    check_update
)


class Menu(tk.Menu):
    def __init__(
            self,
            language: dict,
            icons: dict,
            images: dict,
            main_window,
            frame,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.icons = icons
        self.images = images
        self.language = language
        self.main_window = main_window
        self.frame = frame
        self.depth = 0
        self.index = 0
        self.last = 0
        self.casing_pipe_info = {}
        self.project_and_company_info = {}
        self.lithology_info = {}
        self.rc_info = {}
        self.spt_info = {}
        self.ud_info = {}
        self.pressuremeter_info = {}
        self.lugeon_info = {}
        self.frame_list = []
        self.canvas_list = []
        self.file_list = []
        self.label = None
        self.button_frame = None
        self.spinbox = None
        self.selected = load_config()
        self.previous = self.selected
        self.file_menu = tk.Menu(master=self, tearoff=False)
        self.add_menu = tk.Menu(master=self, tearoff=False)
        self.sample_menu = tk.Menu(master=self.add_menu, tearoff=False)
        self.canvas_menu = tk.Menu(master=self, tearoff=False)
        self.settings_menu = tk.Menu(master=self, tearoff=False)
        self.help_menu = tk.Menu(master=self, tearoff=False)
        self.language_menu = tk.Menu(
            master=self.settings_menu,
            tearoff=False
        )
        self.add_cascade(
            label=self.language["104"][self.selected],
            menu=self.file_menu
        )
        self.add_cascade(
            label=self.language["105"][self.selected],
            menu=self.add_menu
        )
        self.add_cascade(
            label=self.language["106"][self.selected],
            menu=self.canvas_menu
        )
        self.add_cascade(
            label=self.language["107"][self.selected],
            menu=self.settings_menu
        )
        self.add_cascade(
            label=self.language["132"][self.selected],
            menu=self.help_menu
        )
        self.file_menu.add_command(
            label=self.language["108"][self.selected],
            command=lambda: open_project(self=self, msgbox=MsgBox)
        )
        self.file_menu.add_command(
            label=self.language["147"][self.selected],
            command=lambda: close_project(self=self, frame_list=self.frame_list)
        )
        self.file_menu.add_command(
            label=self.language["109"][self.selected],
            command=lambda: save_project(self=self, msgbox=MsgBox)
        )
        self.canvas_menu.add_command(
            label=self.language["110"][self.selected],
            command=lambda: display(
                self=self,
                msgbox=MsgBox,
                canvas=Canvas,
                casing_pipe_info=CasingPipeInfo,
                project_and_company_info=ProjectAndCompanyInfo,
                lithology_info=LithologyInfo,
                rc_info=RCInfo,
                spt_info=SPTInfo,
                ud_info=UDInfo,
                pressuremeter_info=PressuremeterInfo,
                lugeon_info=LugeonInfo
            )
        )
        self.canvas_menu.add_command(
            label=self.language["111"][self.selected],
            command=lambda: export_canvas(
                self=self,
                msgbox=MsgBox,
                canvas_list=self.canvas_list,
                file_list=self.file_list,
                frame_list=self.frame_list
            )
        )
        self.settings_menu.add_cascade(
            label=self.language["112"][self.selected],
            menu=self.language_menu
        )
        self.language_menu.add_command(
            label=self.language["113"][self.selected],
            command=lambda: self.change_language(language="en")
        )
        self.language_menu.add_command(
            label=self.language["114"][self.selected],
            command=lambda: self.change_language(language="tr")
        )
        self.add_menu.add_command(
            label=self.language["86"][self.selected],
            command=lambda: create_spinbox(
                self=self,
                spinbox_frame=SpinboxFrame,
                msgbox=MsgBox,

            )
        )
        self.add_menu.add_command(
            label=self.language["140"][self.selected],
            command=lambda: create_casing_pipe_info(
                self=self,
                casing_pipe_info=CasingPipeInfo,
                msgbox=MsgBox
            )
        )
        self.add_menu.add_command(
            label=self.language["88"][self.selected],
            command=lambda: create_project_and_company_info(
                self=self,
                project_and_company_info=ProjectAndCompanyInfo
            )
        )
        self.add_menu.add_command(
            label=self.language["96"][self.selected],
            command=lambda: create_lithology_info(
                self=self,
                lithology_info=LithologyInfo,
                msgbox=MsgBox
            )
        )
        self.add_menu.add_cascade(
            label=self.language["115"][self.selected],
            menu=self.sample_menu
        )
        self.sample_menu.add_command(
            label="RC",
            command=lambda: create_rc_info(
                self=self,
                rc_info=RCInfo,
                msgbox=MsgBox
            )
        )
        self.sample_menu.add_command(
            label="SPT",
            command=lambda: create_spt_info(
                self=self,
                spt_info=SPTInfo,
                msgbox=MsgBox
            )
        )
        self.sample_menu.add_command(
            label="UD",
            command=lambda: create_ud_info(
                self=self,
                ud_info=UDInfo,
                msgbox=MsgBox
            )
        )
        self.sample_menu.add_command(
            label="Pr",
            command=lambda: create_pressuremeter_info(
                self=self,
                pressuremeter_info=PressuremeterInfo,
                msgbox=MsgBox
            )
        )
        self.sample_menu.add_command(
            label="PD",
            command=lambda: create_lugeon_info(
                self=self,
                lugeon_info=LugeonInfo,
                msgbox=MsgBox
            )
        )
        self.help_menu.add_command(
            label=self.language["133"][self.selected],
            command=lambda: About(
                language=self.language,
                selected=self.selected
            )
        )
        self.help_menu.add_command(
            label=self.language["148"][self.selected],
            command=lambda: check_update(
                icons=icons,
                language=self.language,
                selected=self.selected
            )
        )

    def change_language(self, language: str):
        load_defaults(selected=language)
        if language == "tr":
            self.selected = language
            self.entryconfigure(1, label="Dosya")
            self.entryconfigure(2, label="Ekle")
            self.entryconfigure(3, label="Tuval")
            self.entryconfigure(4, label="Ayarlar")
            self.entryconfigure(5, label="Yardım")
            self.file_menu.entryconfigure(0, label="Aç")
            self.file_menu.entryconfigure(1, label="Kapat")
            self.file_menu.entryconfigure(2, label="Kaydet")
            self.canvas_menu.entryconfigure(0, label="Görüntüle")
            self.canvas_menu.entryconfigure(1, label="Dışa aktar")
            self.settings_menu.entryconfigure(1, label="Dil")
            self.language_menu.entryconfigure(0, label="İngilizce")
            self.language_menu.entryconfigure(1, label="Türkçe")
            self.add_menu.entryconfigure(0, label="Derinlik Bilgisi")
            self.add_menu.entryconfigure(1, label="Muhafaza Borusu Bilgisi")
            self.add_menu.entryconfigure(
                2,
                label="Proje Ve Şirket Bilgileri"
            )
            self.add_menu.entryconfigure(3, label="Litoloji Bilgileri")
            self.add_menu.entryconfigure(4, label="Örnek Bilgileri")
            self.help_menu.entryconfigure(0, label="Hakkında")
            self.help_menu.entryconfigure(1, label="Güncelleştirmeleri denetle")
        elif language == "en":
            self.selected = language
            self.entryconfigure(1, label="File")
            self.entryconfigure(2, label="Add")
            self.entryconfigure(3, label="Canvas")
            self.entryconfigure(4, label="Settings")
            self.entryconfigure(5, label="Help")
            self.file_menu.entryconfigure(0, label="Open")
            self.file_menu.entryconfigure(1, label="Close")
            self.file_menu.entryconfigure(2, label="Save")
            self.canvas_menu.entryconfigure(0, label="Display")
            self.canvas_menu.entryconfigure(1, label="Export")
            self.settings_menu.entryconfigure(1, label="Language")
            self.language_menu.entryconfigure(0, label="English")
            self.language_menu.entryconfigure(1, label="Turkish")
            self.add_menu.entryconfigure(0, label="Depth Information")
            self.add_menu.entryconfigure(1, label="Casing Pipe Information")
            self.add_menu.entryconfigure(
                2,
                label="Project And Company Information"
            )
            self.add_menu.entryconfigure(3, label="Lithology Information")
            self.add_menu.entryconfigure(4, label="Sample Information")
            self.help_menu.entryconfigure(0, label="About")
            self.help_menu.entryconfigure(1, label="Check for Updates")
