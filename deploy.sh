#!/usr/bin/env bash


echo "apt-get update"
sudo apt-get update

echo "install nginx"
sudo apt-get install nginx

echo "copy files to nginx directory"
sudo cp -r html/* /var/www/html/

echo "END"