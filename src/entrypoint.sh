#!/bin/sh
set -exu

eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa_storage
ssh-add -l

if [ "$LOCAL_DEVELOPMENT_MODE" = "on" ]; then
  # Start flask in development mode
  FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=True flask run --host 0.0.0.0 --port 5000
else
  # Start gunicorn, listening on port 500, access log to stdout
  exec gunicorn -w 4 -b '0.0.0.0:5000' --access-logfile=- 'app:app'
fi
