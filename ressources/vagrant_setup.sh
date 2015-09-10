#!/bin/bash

sudo apt-get update
sudo apt-get install -y nginx python-pip supervisor python-dev libldap2-dev libsasl2-dev libmysqlclient-dev screen nodejs npm
(cd /opt/demoinstance/backend && sudo python setup.py install)
sudo cp /opt/demoinstance/ressources/supervisor_dev/*.conf /etc/supervisor/conf.d/
cp /opt/demoinstance/ressources/dev_demoinstance /opt/demoinstance/dev_demoinstance
cp /opt/demoinstance/ressources/dev_demoinstance.py /opt/demoinstance/dev_demoinstance.py
sudo /etc/init.d/nginx stop
sudo /etc/init.d/supervisor stop
sudo rm -f /var/run/supervisor.sock
sudo rm -f /etc/nginx/sites-enabled/default
sudo cp /opt/demoinstance/ressources/nginx/nginx-server /etc/nginx/sites-enabled/default
sudo cp -R /opt/demoinstance/config /etc/demoinstance
sudo ln -s /usr/bin/nodejs /usr/bin/node
screen -S log -d -m sudo /usr/bin/supervisord -c /etc/supervisor/supervisord.conf

