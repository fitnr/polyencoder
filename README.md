Polyencoder
==========

Python module for Google Maps polyline encoding. Want your list of coordinates to look like `e{~vF|c_ci|BqCI}Eyw@`? You've come to the right place!

Includes command line utils for encoding a list of points or an entire geodata file.

## Installing

Two options:
````
pip install polyencoder
pip install polyencoder[layer]
````

The first installs the basic polyencoder. The second installs Fiona, a dependencies for the layer encoder.

Requirements:

* Python >= 2.7
* GDAL (layer encoder only)

## Command line

Encode a set of points:
````
polyencode point x0,y0 x1,y1
````

Encode a geodata layer (.geojson, .shp, etc):
````
polyencode layer id infile.geojson
````

This will produce tab-separated output:
```
1   e%7B%7EvF
2   kF%60%40wFDYtIea
3   ...
```
(Assuming that the 'id' field of the input is 1, 2, 3.)

You can specify more than one key with a comma:
````
polyencode layer id,name infile.geojson
````

By default, results are url-encoded. Get the raw result with `--no-encode`:
````
polyencode layer --no-encode id infile.geojson 

1   e{~vF|c_cMi|BqCg
2   AH~FmClIiLfEkR`AgOjCiOLYrF
````

By default, the result is tab-separated. Use another character:
````
polyencode layer --delimiter , id infile.geojson
````

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

The underlying polyencoder is is Python port of the Javascript Google Maps polyline encoder from Mark McClure, released under a BSD license. It is:
```
Copyright (c) 2009, Koordinates Limited
All rights reserved.
```

Updates and command line utils are
```
Copyright (c) 2015, Neil Freeman
All rights reserved.
```
