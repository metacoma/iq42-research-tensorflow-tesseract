#!/bin/bash

source ./env

docker build -t ${IMAGE_NAME} -f Dockerfile .
