FROM python:2.7-alpine3.7

RUN apk update && \
    apk add openssh-client git unzip vim shadow

RUN useradd -ms /bin/bash user

WORKDIR /home/user

ADD . /home/user/env2consul

WORKDIR env2consul

RUN pip install -r requirements.txt && \
    chown user:user /home/user -R

USER user

RUN mkdir $HOME/.env2consul && \
    mkdir $HOME/.env2consul/devops-env2consul && \
    mkdir $HOME/.ssh && \
    ssh-keyscan -t rsa github.com >> $HOME/.ssh/known_hosts

CMD ["python", "server.py"]
