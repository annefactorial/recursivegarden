#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

./manage.py render_nginx_conf | sudo tee /etc/nginx/nginx.conf > /dev/null

cat /etc/nginx/nginx.conf

echo 'Successfully wrote new nginx.conf to /etc/nginx/nginx.conf'

sudo nginx -t
sudo systemctl reload nginx
