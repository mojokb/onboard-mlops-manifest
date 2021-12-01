#!/bin/bash

sudo docker build -t brightfly/upload-minio:latest .
sudo docker push brightfly/upload-minio:latest