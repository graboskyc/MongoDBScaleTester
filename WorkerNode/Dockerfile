FROM locustio/locust
LABEL maintainer="chris@grabosky.net"
LABEL version="1.0.1"

WORKDIR /tmp/locust 
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
COPY ./locustfile.py ./
EXPOSE 8089 