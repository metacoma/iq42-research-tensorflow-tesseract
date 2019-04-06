#!/bin/bash

source ./env
export DATA_DIR=/data


docker run -p0.0.0.0:8080:80 --name boxes-python -e DATA_DIR --rm -it     \
    -v `pwd`:/opt/app                                                     \
    --tmpfs /${DATA_DIR}:rw,noexec,nosuid,size=65536k                     \
    ${IMAGE_NAME} /bin/bash
