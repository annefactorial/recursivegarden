#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Copy server config files and reload/restart server services
./scripts/deploy-server-config.sh root@localhost

cat ./config/deploy-django.sh | ssh recursivegarden@localhost /bin/bash
