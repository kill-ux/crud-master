#!/bin/bash
set -euo pipefail

echo "=== Provisioning BILLING SERVICE ===";

# 1. Install dependencies
apt-get update && apt-get install -y python3-pip python3-venv postgresql postgresql-contrib rabbitmq-server nodejs npm
sudo npm install pm2 -g

# 2. Create the .env file
# Note: Variables like $BILLING_HOST etc. are passed by Vagrant
cat > /home/vagrant/billing-app/.env << EOF
BILLING_HOST=$BILLING_HOST
BILLING_PORT=$BILLING_PORT
BILLING_DATABASE_URL=$BILLING_DATABASE_URL
RABBITMQ_HOST=$RABBITMQ_HOST
RABBITMQ_QUEUE=$RABBITMQ_QUEUE
RABBITMQ_USER=$RABBITMQ_USER
RABBITMQ_PASS=$RABBITMQ_PASS
EOF
chown vagrant:vagrant /home/vagrant/billing-app/.env

# 3. Setup PostgreSQL for Billing
systemctl start postgresql
systemctl enable postgresql

# Idempotent user and database creation
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname = 'billing_user';" | grep -q 1 || \
sudo -u postgres psql -c "CREATE USER billing_user WITH PASSWORD 'password';"

sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'orders';" | grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE orders OWNER billing_user;"

# 4. Setup RabbitMQ
systemctl start rabbitmq-server
systemctl enable rabbitmq-server

# Create a RabbitMQ user for the gateway (and app) to use
# Using 'guest'/'guest' is restricted to localhost by default
rabbitmqctl add_user rabbit_user password || true
rabbitmqctl set_user_tags rabbit_user administrator || true
rabbitmqctl set_permissions -p / rabbit_user ".*" ".*" ".*" || true

# 5. Firewall configuration
sudo ufw --force enable
sudo ufw allow OpenSSH
# Allow Gateway to access the Billing API and allow RabbitMQ traffic
sudo ufw allow from "$GATEWAY_IP" to any port "$BILLING_PORT"
sudo ufw allow from "$GATEWAY_IP" to any port 5672

# 6. PM2 and App setup
cd /home/vagrant/billing-app
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirement.txt

# Start the API server using PM2
sudo -u vagrant pm2 delete billing-api || true
sudo -u vagrant pm2 start server.py --name "billing-api" --interpreter ./.venv/bin/python3

# Setup PM2 to start on boot
sudo pm2 startup systemd -u vagrant --hp /home/vagrant
sudo -u vagrant pm2 save