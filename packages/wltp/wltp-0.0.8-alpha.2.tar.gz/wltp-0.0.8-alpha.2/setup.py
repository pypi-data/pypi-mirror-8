#!/usr/bin/env python
#
# Copyright 2013-2014 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
''''Setuptools script for *wltp*, the WLTC gear-shift calculator.

Install:
========

To install it, assuming you have download the sources,
do the usual::

    python setup.py install

Or get it directly from the PIP repository::

    pip3 install wltp
'''
## Got ideas for project-setup from many places, among others:
#    http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
#    http://python-packaging-user-guide.readthedocs.org/en/latest/current.html

from setuptools import setup
#from cx_Freeze import Executable
#from cx_Freeze import setup
import os, re

projname = 'wltp'
mydir = os.path.dirname(__file__)

## Version-trick to have version-info in a single place,
## taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
##
def read_project_version():
    fglobals = {}
    exec(open(os.path.join(mydir, projname, '_version.py')).read(), fglobals)  # To read __version__
    return fglobals['__version__']
proj_ver = read_project_version()

def read_text_lines(fname):
    with open(os.path.join(mydir, fname)) as fd:
        return fd.readlines()

def yield_sphinx_only_markup(lines):
    """
    :param file_inp:     a `filename` or ``sys.stdin``?
    :param file_out:     a `filename` or ``sys.stdout`?`

    """
    substs = [
        ## Selected Sphinx-only Roles.
        #
        (r':abbr:`([^`]+)`',        r'\1'),
        (r':ref:`([^`]+)`',         r'`\1`_'),
        (r':term:`([^`]+)`',        r'**\1**'),
        (r':dfn:`([^`]+)`',         r'**\1**'),
        (r':(samp|guilabel|menuselection):`([^`]+)`',        r'``\2``'),


        ## Sphinx-only roles:
        #        :foo:`bar`   --> foo(``bar``)
        #        :a:foo:`bar` XXX afoo(``bar``)
        #
        #(r'(:(\w+))?:(\w+):`([^`]*)`', r'\2\3(``\4``)'),
        (r':(\w+):`([^`]*)`', r'\1(``\2``)'),


        ## Sphinx-only Directives.
        #
        (r'\.\. doctest',           r'code-block'),
        (r'\.\. plot::',            r'.. '),
        (r'\.\. seealso',           r'info'),
        (r'\.\. glossary',          r'rubric'),
        (r'\.\. figure::',          r'.. '),


        ## Other
        #
        (r'\|version\|',              r'x.x.x'),
    ]

    regex_subs = [ (re.compile(regex, re.IGNORECASE), sub) for (regex, sub) in substs ]

    def clean_line(line):
        try:
            for (regex, sub) in regex_subs:
                line = regex.sub(sub, line)
        except Exception as ex:
            print("ERROR: %s, (line(%s)"%(regex, sub))
            raise ex

        return line

    for line in lines:
        yield clean_line(line)



proj_ver = read_project_version()


readme_lines = read_text_lines('README.rst')
description = readme_lines[1]
long_desc = ''.join(yield_sphinx_only_markup(readme_lines))

setup(
    name = projname,
    packages = ['wltp', 'wltp.cycles', 'wltp.test', ],
#     package_data= {'projname': ['data/*.csv']},
#     scripts = ['wltp.py'],
    version=proj_ver,
    test_suite='nose.collector',
    description=description,
    long_description=long_desc,
    author="Kostis Anagnostopoulos @ European Commission (JRC)",
    author_email="ankostis@gmail.com",
    url = "https://github.com/ankostis/wltp",
    license = "European Union Public Licence 1.1 or later (EUPL 1.1+)",
    keywords = [
         "automotive", "vehicle", "vehicles", "car", "cars", "fuel", "consumption", "gears", "gearshifs",
        "simulation", "simulator", "driving", "engine", "wltc", "UNECE", "standard",
    ],
    classifiers = [
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 3 - Alpha",
        'Natural Language :: English',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires = [
        'jsonschema>=1.4',
        'numpy',
    ],
    setup_requires = [
        'sphinx',
        'sphinx_rtd_theme',
    ],
    tests_require = [
        'nose',
        'matplotlib',
        'pandas','openpyxl',
    ],
    zip_safe=True,
    options = {
        'build_exe': {
            "excludes": [
                "jsonschema", #!!!! Schemas do not work in library-zip, so needs manuall to copy directly into app-dir
                "numpy", "scipy", #!!!! lostesso
                "PyQt4", "PySide",
                "IPython", "numexpr",
                "pygments", "pyreadline", "jinja2",
                "setuptools",
                "statsmodels", "docutils",
                "xmlrpc", "pytz",
                "nose",
                "Cython", "pydoc_data", "sphinx", "docutils",
                "multiprocessing", "lib2to3", "_markerlib",
#                 #urllib<--email<--http<--pandas
#                 #distutils" <-- pandas.compat
            ],
            'includes': [
#                 'matplotlib.backends.backend_tkagg',
            ],
            'include_files': [
                ## MANUAL COPY into build/exe-dir
                ##     from: https://bitbucket.org/anthony_tuininga/cx_freeze/issue/43/import-errors-when-using-cx_freeze-with
                #  site_packages(32bit/64bit)/
                #    jsonschema
                #    numpy
                #    scipy
            ],
        }, 'bdist_msi': {
            'add_to_path': False,
        },
    },
#     executables=[Executable("wltp.py", )], #base="Win32GUI")],
)
