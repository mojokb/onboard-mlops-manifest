#! /bin/bash
sudo docker build -t brightfly/make-dataset:latest .
sudo docker push  brightfly/make-dataset:latest