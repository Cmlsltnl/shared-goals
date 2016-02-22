#!/bin/bash
sudo yum install -y gcc libjpeg-devel zlib-devel

git clone https://github.com/mnieber/shared-goals.git
cd shared-goals

virtualenv env
source env/bin/activate
pip install --upgrade pip

pip install -r conf/REQUIREMENTS.txt

exit
