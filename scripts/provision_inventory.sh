#!/bin/bash
set -e

echo "=== Provisioning inventory ==="

# Update and install dependencies
apt-get update
apt-get install -y python3-pip python3-venv postgresql postgresql-contrib

#[############################################################################]
# Setup PostgreSQL
systemctl start postgresql
systemctl enable postgresql
#[----------------------------------------------------------------------------]
# Setup PostgreSQL (Create database and user)
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname = 'mv_user';" |
grep -q 1 || \
sudo -u postgres psql -c "CREATE USER mv_user WITH PASSWORD 'password';"

sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'movies_db';" |
grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE movies_db OWNER mv_user;"
#[############################################################################]



#[############################################################################]
# Setup PM2
sudo apt-get install -y nodejs npm
sudo npm install pm2 -g
#[############################################################################]




#[############################################################################]
# 1. Prepare the application folder
cd /home/vagrant/inventory-app
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

pm2 delete inventory-api || true
pm2 start server.py --name "inventory-api" --interpreter ./.venv/bin/python3
pm2 save
#[############################################################################]




#[############################################################################]
# Setup firewall
sudo ufw --force enable
sudo ufw allow from "$GATEWAY_IP" to any port "$INVENTORY_PORT"
#[############################################################################]
