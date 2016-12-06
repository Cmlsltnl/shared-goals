#!/bin/bash
sudo usermod -g nginx -G ec2-user,wheel

# TODO set default file permissions such that nginx can execute
# also on /home and /home/ec2-user!

# TODO add IP to ALLOWED_HOSTS in settings.py

sudo yum install -y gcc libjpeg-devel zlib-devel nginx git
sudo yum install postgresql94 postgresql94-server postgresql94-libs postgresql94-contrib postgresql94-devel

git clone https://github.com/mnieber/shared-goals.git
chmod -R g+w shared-goals/
cd shared-goals

sed s#{{shared_goals}}#`pwd`#g conf/supervisord.conf.template > conf/supervisord.conf
sed s#{{shared_goals}}#`pwd`#g conf/sharedgoals_nginx.conf.template > conf/sharedgoals_nginx.conf

mkdir log
mkdir static
mkdir media

sudo ln -s `pwd`/conf/sharedgoals_nginx.conf /etc/nginx/conf.d/

virtualenv env
source env/bin/activate
pip install --upgrade pip
pip install -r conf/REQUIREMENTS.txt

# TODO set superuser

cd src
python manage.py collectstatic --noinput

# TODO run migrate

exit
