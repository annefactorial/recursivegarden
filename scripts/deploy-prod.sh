#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Copy server config files and reload/restart server services
./scripts/deploy-server-config.sh root@labyrinth.love

# Do Django deployment on the remote server
cat ./scripts/deploy-django.sh | ssh recursivegarden@labyrinth.love /bin/bash
