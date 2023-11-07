from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "4.0.0 "
DESCRIPTION = "automate upwork"
LONG_DESCRIPTION = "automate upwork"
with open("upwork_scrap.egg-info/requires.txt") as f:
    requirements = f.read().splitlines()
# Setting up
setup(
    name="upwork_scrap",
    version=VERSION,
    author0="NeuralNine (Florian Dedov)",
    author_email="<oussema.benhassena@horizon-tech.tn>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=["python", "video", "stream", "video stream", "camera stream", "sockets"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
