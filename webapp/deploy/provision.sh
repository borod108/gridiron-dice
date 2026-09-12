#!/usr/bin/env bash
# Create the EC2 instance, security group, key pair and Elastic IP for the
# Rick web app, then push the app.  Idempotent-ish: re-running reuses the
# security group / key pair and refuses to create a second instance if one is
# recorded in deploy/.state.
#
# Requires: aws CLI v2 logged in (aws login), ssh, scp, tar.
set -euo pipefail
cd "$(dirname "$0")"
REGION=${AWS_REGION:-us-east-1}
NAME=rick-web
INSTANCE_TYPE=${INSTANCE_TYPE:-t3.micro}
KEY_NAME=${NAME}-key
KEY_FILE=$HOME/.ssh/${KEY_NAME}.pem
STATE=.state
ENVF=.env

aws() { command aws --region "$REGION" --output text "$@"; }

if [ -f "$STATE" ] && grep -q '^INSTANCE_ID=' "$STATE"; then
  echo "Instance already recorded in $STATE; use push.sh to update or teardown.sh first."; exit 1
fi

# --- app password (kept locally in deploy/.env, chmod 600)
if [ ! -f "$ENVF" ]; then
  printf 'RICK_USER=rick\nRICK_PASSWORD=%s\n' "$(openssl rand -base64 18 | tr -d '/+=' | cut -c1-20)" > "$ENVF"
  chmod 600 "$ENVF"
fi

# --- key pair
if ! aws ec2 describe-key-pairs --key-names "$KEY_NAME" >/dev/null 2>&1; then
  aws ec2 create-key-pair --key-name "$KEY_NAME" --key-type ed25519 --query KeyMaterial > "$KEY_FILE"
  chmod 600 "$KEY_FILE"
  echo "created key pair $KEY_NAME -> $KEY_FILE"
fi
[ -f "$KEY_FILE" ] || { echo "key pair exists in AWS but $KEY_FILE is missing"; exit 1; }

# --- VPC / security group
VPC_ID=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true --query 'Vpcs[0].VpcId')
SG_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=${NAME}-sg Name=vpc-id,Values=$VPC_ID --query 'SecurityGroups[0].GroupId' 2>/dev/null || true)
if [ -z "$SG_ID" ] || [ "$SG_ID" = "None" ]; then
  SG_ID=$(aws ec2 create-security-group --group-name ${NAME}-sg --description "rick web app" --vpc-id "$VPC_ID" --query GroupId)
  aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80 --cidr 0.0.0.0/0 >/dev/null
  echo "created security group $SG_ID (80 open to the world)"
fi
MYIP=$(curl -s https://checkip.amazonaws.com)/32
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr "$MYIP" >/dev/null 2>&1 || true
echo "ssh allowed from $MYIP"

# --- AMI: latest Ubuntu 24.04 LTS
AMI=$(aws ssm get-parameter --name /aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id --query Parameter.Value)

# --- instance
INSTANCE_ID=$(aws ec2 run-instances --image-id "$AMI" --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" --security-group-ids "$SG_ID" \
  --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=16,VolumeType=gp3}' \
  --user-data file://user-data.sh \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NAME},{Key=Project,Value=rick}]" \
  --query 'Instances[0].InstanceId')
echo "INSTANCE_ID=$INSTANCE_ID" > "$STATE"
echo "SG_ID=$SG_ID" >> "$STATE"
echo "launched $INSTANCE_ID ($INSTANCE_TYPE, $AMI)"
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

# --- elastic IP so the address survives stop/start
ALLOC_ID=$(aws ec2 allocate-address --domain vpc --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=Name,Value=$NAME},{Key=Project,Value=rick}]" --query AllocationId)
aws ec2 associate-address --instance-id "$INSTANCE_ID" --allocation-id "$ALLOC_ID" >/dev/null
IP=$(aws ec2 describe-addresses --allocation-ids "$ALLOC_ID" --query 'Addresses[0].PublicIp')
echo "ALLOC_ID=$ALLOC_ID" >> "$STATE"
echo "IP=$IP" >> "$STATE"
echo "elastic IP $IP"

echo "waiting for ssh..."
for i in $(seq 1 40); do
  ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 -i "$KEY_FILE" ubuntu@"$IP" true 2>/dev/null && break
  sleep 5
done
./push.sh
