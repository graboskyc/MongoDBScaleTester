FROM locustio/locust
WORKDIR /tmp/locust 
COPY locustfile.py ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
EXPOSE 8089 