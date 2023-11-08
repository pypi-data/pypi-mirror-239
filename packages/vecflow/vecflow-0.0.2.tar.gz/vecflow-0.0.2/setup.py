from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'VecFlow'
LONG_DESCRIPTION = 'We connect your data for easy access by your LLMs.'

# Setting up
setup(
    name="vecflow",
    version=VERSION,
    author="VecFlow",
    author_email="<vecflowai@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'llms', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft :: Windows",
    ]
)