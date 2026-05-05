#!/bin/bash
set -euo pipefail

echo "=== Provisioning BILLING ===";
apt-get update -y && apt-get install -y python3-pip python3-venv curl gnupg 
apt-get install rabbitmq-server -y
sudo rabbitmqctl add_user billing_user billing_user
sudo rabbitmqctl set_permissions -p / billing_user ".*" ".*" ".*" 

# .env
cat > /home/vagrant/billing-app/.env << EOF
BILLING_HOST=$BILLING_HOST
BILLING_PORT=$BILLING_PORT
BILLING_DEBUG=$BILLING_DEBUG
EOF

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