#!/bin/bash
set -euo pipefail

echo "=== Provisioning GATEWAY ===";
apt-get update && apt-get install -y python3-pip python3-venv
cat > /home/vagrant/api-gateway/.env << EOF
GATEWAY_HOST=$GATEWAY_HOST
GATEWAY_PORT=$GATEWAY_PORT
GATEWAY_DEBUG=$GATEWAY_DEBUG
INVENTORY_SERVICE_URL=$INVENTORY_SERVICE_URL
EOF
chown vagrant:vagrant /home/vagrant/api-gateway/.env

# Setup PM2
sudo apt-get install -y nodejs npm
sudo npm install pm2 -g

# Setup service
cd /home/vagrant/api-gateway
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo -u vagrant pm2 delete api-gateway || true
sudo -u vagrant pm2 start server.py --name "api-gateway" --interpreter ./.venv/bin/python3
sudo pm2 startup systemd -u vagrant --hp /home/vagrant
sudo -u vagrant pm2 save