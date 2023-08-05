=========
wkbheader
=========

The focus of this library is to facilitate transfer of data between postgis and python geometry libraries that don't support postgis's ewkb (extended well known binary) standard.
Specifically it can add and reomve srid values from the wkb header.

Installation
============

Install via pip ::

  $ pip install wkbheader

or download source and run ::

  $ python setup.py install


Usage
=====
Example usage with shapely ::

  >>> import wkbheader
  >>> import psycopg2
  >>> import codecs
  >>> from shapely.geometry import Point
  >>> #Connect to some database and create a geometry table 
  >>> conn = psycopg2.connect('...')
  >>> cursor = conn.cursor()
  >>> cursor.execute("CREATE TABLE points (point_geom GEOMETRY(POINT, 4326))")
  >>> #Create a point and insert it into table
  >>> p = Point(3, 4)
  >>> ewkb = wkbheader.set_srid(p.wkb, 4326)
  >>> wkbheader.get_srid(ewkb)
  4326
  >>> hexewkb = codecs.encode(ewkb, 'hex_codec')
  >>> cursor.execute("INSERT INTO points (point_geom) values (%s)", (hexewkb, ))
