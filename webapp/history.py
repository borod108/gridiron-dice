"""Game history: SQLite index + one folder per game under <data>/games/<id>/.

The simulator names its output workbooks after the teams, so two games between
the same teams overwrite each other.  quit() therefore moves the six outputs
into games/<id>/ and records the game here.
"""
import json
import os
import shutil
import sqlite3
import time
from datetime import datetime

DB_NAME = "history.sqlite"
GAMES_DIR = "games"

SCHEMA = """
CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,
    started TEXT NOT NULL,
    ended TEXT,
    home TEXT NOT NULL,
    visitor TEXT NOT NULL,
    home_score INTEGER,
    visitor_score INTEGER,
    status TEXT NOT NULL,          -- in_progress | finished | abandoned
    plays INTEGER DEFAULT 0,
    log TEXT,                       -- JSON list of play-by-play lines
    files TEXT                      -- JSON list of output file names in games/<id>/
);
"""


def _db():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def new_id(home, visitor):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = "%s-%s-%s" % (stamp, home, visitor)
    gid, n = base, 1
    while os.path.exists(game_dir(gid)):
        n += 1
        gid = "%s-%d" % (base, n)
    return gid


def game_dir(gid):
    return os.path.join(GAMES_DIR, gid)


def start(gid, home, visitor):
    os.makedirs(game_dir(gid), exist_ok=True)
    with _db() as con:
        con.execute("INSERT OR IGNORE INTO games (id, started, home, visitor, status) VALUES (?,?,?,?,?)",
                    (gid, datetime.now().isoformat(timespec="seconds"), home, visitor, "in_progress"))


def finish(gid, home_score, visitor_score, log, output_files):
    """Move output workbooks into the game folder and mark the game finished."""
    d = game_dir(gid)
    os.makedirs(d, exist_ok=True)
    moved = []
    for f in output_files:
        if os.path.exists(f):
            shutil.move(f, os.path.join(d, os.path.basename(f)))
            moved.append(os.path.basename(f))
    with _db() as con:
        con.execute("UPDATE games SET ended=?, home_score=?, visitor_score=?, status='finished', plays=?, log=?, files=? WHERE id=?",
                    (datetime.now().isoformat(timespec="seconds"), home_score, visitor_score, len(log),
                     json.dumps(log), json.dumps(moved), gid))
    return moved


def abandon(gid, log=None):
    with _db() as con:
        con.execute("UPDATE games SET ended=?, status='abandoned', log=? WHERE id=? AND status='in_progress'",
                    (datetime.now().isoformat(timespec="seconds"), json.dumps(log or []), gid))


def list_games(limit=200):
    with _db() as con:
        rows = con.execute("SELECT id, started, ended, home, visitor, home_score, visitor_score, status, plays "
                           "FROM games ORDER BY started DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]


def get_game(gid):
    with _db() as con:
        r = con.execute("SELECT * FROM games WHERE id=?", (gid,)).fetchone()
    if r is None:
        return None
    g = dict(r)
    g["log"] = json.loads(g["log"] or "[]")
    g["files"] = json.loads(g["files"] or "[]")
    d = game_dir(gid)
    if os.path.isdir(d):   # trust the folder over the index
        g["files"] = sorted(f for f in os.listdir(d) if f.endswith(".xlsx"))   # hide journal.json
    return g


def delete_game(gid):
    with _db() as con:
        con.execute("DELETE FROM games WHERE id=?", (gid,))
    d = game_dir(gid)
    if os.path.isdir(d):
        shutil.rmtree(d)


def standings():
    """Win/loss/tie per team over finished games, plus points for/against."""
    table = {}
    for g in list_games(limit=100000):
        if g["status"] != "finished":
            continue
        hs, vs = g["home_score"] or 0, g["visitor_score"] or 0
        for team, pf, pa in ((g["home"], hs, vs), (g["visitor"], vs, hs)):
            t = table.setdefault(team, {"team": team, "w": 0, "l": 0, "t": 0, "pf": 0, "pa": 0, "games": 0})
            t["games"] += 1
            t["pf"] += pf
            t["pa"] += pa
            t["w" if pf > pa else "l" if pf < pa else "t"] += 1
    return sorted(table.values(), key=lambda t: (-t["w"], t["l"], -(t["pf"] - t["pa"])))
