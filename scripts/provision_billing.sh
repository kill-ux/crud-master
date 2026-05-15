#!/bin/bash
set -euo pipefail

echo "=== Provisioning BILLING SERVICE ===";

# 1. Install dependencies (adds rabbitmq-server to your standard list)
apt-get update && apt-get install -y python3-pip python3-venv postgresql postgresql-contrib rabbitmq-server

# 2. Create the .env file (ensure these variables match your app logic)
cat > /home/vagrant/billing-app/.env << EOF
BILLING_HOST=$BILLING_HOST
BILLING_PORT=$BILLING_PORT
BILLING_DATABASE_URL=$BILLING_DATABASE_URL
RABBITMQ_HOST=localhost
EOF
chown vagrant:vagrant /home/vagrant/billing-app/.env

# 3. Setup PostgreSQL for Billing
systemctl start postgresql
systemctl enable postgresql
sudo -u postgres psql -c "CREATE USER billing_user WITH PASSWORD 'billing_pass';"
sudo -u postgres psql -c "CREATE DATABASE billing_db OWNER billing_user;"

# 4. Setup RabbitMQ
systemctl start rabbitmq-server
systemctl enable rabbitmq-server

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
pip install -r requirements.txt

# Start both the API server and the background worker
sudo -u vagrant pm2 start server.py --name "billing-api" --interpreter ./.venv/bin/python3