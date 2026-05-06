#!/bin/bash
set -euo pipefail

echo "=== Provisioning BILLING ===";
apt-get update -y && apt-get install -y python3-pip python3-venv curl gnupg postgresql
apt-get install rabbitmq-server -y
sudo rabbitmqctl list_users | grep '^billing_user\s' || \
sudo rabbitmqctl add_user billing_user password
sudo rabbitmqctl set_permissions -p / billing_user ".*" ".*" ".*"

# .env
cat > /home/vagrant/billing-app/.env << EOF
BILLING_HOST=$BILLING_HOST
BILLING_PORT=$BILLING_PORT
BILLING_DEBUG=$BILLING_DEBUG
RABBITMQ_HOST=$RABBITMQ_HOST
RABBITMQ_PORT=$RABBITMQ_PORT
RABBITMQ_USERNAME=$RABBITMQ_USERNAME
RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD
RABBITMQ_QUEUE=$RABBITMQ_QUEUE
BILLING_DATABASE_URL=$BILLING_DATABASE_URL
EOF

# Setup Postgressql 
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname = 'billing_user';" | grep -q 1 || \
sudo -u postgres psql -c "CREATE USER billing_user WITH PASSWORD 'password';"

sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'billing_db';" | grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE billing_db OWNER billing_user;"

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