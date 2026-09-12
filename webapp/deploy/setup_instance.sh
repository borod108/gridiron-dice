#!/usr/bin/env bash
# Runs ON the instance as root (piped in by push.sh).  Unpacks the app,
# builds the venv, installs the systemd unit, restarts.
set -euo pipefail
# wait for cloud-init (first boot) to finish installing python3-venv
cloud-init status --wait >/dev/null 2>&1 || true
id rick >/dev/null 2>&1 || useradd --system --create-home --home-dir /opt/rick --shell /usr/sbin/nologin rick
mkdir -p /opt/rick/app /opt/rick/data
rm -rf /opt/rick/app.new && mkdir -p /opt/rick/app.new
tar -xzf /tmp/rick-app.tgz -C /opt/rick/app.new
rm -rf /opt/rick/app && mv /opt/rick/app.new /opt/rick/app
install -m 600 /tmp/.env /opt/rick/env
rm -f /tmp/rick-app.tgz /tmp/.env
# seed sample teams the first time so the app is usable immediately
if [ -z "$(ls -A /opt/rick/data 2>/dev/null)" ]; then cp /opt/rick/app/sample_data/*.xlsx /opt/rick/data/; fi
[ -d /opt/rick/venv ] || python3 -m venv /opt/rick/venv
/opt/rick/venv/bin/pip install -q --upgrade pip
/opt/rick/venv/bin/pip install -q -r /opt/rick/app/requirements.txt
chown -R rick:rick /opt/rick
install -m 644 /opt/rick/app/deploy/rick-web.service /etc/systemd/system/rick-web.service
install -m 644 /opt/rick/app/deploy/rick-backup.service /etc/systemd/system/rick-backup.service
install -m 644 /opt/rick/app/deploy/rick-backup.timer /etc/systemd/system/rick-backup.timer
systemctl daemon-reload
systemctl enable rick-web >/dev/null
systemctl enable --now rick-backup.timer >/dev/null
systemctl restart rick-web
sleep 2
systemctl --no-pager --lines=5 status rick-web || true
curl -s -o /dev/null -w "local health check: HTTP %{http_code}\n" http://127.0.0.1/healthz || true
