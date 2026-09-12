"""Headless full-game smoke test: python3 simulate.py <data_dir> [seed] [games]

Drives Game with a naive coach (punt/FG on 4th, kick XP after TDs) until the
engine reports the game over, then compiles stats.  Prints any engine
traceback.  Used to validate the Python 3 port; not part of the web UI.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def run_one(home, visitor, seed, verbose=False):
    import game
    random.seed(seed)
    g = game.Game(home, visitor, seed=seed)
    errors = []
    steps = 0
    while steps < 400 and not g.game_over():
        steps += 1
        act = g.auto_action()
        r = g.do(act, {})
        if verbose:
            s = g.state()
            print("%3d %-9s Q%s %s | %s&%s on %s | %s-%s | %s -> %s %s" % (
                steps, act, s["quarter"], s["clock"], s["down"], s["ytg"], s["ballon"],
                s["home_score"], s["visitor_score"], s["play_call"], r["results"], r["messages"]))
        if r["error"]:
            errors.append((steps, act, r["error"]))
            if verbose:
                print(r["error"])
            break
    q = g.quit()
    return g, steps, errors, q


if __name__ == "__main__":
    data = sys.argv[1]
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    verbose = "-v" in sys.argv
    os.chdir(data)
    import game
    teams = game.list_team_files(".")
    home, visitor = teams[0], teams[1]
    for seed in range(seed0, seed0 + n):
        g, steps, errors, q = run_one(home, visitor, seed, verbose)
        print("seed %d: %d steps, final %s, files %s, errors %d" % (seed, steps, q["final_score"], len(q["files"]), len(errors)))
        for e in errors:
            print("  step", e[0], e[1]); print(e[2])
        if q["error"]:
            print("  QUIT ERROR:"); print(q["error"])
