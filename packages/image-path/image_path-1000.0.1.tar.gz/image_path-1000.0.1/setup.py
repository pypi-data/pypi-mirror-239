from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1000.0.1'
DESCRIPTION = 'Dependecy Confusion POC'

# Setting up
setup(
    name="image_path",
    version=VERSION,
    author="Anonymous",
    author_email="kaiksi@wearehackerone.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)

