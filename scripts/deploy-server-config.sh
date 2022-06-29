#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ $# -eq 0 ]; then
    echo "No remote server specified"
    exit 1
fi

REMOTE_SERVER="$1"

# Copy all server config files to the server
scp config/nginx.conf "$REMOTE_SERVER:/etc/nginx/nginx.conf"
#scp config/certbot-renewal.service "$REMOTE_SERVER:/etc/systemd/system/certbot-renewal.service"
#scp config/certbot-renewal.timer "$REMOTE_SERVER:/etc/systemd/system/certbot-renewal.timer"
#scp config/recursivegarden.service "$REMOTE_SERVER:/etc/systemd/system/recursivegarden.service"

ssh "$REMOTE_SERVER" << ENDSSH
systemctl daemon-reload
systemctl restart certbot-renewal.service
systemctl restart certbot-renewal.timer
systemctl restart recursivegarden.service
systemctl reload nginx
ENDSSH

#ssh "$REMOTE_SERVER" << ENDSSH
#systemctl daemon-reload
#systemctl restart certbot-renewal.service
#systemctl restart certbot-renewal.timer
#systemctl restart recursivegarden.service
#systemctl reload nginx
#ENDSSH
