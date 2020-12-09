FROM locustio/locust
LABEL maintainer="chris@grabosky.net"
LABEL version="1.0.1"

WORKDIR /tmp/locust 
COPY locustfile.py ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
EXPOSE 8089 