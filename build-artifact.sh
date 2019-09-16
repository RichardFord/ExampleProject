#!/usr/bin/env bash

mkdir deployTemp

cd deployTemp
python3.7 -m venv .

source bin/activate
pip install sqlalchemy==1.2.15

curl -LO 'https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-8.0.11.tar.gz'
tar -xvzf mysql*tar*gz

cd mysql-connector-python-8.0.11
python setup.py install
cd ..

deactivate

cd lib/python3.7/site-packages
zip -r9 ../../../../deployment.zip *
cd ../../../../
zip -ur deployment.zip demo/
rm -rf deployTemp