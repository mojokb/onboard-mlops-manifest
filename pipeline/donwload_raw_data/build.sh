#! /bin/bash

sudo docker build -t brightfly/download-minio:latest .
sudo docker push  brightfly/download-minio:latest
