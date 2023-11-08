from setuptools import setup, find_packages
import codecs
import os

#here = os.path.abspath(os.path.dirname(__file__))

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#    long_description = "\n" + fh.read()

VERSION = '0.0.11'
DESCRIPTION = 'For Tyson'
LONG_DESCRIPTION = 'For Tyson'

# Setting up
setup(
    name="farewelltyson",
    version=VERSION,
    author="Jordan",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','importlib'],
    keywords=['python', 'tyson', 'message', 'bye', 'goodbye'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_data={'farewelltyson': ['all_data.csv'], 'farewelltyson': ['the_new_data.csv']}
)
