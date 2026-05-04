#!/bin/bash
set -euo pipefail

echo "=== Provisioning GATEWAY ===";
apt-get update -y && apt-get install -y python3-pip python3-venv curl gnupg 
apt-get install rabbitmq-server -y