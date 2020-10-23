# -*- coding: utf-8 -*-

import os
import tkinter as tk

from time import sleep
from tkinter import ttk
from numpy import arange
from json import load, dump
from subprocess import Popen
from webbrowser import open_new
from PyPDF2 import PdfFileMerger
from urllib.error import URLError
from urllib.request import urlopen
from configparser import ConfigParser
from PIL import Image, ImageTk, ImageOps
from tkinter.filedialog import askopenfilename, asksaveasfilename
