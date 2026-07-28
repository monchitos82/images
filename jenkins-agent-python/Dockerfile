FROM jenkins/inbound-agent:latest
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv pandoc && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/deploy && \
    chown jenkins:jenkins /opt/deploy && \
    chmod 777 /opt/deploy

USER jenkins
