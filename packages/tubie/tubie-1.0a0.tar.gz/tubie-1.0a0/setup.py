from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0 alpha'
DESCRIPTION = 'Youtube video downloader and converter'
LONG_DESCRIPTION = 'A package that allows to download videos from Youtube and convert to various formats.'

# Setting up
setup(
    name="tubie",
    version=VERSION,
    author="keyaedisa",
    author_email="<keyaedisa@proton.me>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['os', 'shutil', 're', 'pytube', 'moviepy.editor', 'ffmpeg', 'subprocess'],
    keywords=['python', 'video', 'stream', 'video converter', 'youtube', 'downloader'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
