FROM metacoma/east:bionic
ENV PYTHONIOENCODING utf-8
RUN apt-get update
RUN apt-get install -y --no-install-recommends --no-upgrade\
											tesseract-ocr\
											tesseract-ocr-rus
                      python3-flask
RUN pip3 install pillow pytesseract opencv-python imutils flask requests_toolbelt multipart
ENV FLASK_APP /opt/east/iq42backend.py
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

