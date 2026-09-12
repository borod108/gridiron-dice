#!/usr/bin/env bash
# Push the current webapp/ tree to the instance recorded in deploy/.state and
# (re)start the service.  Safe to re-run for every code change.
set -euo pipefail
cd "$(dirname "$0")"
source .state
KEY_FILE=$HOME/.ssh/rick-web-key.pem
SSH="ssh -o StrictHostKeyChecking=accept-new -i $KEY_FILE ubuntu@$IP"
tar --exclude='./data' --exclude='./deploy/.state' --exclude='./deploy/.env' --exclude='__pycache__' -czf /tmp/rick-app.tgz -C .. .
scp -o StrictHostKeyChecking=accept-new -i "$KEY_FILE" /tmp/rick-app.tgz .env ubuntu@"$IP":/tmp/
$SSH 'sudo bash -s' < setup_instance.sh
echo
echo "App is up at http://$IP/  (user and password in deploy/.env)"
