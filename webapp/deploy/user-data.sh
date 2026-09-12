#!/bin/bash
# Cloud-init: base packages only; the app itself is pushed over ssh by push.sh
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3-venv python3-pip
id rick >/dev/null 2>&1 || useradd --system --create-home --home-dir /opt/rick --shell /usr/sbin/nologin rick
mkdir -p /opt/rick/app /opt/rick/data
chown -R rick:rick /opt/rick
