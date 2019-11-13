# Satellite Image Segmentation - REST API

Berkeley Image Seg is a region merging image object segmentation algorithm  
Give it multiband satellite imagery and it returns an int image labeled with object IDs  

See [examples.py](examples.py) for how to call the service, the [Jupyter notebook](examples.ipynb) doing a basic classification on resulting image objects, and [app.py](app.py) is the Flask server itself

Make REST calls to api.imageseg.com per the examples  
Visit [api.imageseg.com](https://api.imageseg.com) in your browser and it will show you this repo's source code  

This is a REST API deployed serverless to Google Cloud Run  
Using Cloud Run because the core algorithm is Cython compiled to an so/pyd file  
The Google Cloud Run startup details are below

The Google Cloud Run tutorial  
https://cloud.google.com/run/docs/quickstarts/build-and-deploy

Admin page  
https://console.cloud.google.com/run?authuser=1&project=graphite-proton-825

Mapped api.imageseg.com subdomain managed by wix.com to Cloud Run  
https://cloud.google.com/run/docs/mapping-custom-domains  
https://www.google.com/webmasters/verification/home?hl=en&authuser=1  
On Wix console set CNAME from api.imageseg.com to ghs.googlehosted.com  

www.imageseg.com  
