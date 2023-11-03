from setuptools import setup                                                # setuptools is our method for building the module
from setuptools import find_packages
from glob import glob

import os

# VERSION
# parse the __planit_version__ variable from python script
VERSION_PATH = os.path.join("src", "planit", "version.py")
exec(compile(open(VERSION_PATH).read(),VERSION_PATH, "exec"))
PLANIT_VERSION = __planit_version__
PY4J_VERSION = __py4j_version__
LICENSE_LOCATION = "http://www.goplanit.org/docs/licenses/"

# RESOURCES
# pars all jars from resource dir
RESOURCE_DIR = "share/planit"
RESOURCE_JAR_FILE_NAMES = glob(RESOURCE_DIR+'/**')                          

setup(
    name="PLANit-Python",
    version= PLANIT_VERSION,
    description="Python API for traffic assignment using PLANit",
    long_description="PLANit-Python enables Python programs running in "
                     "a Python interpreter to configure and run "
                     "a PLANit traffic assignment. It uses Py4J to "
                     "access the underlying Java API that can be used "
                     "for the same purpose",                     
    url="http://www.goplanit.org",
    author="Mark Raadsen",
    author_email="info@goplanit.org",                              
    license="modified BSD License (see "+LICENSE_LOCATION+")",              # adopted license
    classifiers=[                                                           # meta information regarding this module
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Java",
        "Topic :: Scientific/Engineering",        
    ],
    # we only include these packages
    packages=["planit", "test_utils"],
    # indicate the ./src directory is where to find packages rather than this ""
    package_dir={"": "src"},
    # copy all jars in rsc dir as data_files in module
    data_files=[(RESOURCE_DIR, RESOURCE_JAR_FILE_NAMES)],
    install_requires=[
        # python installation for py4j
        'py4j>=' + PY4J_VERSION,
        'pandas',
        'pytest',
      ],    

)