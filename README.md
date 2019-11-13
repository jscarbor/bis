# Satellite Image Segmentation - REST API

Berkeley Image Seg is a region merging image object segmentation algorithm  
Give it multiband satellite imagery and it returns an int image labeled with object IDs  

See [app.py](app.py) as the Flask server, [examples.py](examples.py) as doctests calling the server, and the [Jupyter notebook](examples.ipynb) doing a basic classification on resulting image objects

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
jscar@berkenviro.com  
