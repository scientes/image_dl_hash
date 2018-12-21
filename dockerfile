FROM python:3
ADD image_dl.py /
RUN pip install -r requirements.txt
RUN mkdir images
CMD ["python","./image_dl_hash.py"]
