FROM python:3
ADD image_dl.py /
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV PYTHONPATH='/src/:$PYTHONPATH'

COPY entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
