FROM flink:1.19

USER root
RUN apt-get update
RUN apt-get install -y vim unzip openjdk-17-jdk
RUN apt-get install -y build-essential cmake make gcc g++ 
RUN apt-get install -y python3 python3-pip python3-arrow python3-numpy
RUN ln -s /usr/bin/python3 /usr/bin/python
