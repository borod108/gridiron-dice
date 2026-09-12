#!/usr/bin/env bash
# One-time: create a private S3 bucket and an instance role that can write to
# it, attach the role to the running instance, record the bucket in .env and
# redeploy.  Re-runnable.
set -euo pipefail
cd "$(dirname "$0")"
source .state
REGION=${AWS_REGION:-us-east-1}
aws() { command aws --region "$REGION" --output text "$@"; }
ACCOUNT=$(aws sts get-caller-identity --query Account)
BUCKET=${RICK_BACKUP_BUCKET:-gridiron-dice-backup-$ACCOUNT}
ROLE=rick-web-role

if ! aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  aws s3api create-bucket --bucket "$BUCKET" >/dev/null   # us-east-1 needs no LocationConstraint
  aws s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
  echo "created private bucket $BUCKET"
fi

if ! aws iam get-role --role-name "$ROLE" >/dev/null 2>&1; then
  aws iam create-role --role-name "$ROLE" --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}' >/dev/null
  echo "created role $ROLE"
fi
aws iam put-role-policy --role-name "$ROLE" --policy-name s3-backup --policy-document "{\"Version\":\"2012-10-17\",\"Statement\":[
  {\"Effect\":\"Allow\",\"Action\":[\"s3:ListBucket\"],\"Resource\":\"arn:aws:s3:::$BUCKET\"},
  {\"Effect\":\"Allow\",\"Action\":[\"s3:PutObject\",\"s3:GetObject\",\"s3:DeleteObject\"],\"Resource\":\"arn:aws:s3:::$BUCKET/*\"}]}"
if ! aws iam get-instance-profile --instance-profile-name "$ROLE" >/dev/null 2>&1; then
  aws iam create-instance-profile --instance-profile-name "$ROLE" >/dev/null
  aws iam add-role-to-instance-profile --instance-profile-name "$ROLE" --role-name "$ROLE"
  sleep 10   # IAM propagation
fi
ASSOC=$(aws ec2 describe-iam-instance-profile-associations --filters Name=instance-id,Values=$INSTANCE_ID Name=state,Values=associated --query 'IamInstanceProfileAssociations[0].AssociationId')
if [ -z "$ASSOC" ] || [ "$ASSOC" = "None" ]; then
  aws ec2 associate-iam-instance-profile --instance-id "$INSTANCE_ID" --iam-instance-profile Name="$ROLE" >/dev/null
  echo "attached $ROLE to $INSTANCE_ID"
fi
grep -q '^RICK_BACKUP_BUCKET=' .env && sed -i "s|^RICK_BACKUP_BUCKET=.*|RICK_BACKUP_BUCKET=$BUCKET|" .env || echo "RICK_BACKUP_BUCKET=$BUCKET" >> .env
echo "BUCKET=$BUCKET" >> .state
./push.sh
