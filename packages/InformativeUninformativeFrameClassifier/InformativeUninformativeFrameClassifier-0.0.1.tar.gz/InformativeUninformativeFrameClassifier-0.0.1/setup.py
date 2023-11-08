#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@brief Setup for the InformativeUninformativeFrameClassifier package.
@author Hassna Irzan (rmaphir@gmail.com).
"""
import setuptools
import unittest
from os import path

# Read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

VERSION = "0.0.1"
DESCRIPTION = "Python module to train and test informative/uninformative frames on Cholect80 and HeiCo datasets."
LONG_DESCRIPTION = long_description

setuptools.setup(
    name="InformativeUninformativeFrameClassifier",
    version=VERSION,
    description=DESCRIPTION,
    author="Hassna Irzan",
    author_email="rmaphir@gmail.com",
    license="MIT License",
    url="https://github.com/HassnaIrzan/InformativeUninformativeFrameClassifier",
    packages=["InformativeUninformativeFrameClassifier"],
    package_dir={
        "InformativeUninformativeFrameClassifier": "src",
    },
    install_requires=[
        "numpy", 
        "torch",
        "torchvision",
        "timm",
        "tensorboard",
        "sklearn",
        "pillow",
        "natsort",
    ],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
)
