#!/bin/bash
set -euo pipefail

echo "=== Provisioning INVENTOR ===";
apt-get update && apt-get install -y python3-pip python3-venv postgresql postgresql-contrib
cat > /home/vagrant/inventory-app/.env << ENF
INVENTORY_HOST=$INVENTORY_HOST
INVENTORY_PORT=$INVENTORY_PORT
INVENTORY_MOVIES_DATABASE_URL=$INVENTORY_MOVIES_DATABASE_URL
INVENTORY_DEBUG=$INVENTORY_DEBUG
ENF
chown vagrant:vagrant /home/vagrant/inventory-app/.env


# Setup firewall
sudo ufw --force enable
sudo ufw allow OpenSSH
sudo ufw allow from "$GATEWAY_IP" to any port "$INVENTORY_PORT"


# Setup PostgreSQL
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname = 'mv_user';" |
grep -q 1 || \
sudo -u postgres psql -c "CREATE USER mv_user WITH PASSWORD 'password';"

sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'movies_db';" |
grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE movies_db OWNER mv_user;"


# Setup PM2
sudo apt-get install -y nodejs npm
sudo npm install pm2 -g

# Setup service
cd /home/vagrant/inventory-app
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo -u vagrant pm2 delete api-inventory || true
sudo -u vagrant pm2 start server.py --name "api-inventory" --interpreter ./.venv/bin/python3
sudo -u vagrant pm2 save