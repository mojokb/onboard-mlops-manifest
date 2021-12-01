#!/bin/bash

kubectl -n argo port-forward $(kubectl -n argo get pod -l eventsource-name=webhook -o name) 12000:12000 &
curl -d '{"bucket_name":"torch-raw-images", "object_prefix":"20211128-163614/"}' -H "Content-Type: application/json" -X POST http://localhost:12000/example
kill -9 %1
