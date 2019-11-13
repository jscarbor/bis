"""
Call the satellite image segmentation REST API

Berkeley Image Seg is a region merging image object segmentation algorithm
Give it multiband satellite imagery and it returns an int image labeled with object IDs
www.imageseg.com  jscar@berkenviro.com
This code is at https://github.com/jscarbor/bis

>>> # endpoint = 'http://localhost:8080/v1/segment'
>>> endpoint = 'https://api.imageseg.com/v1/segment'

Send a small image as an array/list in 'array' parameter in URL of a GET request
>>> r = requests.get(endpoint + '?array=[[[1]],[[2]],[[1]]]')  # 3 band, 1 pix
>>> regions = np.array(r.json())
>>> regions.shape
(1, 1)
>>> regions
array([[0]])

Send an image as a JSON array/list in the body of a POST request
>>> array = rasterio.open('agé.bmp').read()
>>> array.shape, array.dtype  # A plain RGB image
((3, 127, 212), dtype('uint8'))
>>> r = requests.post(endpoint, json=array.tolist())
>>> regions = np.array(r.json())
>>> regions.shape
(127, 212)
>>> regions.max() + 1  # Total number of image objects / labels / IDs
338
>>> regions  # doctest:+ELLIPSIS
array([[310, 310, 310, ..., 328, 328, 336],
       [334, 334, 334, ..., 328, 328, 336],
       [293, 293, 293, ..., 328, 328, 328],
       ...,
       [  0,   0,   0, ...,  20,  20,  20],
       [  0,   0,   0, ...,  20,  20,  20],
       [  0,   0,   0, ...,  20,  20,  20]])

Send an image as a rasterio compatible bytestream in the file of a POST request
You'll get a GeoTIFF back with the same georeferencing
>>> r = requests.post(endpoint, files={'file': open('agé.bmp', 'rb')})
>>> regions = rasterio.io.MemoryFile(r.content).open().read(1)
>>> regions.shape
(127, 212)
>>> regions.max() + 1
338

Send the link to a file on the internet as 'url' parameter of a GET request
>>> r = requests.get(endpoint + '?url=https://api.imageseg.com/agé.bmp')
>>> regions = rasterio.io.MemoryFile(r.content).open().read(1)
>>> regions.shape
(127, 212)
>>> regions.max() + 1
338

Your multi-spectral sensor, computed bands, or EO fused with LiDAR are cool too
>>> rasterio.open('11-band.tif').profile  #doctest:+NORMALIZE_WHITESPACE
{'driver': 'GTiff', 'dtype': 'int16', 'nodata': None,
 'width': 200, 'height': 200, 'count': 11, 'crs': CRS.from_epsg(32613),
 'transform': Affine(30.0, 0.0, 399255.0, 0.0, -30.0, 2605275.0),
 'tiled': False, 'interleave': 'pixel'}
>>> r = requests.post(endpoint, files={'file': open('11-band.tif', 'rb')})
>>> dataset = rasterio.io.MemoryFile(r.content).open()
>>> dataset.profile  #doctest:+NORMALIZE_WHITESPACE
{'driver': 'GTiff', 'dtype': 'int32', 'nodata': 0.0,
 'width': 200, 'height': 200, 'count': 1, 'crs': CRS.from_epsg(32613),
 'transform': Affine(30.0, 0.0, 399255.0, 0.0, -30.0, 2605275.0),
 'blockxsize': 256, 'blockysize': 256, 'tiled': True, 'compress': 'lzw',
 'interleave': 'band'}
>>> dataset.read(1).max() + 1
187

RapidEye from https://developers.planet.com/planetschool/downloading-imagery/
>>> rasterio.open('redding1.tiff').profile  #doctest:+NORMALIZE_WHITESPACE
{'driver': 'GTiff', 'dtype': 'uint8', 'nodata': None, 'width': 5000,
 'height': 5000, 'count': 4, 'crs': CRS.from_epsg(32610),
 'transform': Affine(5.0, 0.0, 523500.0, 0.0, -5.0, 4536500.0),
 'tiled': False, 'compress': 'lzw', 'interleave': 'pixel'}
>>> r = requests.post(endpoint, files={'file': open('redding1.tiff', 'rb')})
...   #doctest:+SKIP
>>> rasterio.io.MemoryFile(r.content).open().read(1).max() +  1
...   #doctest:+SKIP
172859
"""
import numpy as np
import rasterio
import requests

import doctest
doctest.testmod()
