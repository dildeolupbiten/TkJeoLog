# -*- coding: utf-8 -*-

from .casing_pipe_info import CasingPipeInfo


class LugeonInfo(CasingPipeInfo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
