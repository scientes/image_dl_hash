FROM python:3
ADD image_dl.py /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir images
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]