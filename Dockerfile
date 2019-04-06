FROM ubuntu:bionic
ENV PYTHONIOENCODING utf-8
RUN apt-get update
RUN apt-get install -y --no-install-recommends --no-upgrade\
                      python3-minimal\
                      python3-pip\
											libsm6\
											libxext6\
											libglib2.0-0\
											libxrender1\
											tesseract-ocr\
											tesseract-ocr-rus\
											cython3
ADD requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app/
RUN pip3 install setuptools
RUN pip3 install -r requirements.txt
RUN apt install -y --no-install-recommends --no-upgrade gcc python3-dev
ADD text-detection-ctpn/requirements.txt /opt/app/text-detection-ctpn/requirements.txt
WORKDIR /opt/app/text-detection-ctpn
RUN pip3 install -r requirements.txt
#RUN ln -s /usr/lib/x86_64-linux-gnu/libcublas.so.7.5 /usr/lib/x86_64-linux-gnu/libcublas.so.8.0
#RUN ln -s /usr/lib/x86_64-linux-gnu/libcusolver.so.7.5 /usr/lib/x86_64-linux-gnu/libcusolver.so.8.0
#RUN apt-get install -y --no-install-recommends --no-upgrade libcublas9.1 libcusolver9.1 libcudart9.1 libcuda1-340 libcupti-dev
#RUN ln -s /usr/lib/x86_64-linux-gnu/libcublas.so.9.1 /usr/lib/x86_64-linux-gnu/libcublas.so.8.0
#RUN ln -s /usr/lib/x86_64-linux-gnu/libcusolver.so.9.1 /usr/lib/x86_64-linux-gnu/libcusolver.so.8.0
#RUN ln -s /usr/lib/x86_64-linux-gnu/libcudart.so.9.1 /usr/lib/x86_64-linux-gnu/libcudart.so.8.0
