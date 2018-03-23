FROM python:2.7-alpine3.7

RUN mkdir /home/user

WORKDIR /home/user

RUN apk update && apk add git

ADD https://github.com/dkorel-copperleaf/env2consul/archive/master.zip .
RUN unzip master.zip

WORKDIR /home/user/env2consul-master

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
