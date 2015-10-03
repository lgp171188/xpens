#!/bin/bash

set -e

cd ~vagrant/xpens

apt-get update
apt-get -y -q upgrade

export LC_ALL="en_US.UTF-8"
locale-gen en_US.UTF-8

apt-get install -y -q git build-essential linux-headers-amd64 libpython-dev\
        virtualenvwrapper postgresql libpq-dev libjpeg-dev libfreetype6-dev\
        libpng-dev editorconfig iceweasel

sudo -H -u postgres -s -- <<EOF
createuser -d xpens
createdb -O xpens xpens
psql -c "ALTER USER xpens WITH PASSWORD 'xpens';"
EOF

sudo -H -u vagrant -s -- <<EOF
mkdir ~/.venvs
export WORKON_HOME=~/.venvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv xpens-py2.7
cd ~/xpens
pip install -r requirements/local.txt
cd xpens
cp xpens/settings{_template,}.py

python manage.py migrate --noinput

echo "export WORKON_HOME=~/.venvs" >> ~/.bashrc
echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
echo "workon xpens-py2.7" >> ~/.bashrc
EOF
