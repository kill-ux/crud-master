#!/bin/bash
set -e

echo "=== Provisioning inventory ==="

# Update and install dependencies
apt-get update
apt-get install -y python3-pip python3-venv postgresql postgresql-contrib

systemctl start postgresql
systemctl enable postgresql

# Setup PostgreSQL (Create database and user)
sudo -u postgres psql -c "CREATE USER IF NOT EXISTS mv_user PASSWORD 'password';" 2>/dev/null || true
sudo -u postgres createdb --owner=mv_user movies_db 2>/dev/null || true


# Setup PM2
sudo apt-get install -y nodejs npm
sudo npm install pm2 -g

# 1. Prepare the application folder
# cd 