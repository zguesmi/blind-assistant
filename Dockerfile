FROM python:3-slim

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt --no-cache-dir && rm /requirements.txt

COPY src /src
COPY docker-entrypoint /docker-entrypoint

ENTRYPOINT [ "/docker-entrypoint" ]
CMD [ "INFO" ]
