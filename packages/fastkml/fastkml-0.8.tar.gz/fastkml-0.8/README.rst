Introduction
============

fastkml is a library to read, write and manipulate kml files. It aims
to keep it simple and fast (using lxml_ if available). Fast refers to
the time you spend to write and read KML files as well as the time you
spend to get aquainted to the library or to create KML objects. It provides
a subset of KML and is aimed at documents that can be read from multiple
clients such as openlayers and google maps rather than to give you all
functionality that KML on google earth provides.

Geometries are handled as pygeoif_ or shapely_ (if installed) objects.

.. _pygeoif: http://pypi.python.org/pypi/pygeoif/
.. _shapely: http://pypi.python.org/pypi/Shapely
.. _collective.geo.fastkml: http://pypi.python.org/pypi/collective.geo.fastkml
.. _lxml: https://pypi.python.org/pypi/lxml
.. _dateutils: https://pypi.python.org/pypi/dateutils

fastkml is continually tested with *Travis CI*

.. image:: https://api.travis-ci.org/cleder/fastkml.png
    :target: https://travis-ci.org/cleder/fastkml

.. image:: https://coveralls.io/repos/cleder/fastkml/badge.png?branch=master
    :target: https://coveralls.io/r/cleder/fastkml?branch=master

.. image:: https://www.ohloh.net/p/fastkml/widgets/project_thin_badge.gif
    :target: https://www.ohloh.net/p/fastkml

Rationale
==========

Why yet another KML library? None of the existing ones quite fitted my requirements
 
* fastkml can *read and write* KML files, feeding fastkmls output back into fastkml 
  and serializing it again will result in the same output. 
* You can parse any kml snipppet, it does not need to be a complete KML document.
* It runs on python 2 and 3. 
* It is fully tested and actively maintained.
* Geometries are handled in the `__geo_interface__` standard.
* Minimal dependencies, pure python.
* If available lxml_ will be used to increase its speed.


Install
========

You can install the package with `pip install fastkml` or `easy_install fastkml` 
which should also pull in all requirements.

Requirements
-------------

* pygeoif_
* dateutils_

optional:

* lxml_
* shapely_

You can install the requirements for fastkml by using pip:

    pip install -r requirements/common.txt

To install packages required for running tests:

    pip install -r requirements/test.txt


Limitations
===========

*Tesselate*, *Extrude* and *Altitude Mode* are assigned to a Geometry or
Geometry collection (MultiGeometry). You cannot assign diffrent
values of *Tesselate*, *Extrude* or *Altitude Mode* on parts of a MultiGeometry.


Usage
=====

You can find more examples in the included tests.py file or in
collective.geo.fastkml_,
here is a quick overview:


Build a KML from scratch:
--------------------------

Example how to build a simple KML file

    >>> from fastkml import kml
    >>> from shapely.geometry import Point, LineString, Polygon
    >>> k = kml.KML()
    >>> ns = '{http://www.opengis.net/kml/2.2}'
    >>> d = kml.Document(ns, 'docid', 'doc name', 'doc description')
    >>> f = kml.Folder(ns, 'fid', 'f name', 'f description')
    >>> k.append(d)
    >>> d.append(f)
    >>> nf = kml.Folder(ns, 'nested-fid', 'nested f name', 'nested f description')
    >>> f.append(nf)
    >>> f2 = kml.Folder(ns, 'id2', 'name2', 'description2')
    >>> d.append(f2)
    >>> p = kml.Placemark(ns, 'id', 'name', 'description')
    >>> p.geometry =  Polygon([(0, 0, 0), (1, 1, 0), (1, 0, 1)])
    >>> f2.append(p)
    >>> print k.to_string(prettyprint=True)
    '<kml:kml xmlns:ns0="http://www.opengis.net/kml/2.2">
      <kml:Document id="docid">
        <kml:name>doc name</kml:name>
        <kml:description>doc description</kml:description>
        <kml:visibility>1</kml:visibility>
        <kml:open>0</kml:open>
        <kml:Folder id="fid">
          <kml:name>f name</kml:name>
          <kml:description>f description</kml:description>
          <kml:visibility>1</kml:visibility>
          <kml:open>0</kml:open>
          <kml:Folder id="nested-fid">
            <kml:name>nested f name</kml:name>
            <kml:description>nested f description</kml:description>
            <kml:visibility>1</kml:visibility>
            <kml:open>0</kml:open>
          </kml:Folder>
        </kml:Folder>
        <kml:Folder id="id2">
          <kml:name>name2</kml:name>
          <kml:description>description2</kml:description>
          <kml:visibility>1</kml:visibility>
          <kml:open>0</kml:open>
          <kml:Placemark id="id">
            <kml:name>name</kml:name>
            <kml:description>description</kml:description>
            <kml:visibility>1</kml:visibility>
            <kml:open>0</kml:open>
            <kml:Polygon>
              <kml:outerBoundaryIs>
                <kml:LinearRing>
                  <kml:coordinates>0.000000,0.000000,0.000000
                  1.000000,1.000000,0.000000
                  1.000000,0.000000,1.000000
                  0.000000,0.000000,0.000000
                  </kml:coordinates>
                </kml:LinearRing>
             </kml:outerBoundaryIs>
            </kml:Polygon>
          </kml:Placemark>
        </kml:Folder>
      </kml:Document>
    </kml:kml>'



Read a KML file
----------------

You can create a KML object by reading a KML file

    >>> from fastkml import kml
    >>> doc = """<?xml version="1.0" encoding="UTF-8"?>
    ... <kml xmlns="http://www.opengis.net/kml/2.2">
    ... <Document>
    ...   <name>Document.kml</name>
    ...   <open>1</open>
    ...   <Style id="exampleStyleDocument">
    ...     <LabelStyle>
    ...       <color>ff0000cc</color>
    ...     </LabelStyle>
    ...   </Style>
    ...   <Placemark>
    ...     <name>Document Feature 1</name>
    ...     <styleUrl>#exampleStyleDocument</styleUrl>
    ...     <Point>
    ...       <coordinates>-122.371,37.816,0</coordinates>
    ...     </Point>
    ...   </Placemark>
    ...   <Placemark>
    ...     <name>Document Feature 2</name>
    ...     <styleUrl>#exampleStyleDocument</styleUrl>
    ...     <Point>
    ...       <coordinates>-122.370,37.817,0</coordinates>
    ...     </Point>
    ...   </Placemark>
    ... </Document>
    ... </kml>"""
    >>> k = kml.KML()
    >>> k.from_string(doc)
    >>> features = list(k.features())
    >>> len(features)
    1
    >>> features[0].features()
    <generator object features at 0x2d7d870>
    >>> f2 = list(features[0].features())
    >>> len(f2)
    2
    >>> f2[0]
    <fastkml.kml.Placemark object at 0x2d791d0>
    >>> f2[0].description
    >>> f2[0].name
    'Document Feature 1'
    >>> f2[1].name
    'Document Feature 2'
    >>> f2[1].name = "ANOTHER NAME"
    >>> print k.to_string(prettyprint=True)
    <kml:kml xmlns:ns0="http://www.opengis.net/kml/2.2">
      <kml:Document>
        <kml:name>Document.kml</kml:name>
        <kml:visibility>1</kml:visibility>
        <kml:open>1</kml:open>
        <kml:Style id="exampleStyleDocument">
          <kml:LabelStyle>
            <kml:color>ff0000cc</kml:color>
            <kml:scale>1.0</kml:scale>
          </kml:LabelStyle>
        </kml:Style>
        <kml:Placemark>
          <kml:name>Document Feature 1</kml:name>
          <kml:visibility>1</kml:visibility>
          <kml:open>0</kml:open>
          <kml:Point>
            <kml:coordinates>-122.371000,37.816000,0.000000</kml:coordinates>
          </kml:Point>
        </kml:Placemark>
        <kml:Placemark>
          <kml:name>ANOTHER NAME</kml:name>
          <kml:visibility>1</kml:visibility>
          <kml:open>0</kml:open>
          <kml:Point>
            <kml:coordinates>-122.370000,37.817000,0.000000</kml:coordinates>
          </kml:Point>
        </kml:Placemark>
      </kml:Document>
    </kml:kml>



