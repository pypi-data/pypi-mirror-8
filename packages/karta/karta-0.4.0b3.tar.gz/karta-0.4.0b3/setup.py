from ez_setup import use_setuptools
use_setuptools()
from os.path import exists
from setuptools import setup, Extension
import numpy

VERSION = "0.4.0b3"

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
    include_dirs = [numpy.get_include()]
    ext = ".pyx"
except ImportError:
    USE_CYTHON = False
    include_dirs = []
    ext = ".c"
    print("Warning: Cython not imported")
    print("If C sources exist in the source tree, they will be used")

extensions = [Extension("karta.raster.cfill_sinks",
                        ["karta/raster/cfill_sinks"+ext],
                        include_dirs=include_dirs),
              Extension("karta.raster.crfuncs",
                        ["karta/raster/crfuncs"+ext],
                        include_dirs=include_dirs),
              Extension("karta.vector._cvectorgeo",
                        ["karta/vector/_cvectorgeo"+ext],
                        include_dirs=include_dirs)]

if USE_CYTHON:
    extensions = cythonize(extensions)

for extension in extensions:
    if not all(exists(src) for src in extension.sources):
        # C-extension sources missing, so don't try to build them
        extensions = []
        print("Warning: Extension source not found: {0}".format(extension.sources))
        print("Not building accelerated modules")
        break

setup(
    name = "karta",
    version = VERSION,
    install_requires = ["numpy>=1.6", "cython>=0.15", "pyproj>=1.9", "pyshp>=1.2"],
    author = "Nat Wilson",
    author_email = "njwilson23@gmail.com",
    packages = ["karta", "karta.vector", "karta.raster"],
    url = "http://njwilson23.github.io/karta/",
    description = "A tidy Python package for geospatial computation",
    long_description = """
Karta - tidy Python package for geospatial computation
======================================================

*Karta* is a Leatherman for geographic analyses. *Karta* provides an
lightweight interface for solving problems in Python/Python3. It
presents a simple and clean vector and raster data types, a small
selection of geographical analysis functions, and the ability to read
and write several useful formats.

Goals of *Karta* include exposing a simple and fast framework for
spatial analysis. *Karta* is under development and suggestions and pull
requests are welcome, particularly to improve format support and test
coverage.

DOCUMENTATION
-------------

API documentation can be built by running ``make`` from the ``doc/``
directory. The beginnings of a tutorial to introduce *Karta* are in the
`Wiki <https://github.com/njwilson23/karta/wiki/Tutorial>`__.

CONTENTS AT A GLANCE
--------------------

-  vector

   -  guppy: Vector geometry classes (e.g. ``Point``, ``Multipoint``,
      ``Line``, ``Polygon``) supporting the `Python
      \_\_geo\_interface\_\_ <https://gist.github.com/sgillies/2217756>`__
   -  gpx: GPX class for parsing and constructing GPX eXchange files
   -  geojson: Classes and functions for reading and writing GeoJSON
   -  shp\_funcs: Shapefile-to-guppy conversions through *pyshp*
      interface
   -  xyfile: ASCII table functions
   -  quadtree: QuadTree implementation
   -  stats: Geostatistical functions (experimental)

-  raster

   -  grid: Basic Grid types, including ``RegularGrid`` and
      ``WarpedGrid``
   -  raster: General purpose raster functions
   -  aaigrid: Grid subclass specifically for reading and writing ESRI
      ASCII grids
   -  streamline: Streamline calculation
   -  flow: Stream flow functions (experimental)

-  crs : ``CRS`` and ``CRSRegister`` classes used throughout *Karta*

-  tests : unit tests

FORMATS
-------

*Karta* provides a basic working interface to several of common file
formats. Currently partially-supported are:

-  vector

   -  GeoJSON (r,w)
   -  ESRI Shapefiles via pyshp (r,w)
   -  GPS eXchange (GPX) (r,w)
   -  ASCII tables (XYZ) (r,w)

-  raster

   -  ESRI ASCII Grid (r,w)
   -  GeoTiff through GDAL (r)
   -  USGS DEM (WIP)

INSTALLATION
------------

The easiest way to install is to use ``pip``.

To install the latest release from PyPI, run

::

    pip install karta

To build from source,

::

    git clone https://github.com/njwilson23/karta.git
    pip install -r karta/requirements.txt
    pip install karta/

DEPENDENCIES
------------

Required
~~~~~~~~

-  Python 2.7+ or Python 3.2+
-  numpy
-  pyshp
-  pyproj (for geodetic calculations)

Optional
~~~~~~~~

-  cython
-  gdal (for geotiff I/O)
-  scipy

Cython is an optional dependency used to speed up select functions. In
general, enhanced-performance functions will then be called
automatically when available, otherwise *Karta* will fall back to numpy
and pure-Python versions.

When installing from PyPI, C source code is provided and will be
automatically compiled if a suitable compiler is available.

LICENSE
-------

This software is provided under the MIT license.

MIT License:
~~~~~~~~~~~~

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""",
    download_url = "https://github.com/njwilson23/karta/archive/master.zip",
    classifiers = ["Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Development Status :: 3 - Alpha",
                   "Topic :: Scientific/Engineering"],
    license = "MIT License",
    ext_modules = extensions
)

