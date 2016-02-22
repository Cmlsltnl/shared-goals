#!/bin/bash
sudo yum install -y gcc libjpeg-devel zlib-devel

git clone https://github.com/mnieber/shared-goals.git
cd shared-goals

sed s#{{shared_goals}}#`pwd`#g conf/supervisord.conf.template > conf/supervisord.conf
sed s#{{shared_goals}}#`pwd`#g conf/shared_goals_nginx.conf.template > conf/shared_goals_nginx.conf

sudo mkdir /etc/nginx/sites-enabled
ln -s conf/sharedgoals_nginx.conf /etc/nginx/sites-enabled/

virtualenv env
source env/bin/activate
pip install --upgrade pip

pip install -r conf/REQUIREMENTS.txt


exit
