#!/usr/bin/env bash
echo "User 'postgres' password:"
pg_dump -Fc --no-acl --no-owner -h localhost -U postgres ernirnet > /home/ernir/Dropbox/Public/ernirnet.dump
heroku run python manage.py migrate
echo "Waiting for upload"
sleep 5
heroku pg:backups restore 'http://dl.dropboxusercontent.com/u/19444168/ernirnet.dump' DATABASE -a ernirnet --confirm ernirnet
