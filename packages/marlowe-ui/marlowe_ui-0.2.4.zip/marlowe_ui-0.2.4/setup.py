import sys
import os
import glob
from setuptools import setup, find_packages

ver_file = os.path.join('marlowe_ui', 'version.py')
vars = {}
exec(open(ver_file).read(), vars)

setup(name = "marlowe_ui",
    version = vars['__version__'],
    description = "UI program for Marlowe input data file",
    long_description = open('README').read(),
    author = "Takaaki AOKI",
    author_email = "aoki@sakura.nucleng.kyoto-u.ac.jp",
    url = "http://sakura.nucleng.kyoto-u.ac.jp/~aoki/mui/",
    #download_url = "http://sakura.nucleng.kyoto-u.ac.jp/~aoki/mui/",
    packages = find_packages(),
    package_dir = {'marlowe_ui':'marlowe_ui'},
    scripts = ["mui.py"],
    options={},
    install_requires=['lockfile >= 0.9.0'],
    test_suite='tests',
    #This next part it for the Cheese Shop, look a little down the page.
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Topic :: Scientific/Engineering :: Physics"
    ]
) 
