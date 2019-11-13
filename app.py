"""
Google Cloud Run serverless deployment of BIS API by James

Berkeley Image Seg is a region merging image object segmentation algorithm
Give it multiband satellite imagery and it returns an int image labeled with object IDs
Using Cloud Run because the core algorithm is Cython compiled to an so/pyd file
www.imageseg.com  jscar@berkenviro.com

The Google Cloud Run tutorial
https://cloud.google.com/run/docs/quickstarts/build-and-deploy

Admin page
https://console.cloud.google.com/run?authuser=1&project=graphite-proton-825

Mapped api.imageseg.com subdomain managed by wix.com to Cloud Run
https://cloud.google.com/run/docs/mapping-custom-domains
https://www.google.com/webmasters/verification/home?hl=en&authuser=1
On Wix console set CNAME from api.imageseg.com to ghs.googlehosted.com
"""
import os, json
from flask import Flask, Response, request, jsonify, send_file
from tempfile import NamedTemporaryFile
import numpy as np
import rasterio
from rasterio.profiles import DefaultGTiffProfile

CLOUD = bool(os.environ.get('K_SERVICE', None))
if CLOUD:
    "Google Cloud Run per reserved environment variable"
    from cregionmerge_ubuntu18_04_64bit_py36_20190309 import cregionmerge
else:
    "Local Mac development and corresponding binary"
    from cregionmerge_macos10_15_64bit_py37_20191025 import cregionmerge

app = Flask(__name__)


@app.route('/v1/segment', methods=['GET', 'POST'])
def entry():
    """Web wrapper for segmentation call into BIS."""
    wasfile = False
    if 'file' in request.files:
        wasfile = True
        f = request.files['file']
        filename = f.name
        tmpname = NamedTemporaryFile().name
        f.save(tmpname)
        dataset = rasterio.open(tmpname)
        array = dataset.read()
        os.remove(tmpname)
    elif 'url' in request.args:
        wasfile = True
        filename = request.args.get('url')
        dataset = rasterio.open(filename)
        array = dataset.read()
    elif request.json:
        array = request.json
    else:
        array = request.args.get('array')
        if not array:
            raise ValueError("Send image as file data, json data, "
                             "url parameter, or array parameter")
        array = json.loads(array)
    regions = segment(np.asarray(array))
    if wasfile:
        new = DefaultGTiffProfile(count=1)
        old = dataset.profile
        new['height'], new['width'] = dataset.shape
        new['crs'] = old['crs']
        new['transform'] = old['transform']
        new['dtype'] = regions.dtype
        memfile = rasterio.io.MemoryFile()
        memfile.open(**new).write(regions, 1)
        return send_file(memfile,
                         attachment_filename=filename + '_10_05_05.tif',
                         mimetype='image/tiff')
    else:
        return jsonify(regions.tolist())


def segment(array, t=10, s=0.5, c=0.5, nd=False, ndv=0):
    """BIS API segmentation call.

    >>> segment(np.array([[[1]], [[1]], [[1]]])) # One pixel, three band
    array([[0]], dtype=int32)

    >>> array = rasterio.open('img/agé.bmp').read()  # Plain RGB image
    >>> array.shape  # nbands, height, width
    (3, 127, 212)
    >>> array  # doctest:+ELLIPSIS
    array([[[154, 151, 160, ..., 152, 152, 255],
    ...
            [ 57,  61,  64, ...,  55,  61,  56]]], dtype=uint8)
    >>> regions = segment(array)
    >>> regions.shape
    (127, 212)
    >>> regions  # doctest:+ELLIPSIS
    array([[310, 310, 310, ..., 328, 328, 336],
    ...
           [  0,   0,   0, ...,  20,  20,  20]], dtype=int32)
    >>> regions.max() + 1  # Total number of image objects / labels / IDs
    338
    """
    array = array.transpose(1, 2, 0)  # BIS wants pixel interleaved
    height, width, nbands = array.shape
    size = height * width
    merger = cregionmerge.cmerger(array, size, width, height, nbands, s, c,
                                  nodata=nd, nd_val=ndv)
    regions = np.zeros((height, width), dtype=np.int32)
    merger.merge(t, regions)
    return regions


@app.route('/v1/test')
def test():
    """Trivial handling of a request with parameters / first function."""
    array = request.args.get('array', '[[0,0,0]]')
    add = request.args.get('add', '0')
    answer = np.array(json.loads(array)) + float(add)
    return _debug(answer)


@app.route('/')
def root():
    """Lay bare the source code as the help!"""
    files = ['examples.py', 'app.py', 'Dockerfile', '.dockerignore', 'deploy.zsh']
    s = '\n\n'.join([f + ':\n--------------\n' + open(f).read() for f in files])
    s += '\n\nTest image available from https://api.imageseg.com/agé.bmp\n'
    return _debug(s)


@app.route('/agé.bmp')
def ag():
    """Serve up this one file for user testing"""
    return send_file('agé.bmp')


def _debug(answer):
    body = f"{answer}\n\n{request.args}\nOn cloud: {CLOUD}"
    return Response(body, mimetype='text/plain')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
