"""Back up the data directory to S3 as a single tar.gz; keep the newest N.

    python3 backup.py backup            # upload backups/<host>-<UTC stamp>.tgz
    python3 backup.py list
    python3 backup.py restore <key> [dir]   # download and unpack into dir (default: data dir)

Bucket comes from RICK_BACKUP_BUCKET; data dir from RICK_DATA_DIR.  Credentials
come from the instance role on EC2 or the normal AWS CLI chain locally.
"""
import io
import os
import socket
import sys
import tarfile
from datetime import datetime, timezone

DATA_DIR = os.path.abspath(os.environ.get("RICK_DATA_DIR", os.path.join(os.path.dirname(__file__), "data")))
BUCKET = os.environ.get("RICK_BACKUP_BUCKET", "")
PREFIX = "backups/"
KEEP = int(os.environ.get("RICK_BACKUP_KEEP", "30"))


def _s3():
    import boto3
    return boto3.client("s3")


def make_archive():
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for root, dirs, files in os.walk(DATA_DIR):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.startswith(".") or f.endswith(".tmp"):
                    continue
                full = os.path.join(root, f)
                tar.add(full, arcname=os.path.relpath(full, DATA_DIR))
    buf.seek(0)
    return buf


def backup():
    if not BUCKET:
        print("RICK_BACKUP_BUCKET not set; nothing to do")
        return None
    key = "%s%s-%s.tgz" % (PREFIX, socket.gethostname(), datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    s3 = _s3()
    s3.upload_fileobj(make_archive(), BUCKET, key)
    print("uploaded s3://%s/%s" % (BUCKET, key))
    prune(s3)
    return key


def _keys(s3):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        out.extend(page.get("Contents", []))
    return sorted(out, key=lambda o: o["Key"])


def prune(s3):
    keys = _keys(s3)
    for o in keys[:-KEEP] if len(keys) > KEEP else []:
        s3.delete_object(Bucket=BUCKET, Key=o["Key"])
        print("pruned", o["Key"])


def list_backups():
    for o in _keys(_s3()):
        print("%-60s %10d  %s" % (o["Key"], o["Size"], o["LastModified"].strftime("%Y-%m-%d %H:%M")))


def restore(key, dest=None):
    dest = os.path.abspath(dest or DATA_DIR)
    buf = io.BytesIO()
    _s3().download_fileobj(BUCKET, key, buf)
    buf.seek(0)
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=buf, mode="r:gz") as tar:
        for m in tar.getmembers():   # refuse paths that escape dest
            if m.name.startswith("/") or ".." in m.name.split("/"):
                raise SystemExit("unsafe member %s" % m.name)
        tar.extractall(dest)
    print("restored %s into %s" % (key, dest))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "backup"
    if cmd == "backup":
        backup()
    elif cmd == "list":
        list_backups()
    elif cmd == "restore":
        restore(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        raise SystemExit(__doc__)
