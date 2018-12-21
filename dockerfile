FROM python:3
ADD image_dl.py /
RUN pip install pillow
RUN pip install imagehash
RUN pip install requests
RUN mkdir images
CMD ["python","./image_dl_hash.py"]
