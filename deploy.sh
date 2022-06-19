#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

cd /home/recursivegarden/

# Clone the repo if it isn't already
if [ ! -d /home/recursivegarden/recursivegarden/ ]; then
    echo 'Cloning git repo'
    # Set the origin to 'github' so we can `git pull github main`
    git clone --origin github git@github.com:annefactorial/recursivegarden.git
else
    echo 'Git repo already initialized'
fi

# Check out the latest master branch
cd /home/recursivegarden/recursivegarden/
git fetch github
git checkout github/main

# Create the virtualenv if it doesn't exist
if [ ! -d env ]; then
    echo 'Creating virtualenv'
    virtualenv env
else
    echo 'Updating virtualenv'
fi
source env/bin/activate
pip install -r requirements/production.txt
echo 'Restarting systemd service'
yes yes | /home/recursivegarden/recursivegarden/env/bin/python manage.py collectstatic
sudo systemctl restart recursivegarden
