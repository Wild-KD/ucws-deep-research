#!/bin/bash
# Deploy Investment Research Engine to Aliyun server
# Run this ON the server, not locally.
#
# First-time setup:
#   1. SSH into server
#   2. git clone https://github.com/Wild-KD/investment-research-engine.git /opt/investment-engine
#   3. cd /opt/investment-engine
#   4. cp .env.example .env && nano .env  (fill in API keys)
#   5. bash deploy/deploy.sh
#
# Subsequent deploys:
#   cd /opt/investment-engine && bash deploy/deploy.sh

set -e

echo "=== Investment Research Engine Deploy ==="

cd /opt/investment-engine

# Pull latest code
echo "[1/5] Pulling latest code..."
git pull origin main

# Install Python dependencies
echo "[2/5] Installing Python dependencies..."
pip3 install -r requirements.txt --quiet

# Create directories
echo "[3/5] Creating directories..."
mkdir -p uploads output

# Load env
echo "[4/5] Loading environment..."
set -a
source .env
set +a

# Start/restart with PM2
echo "[5/5] Starting service on port ${PORT:-9001}..."
if pm2 describe investment-engine > /dev/null 2>&1; then
    pm2 restart investment-engine
else
    pm2 start deploy/ecosystem.config.js
fi

echo ""
echo "=== Deploy complete ==="
echo "Service: http://localhost:${PORT:-9001}"
echo "Public:  https://www.askmbb.com/investment/"
echo ""
echo "Don't forget to add the nginx location block if first deploy:"
echo "  See deploy/nginx-investment.conf"
echo "  sudo nginx -t && sudo systemctl reload nginx"
