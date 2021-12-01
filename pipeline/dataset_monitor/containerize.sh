#!/bin/bash

sudo docker build -t 192.168.64:5:30000/dataset-minitor:latest .
sudo docker push 192.168.64.5:30000/dataset-monitor:latest