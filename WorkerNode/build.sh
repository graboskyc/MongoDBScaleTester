#!/bin/bash

echo
echo "+======================"
echo "| START: LOCUST"
echo "+======================"
echo


echo 
echo "LOCUST: Building container"
echo
docker build -t graboskyc/mongodb-locust-scale:buckets .

echo 
echo "LOCUST: Starting container"
echo
docker stop locbldctr
docker rm locbldctr
docker run -t -i -d -p 8888:8888 --name locbldctr --restart unless-stopped -e token="localdev" graboskyc/mongodb-locust-scale:buckets

echo
echo "+======================"
echo "| END: LOCUST"
echo "+======================"
echo
