# Rick's College Football Simulator — web version

Minimal Flask front end over the original simulator engine.

- How to use it: [MANUAL.md](MANUAL.md)
- Why it is built this way: [DECISIONS.md](DECISIONS.md)

## Run locally
    cd webapp
    pip install -r requirements.txt
    RICK_DATA_DIR=./data python3 app.py        # http://127.0.0.1:8000
Set RICK_PASSWORD to require a login (user: rick).

## Test the engine headlessly
    python3 make_sample_data.py data
    python3 simulate.py data 1 5 [-v]

## Deploy to EC2
    aws login                 # once per session
    deploy/provision.sh       # creates instance + Elastic IP, pushes app, prints URL
    deploy/push.sh            # redeploy after code changes
    deploy/teardown.sh        # destroy the instance (data on it is lost)
Login details are in deploy/.env. SSH: ssh -i ~/.ssh/rick-web-key.pem ubuntu@<IP>
