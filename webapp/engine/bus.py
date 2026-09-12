"""Headless message bus.

The original desktop simulator pushed every scoreboard update straight into
Tkinter labels and every user notice into tkMessageBox pop-ups.  The web
version routes those same calls here instead.  ``board`` is the scoreboard
state, ``messages`` are the pop-ups raised since the last reset, ``results``
is the running play-by-play text.
"""

board = {}          # code -> latest value written by ScoreboardClass.ResultDisplay
messages = []       # (title, text) pairs from tkMessageBox.showinfo
results = []        # ordered play-result strings (codes 0,1,2,8-12)
ball = {"yardline": 25, "offense_flag": 0}


def reset_turn():
    """Clear per-action buffers.  Called by the game before each button press."""
    del messages[:]
    del results[:]


def reset_all():
    board.clear()
    reset_turn()
    ball.update({"yardline": 25, "offense_flag": 0})
