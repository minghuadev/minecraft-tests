#!/bin/bash

MY_IP=$(ifconfig | grep 'inet ' | grep -v 127\. | grep -v \.0\.1 | sed -e 's/[\t ][\t ]*/ /g' | cut -d' ' -f3)
docker run -d -p 5080:80 --restart=always  \
  -e REGISTRY_URL="http://${MY_IP}:5000" \
  --name registryui joxit/docker-registry-ui:static

