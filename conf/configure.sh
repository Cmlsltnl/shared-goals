#!/bin/bash
sudo yum install -y gcc libjpeg-devel zlib-devel

git clone https://github.com/mnieber/shared-goals.git
cd shared-goals

sed s#{{shared_goals}}#`pwd`#g conf/supervisord.conf.template > conf/supervisord.conf
sed s#{{shared_goals}}#`pwd`#g conf/sharedgoals_nginx.conf.template > conf/sharedgoals_nginx.conf

mkdir log
mkdir static
mkdir media

sudo mkdir /etc/nginx/sites-enabled
sudo ln -s `pwd`/conf/sharedgoals_nginx.conf /etc/nginx/sites-enabled/

virtualenv env
source env/bin/activate
pip install --upgrade pip

pip install -r conf/REQUIREMENTS.txt

cd src
python manage.py collectstatic --noinput

exit
