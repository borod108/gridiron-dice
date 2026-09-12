#!/usr/bin/env bash
# Terminate the instance and release the Elastic IP recorded in deploy/.state.
# Leaves the security group and key pair in place (free).  DATA ON THE
# INSTANCE IS LOST - download anything you need from the Files page first.
set -euo pipefail
cd "$(dirname "$0")"
source .state
REGION=${AWS_REGION:-us-east-1}
aws --region "$REGION" ec2 terminate-instances --instance-ids "$INSTANCE_ID" --output text >/dev/null
aws --region "$REGION" ec2 wait instance-terminated --instance-ids "$INSTANCE_ID"
aws --region "$REGION" ec2 release-address --allocation-id "$ALLOC_ID"
rm -f .state
echo "terminated $INSTANCE_ID and released $IP"
