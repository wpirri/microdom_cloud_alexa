#!/bin/sh

docker build -t microdom-cloud-alexa:latest .
docker tag microdom-cloud-alexa:latest ghcr.io/wpirri/microdom-cloud-alexa:latest
docker push ghcr.io/wpirri/microdom-cloud-alexa:latest

