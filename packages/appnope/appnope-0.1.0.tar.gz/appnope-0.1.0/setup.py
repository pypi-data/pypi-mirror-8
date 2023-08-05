#-----------------------------------------------------------------------------
#  Copyright (C) 2013 Min RK
#
#  Distributed under the terms of the 2-clause BSD License.
#-----------------------------------------------------------------------------

from __future__ import print_function

import sys
import platform

from distutils.core import setup
from distutils.extension import Extension
from distutils.version import LooseVersion as V

if sys.platform != 'darwin':
    raise ValueError("Only meant for install on OS X >= 10.9")
elif V(platform.mac_ver()[0]) < V('10.9'):
    print("Only meant for install on OS X >= 10.9", file=sys.stderr)

with open('appnope/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            __version__ = eval(line.split('=', 1)[1])
            break

setup_args = dict(
    name = "appnope",
    version = __version__,
    packages = ["appnope"],
    author = "Min Ragan-Kelley",
    author_email = "benjaminrk@gmail.com",
    url = 'http://github.com/minrk/appnope',
    download_url = 'http://github.com/minrk/appnope/releases',
    description = "Disable App Nap on OS X 10.9",
    long_description = "",
    license = "BSD",
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)

setup(**setup_args)

