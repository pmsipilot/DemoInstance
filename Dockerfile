FROM ubuntu:14.04
MAINTAINER PMSIpilot
RUN apt-get update && apt-get install git python python-dev\
 python-pip mysql-client libmysqlclient-dev nodejs npm\
  libldap2-dev libsasl2-dev libssl-dev -y
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower grunt-cli
RUN mkdir /opt/demoinstance 
COPY ./ /opt/demoinstance
WORKDIR /opt/demoinstance
RUN pip install -r requirements.txt
WORKDIR /opt/demoinstance/web
RUN npm install
RUN bower install --allow-root
RUN grunt
WORKDIR /opt/demoinstance/
VOLUME /opt/demoinstance/config.ini
VOLUME /opt/demoinstance/instance_image/
CMD python demo.py
EXPOSE 8080
