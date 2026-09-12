"""Minimal web front end for Rick's college football simulator.

Run:  RICK_DATA_DIR=/path/to/data RICK_PASSWORD=secret python3 app.py
or under gunicorn (see deploy/).  Single game at a time, single process.
"""
import os
import re
import secrets
import threading
from datetime import datetime
from functools import wraps

from flask import (Flask, Response, abort, flash, redirect, render_template,
                   request, send_from_directory, url_for)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.environ.get("RICK_DATA_DIR", os.path.join(HERE, "data")))
PASSWORD = os.environ.get("RICK_PASSWORD", "")
USERNAME = os.environ.get("RICK_USER", "rick")
os.makedirs(DATA_DIR, exist_ok=True)
os.chdir(DATA_DIR)   # the engine reads/writes workbooks relative to cwd

import game  # noqa: E402  (after chdir so nothing else depends on cwd)

app = Flask(__name__, template_folder=os.path.join(HERE, "templates"),
            static_folder=os.path.join(HERE, "static"))
app.secret_key = os.environ.get("RICK_SECRET", secrets.token_hex(16))
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

STATE = {"game": None}
LOCK = threading.Lock()
ALLOWED_EXT = (".xlsx", ".txt")
SAFE_NAME = re.compile(r"[^A-Za-z0-9 _.\-]")


# ------------------------------------------------------------------ auth
def _authorized():
    if not PASSWORD:
        return True
    a = request.authorization
    return a is not None and a.username == USERNAME and secrets.compare_digest(a.password or "", PASSWORD)


@app.before_request
def require_auth():
    if not _authorized():
        return Response("Login required", 401, {"WWW-Authenticate": 'Basic realm="rick"'})


# ------------------------------------------------------------------ helpers
def clean_name(name):
    name = os.path.basename(name or "").strip()
    name = SAFE_NAME.sub("_", name)
    if not name or name.startswith(".") or not name.lower().endswith(ALLOWED_EXT):
        return None
    return name


def list_files():
    out = []
    for f in sorted(os.listdir(DATA_DIR), key=str.lower):
        p = os.path.join(DATA_DIR, f)
        if not os.path.isfile(p) or f.startswith("."):
            continue
        st = os.stat(p)
        kind = "team"
        if f.endswith(game.OUTPUT_SUFFIXES):
            kind = "output"
        elif not f.lower().endswith(".xlsx"):
            kind = "other"
        out.append({"name": f, "size": st.st_size, "kind": kind,
                    "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")})
    return out


def current_game():
    return STATE["game"]


# ------------------------------------------------------------------ routes: files
@app.route("/")
def index():
    g = current_game()
    return render_template("index.html", files=list_files(), teams=game.list_team_files(DATA_DIR),
                           game=g, state=g.state() if g else None)


@app.route("/upload", methods=["POST"])
def upload():
    n = 0
    for f in request.files.getlist("files"):
        name = clean_name(f.filename)
        if not name:
            flash("Skipped %s (only .xlsx and .txt files are accepted)" % (f.filename or "unnamed"))
            continue
        f.save(os.path.join(DATA_DIR, name))
        n += 1
    if n:
        flash("Uploaded %d file(s)" % n)
    return redirect(url_for("index"))


@app.route("/files/<path:name>")
def download(name):
    name = clean_name(name)
    if not name or not os.path.isfile(os.path.join(DATA_DIR, name)):
        abort(404)
    return send_from_directory(DATA_DIR, name, as_attachment=True)


@app.route("/delete/<path:name>", methods=["POST"])
def delete(name):
    name = clean_name(name)
    if not name:
        abort(404)
    g = current_game()
    if g and not g.finished and name[:-5] in (g.homeTeamName, g.visitingTeamName):
        flash("%s is in use by the game in progress" % name)
        return redirect(url_for("index"))
    p = os.path.join(DATA_DIR, name)
    if os.path.isfile(p):
        os.remove(p)
        flash("Deleted %s" % name)
    return redirect(url_for("index"))


@app.route("/delete-outputs", methods=["POST"])
def delete_outputs():
    n = 0
    for f in list_files():
        if f["kind"] == "output":
            os.remove(os.path.join(DATA_DIR, f["name"]))
            n += 1
    flash("Deleted %d output file(s)" % n)
    return redirect(url_for("index"))


# ------------------------------------------------------------------ routes: game
@app.route("/start", methods=["POST"])
def start():
    home, visitor = request.form.get("home", ""), request.form.get("visitor", "")
    with LOCK:
        g = current_game()
        if g and not g.finished:
            flash("A game is already in progress. End or abandon it first.")
            return redirect(url_for("game_page"))
        try:
            STATE["game"] = game.Game(home, visitor)
        except game.GameError as e:
            flash(str(e))
            return redirect(url_for("index"))
        except Exception as e:  # bad workbook layout etc.
            flash("Could not start the game: %s: %s" % (type(e).__name__, e))
            return redirect(url_for("index"))
    return redirect(url_for("game_page"))


@app.route("/game")
def game_page():
    g = current_game()
    if g is None:
        return redirect(url_for("index"))
    if g.finished:
        return render_template("done.html", state=g.state(), result=g.last_quit)
    return render_template("game.html", state=g.state(), boxes=game.CHECKBOXES, last=g.last_turn)


@app.route("/game/action", methods=["POST"])
def game_action():
    action = request.form.get("action", "")
    boxes = {k: 1 for k in request.form.getlist("box")}
    with LOCK:
        g = current_game()
        if g is None or g.finished:
            return redirect(url_for("index"))
        try:
            g.last_turn = g.do(action, boxes)
        except game.GameError as e:
            flash(str(e))
    return redirect(url_for("game_page"))


@app.route("/game/end", methods=["POST"])
def game_end():
    with LOCK:
        g = current_game()
        if g is None:
            return redirect(url_for("index"))
        if not g.finished:
            g.last_quit = g.quit()
    return redirect(url_for("game_page"))


@app.route("/game/abandon", methods=["POST"])
def game_abandon():
    with LOCK:
        STATE["game"] = None
    flash("Game discarded")
    return redirect(url_for("index"))


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host=os.environ.get("RICK_HOST", "127.0.0.1"), port=int(os.environ.get("RICK_PORT", "8000")), debug=False)
