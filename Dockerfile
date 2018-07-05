FROM ubuntu:16.04

COPY requirements.txt /blind-assistant/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      && \
    pip3 install -r /blind-assistant/requirements.txt --no-cache-dir && \
    rm /blind-assistant/requirements.txt && \
    apt-get remove -y --autoremove python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY src /blind-assistant
COPY docker-entrypoint /blind-assistant/docker-entrypoint

ENTRYPOINT [ "/blind-assistant/docker-entrypoint" ]
CMD [ "INFO" ]
