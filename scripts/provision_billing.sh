#!/bin/bash
set -euo pipefail

echo "=== Provisioning BILLING ===";
apt-get update -y && apt-get install -y python3-pip python3-venv curl gnupg 
apt-get install rabbitmq-server -y

# Setup PM2
sudo apt-get install -y nodejs npm
sudo npm install pm2 -g

# Setup service
cd /home/vagrant/billing-app
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo -u vagrant pm2 delete api-billing || true
sudo -u vagrant pm2 start server.py --name "api-billing" --interpreter ./.venv/bin/python3
sudo pm2 startup systemd -u vagrant --hp /home/vagrant
sudo -u vagrant pm2 save