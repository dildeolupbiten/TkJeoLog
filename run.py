#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

installed_packages = [
    p.decode().split("==")[0]
    for p in subprocess.check_output(
        [sys.executable, "-m", "pip", "freeze"]
    ).split()
]

packages = ["numpy", "Pillow", "PyPDF2"]

for package in packages:
    if package not in installed_packages:
        os.system(f"{sys.executable} -m pip install {package}")
           
if __name__ == "__main__":
    import Scripts
    Scripts.main()
