#!/bin/zsh
~/Downloads/google-cloud-sdk/bin/gcloud builds submit --tag gcr.io/graphite-proton-825/app
~/Downloads/google-cloud-sdk/bin/gcloud beta run deploy app --image gcr.io/graphite-proton-825/app --platform managed
