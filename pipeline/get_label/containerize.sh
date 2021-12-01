#!/bin/bash

sudo docker build -t brightfly/get-label:latest .
sudo docker push brightfly/get-label:latest
