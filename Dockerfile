FROM metacoma/east:bionic
ENV PYTHONIOENCODING utf-8
RUN apt-get update
RUN apt-get install -y --no-install-recommends --no-upgrade\
											tesseract-ocr\
											tesseract-ocr-rus
RUN pip3 install pillow pytesseract opencv-python imutils
