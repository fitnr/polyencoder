Polyencoder
==========

Python modules for Google Maps polyline encoding.

Python port of the Javascript Google Maps polyline encoder from Mark McClure, released under a BSD license. Both a pure python (gpolyencode) and a C++ extension (cgpolyencode) are implemented, with numerous unit tests.

== Requirements ==

  * Python >= 2.7
  * 

== Installing ==

=== Pure Python module (gpolyencode) ===

  $ sudo python python/setup.py install

If you have the Python `easy_install` utility available, you can also type the following to download and install in one step:

  $ sudo easy_install gpolyencode
  $ sudo easy_install --upgrade gpolyencode    # to force upgrading

## Command line

polyencode layer [options] KEYS INPUT
polyencode point x0,y0 x1,y1

## API

````python
>>> import polyencoder
>>> encoder = polyencoder.PolyEncoder()
# points are a sequence of (longitude,latitude) coordinate pairs
>>> points = ((8.94328,52.29834), (8.93614,52.29767), (8.93301,52.29322), (8.93036,52.28938), (8.97475,52.27014),)
>>> encoder.polyencode(points)
'soe~Hovqu@dCrk@xZpR~VpOfwBmtG'
````

The constructor takes several arguments:
  * `num_levels` specifies how many different levels of magnification the polyline will have. (default: 18)
  * `zoom_factor` specifies the change in magnification between those levels. (default: 2)
  * `threshold` indicates the length of a barely visible object at the highest zoom level. (default: 0.00001)
  * `force_endpoints` indicates whether or not the endpoints should be visible at all zoom levels. (default: True)

See http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/description.html for more details on what these parameters mean and how to tweak them. The defaults are sensible for most situations.

## License

This module is distributed under a BSD license.

The underlying polyencoder is:
```
Copyright (c) 2009, Koordinates Limited
All rights reserved.
```

Updates and command line utils are
```
Copyright (c) 2015, Neil Freeman
All rights reserved.
```