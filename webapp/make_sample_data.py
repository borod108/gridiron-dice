"""Generate synthetic team stat workbooks in the exact layout the simulator reads.

Usage:  python3 make_sample_data.py [output_dir] [TeamName ...]

With no team names it writes SampleHome.xlsx and SampleAway.xlsx.  Each team's
numbers come from a seed derived from its name, so reruns are identical.

Builds the sheet skeleton with the original StatsWorksheet class (so section
labels land where PickAPlayer.FindStats expects them) and then fills the rows
the simulator actually consumes.  Numbers are plausible, not real.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "engine"))

from openpyxl import load_workbook          # noqa: E402
import PickAPlayer                          # noqa: E402
import StatsWorksheet                       # noqa: E402

FIRST = ["Marcus", "Jalen", "Tyler", "Devin", "Caleb", "Jordan", "Malik", "Trey",
         "Kyle", "Andre", "Brandon", "Isaiah", "Noah", "Elijah", "Cameron",
         "Darius", "Xavier", "Logan", "Chase", "Mason", "Ethan", "Owen", "Levi"]
LAST = ["Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore",
        "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
        "Thompson", "Garcia", "Robinson", "Clark", "Lewis", "Walker", "Hall",
        "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams"]


def names(n, rng):
    out = set()
    while len(out) < n:
        out.add("%s %s" % (rng.choice(FIRST), rng.choice(LAST)))
    return sorted(out)


def cum_ranges(weights):
    """Return list of (cp1, cp2) integer percentage bands, last band ends at 100."""
    total = float(sum(weights))
    bands, lo = [], 0
    for i, w in enumerate(weights):
        hi = 100 if i == len(weights) - 1 else lo + int(round(100 * w / total))
        bands.append((lo, hi))
        lo = hi
    return bands


def build_team(team, out_dir, seed):
    rng = random.Random(seed)
    cwd = os.getcwd()
    os.chdir(out_dir)
    try:
        n_rb, n_rec, n_def = 5, 8, 14
        sw = StatsWorksheet.StatsWorksheet(team, {
            "Rushing_Stats": n_rb, "Passing_Stats": 2,
            "Receiving_Stats": n_rec, "Defensive_Stats": n_def}, {})
        sw.CreateWorksheetStructure()
        wb = load_workbook(team + ".xlsx")
        ws = wb.active
        pos = PickAPlayer.PickAPlayer(ws, 0, 0, 0, 0, 0)
        pos.FindStats()
        c = ws.cell

        # ---- Runners: B name C carries D YPC E avail F adj G CP1 H CP2 I type J BCP1 K BCP2 L backup
        rb_names = names(n_rb, rng)
        carries = [180, 110, 60, 45, 20]
        types = ["RB", "RB", "QB", "RB", "WR"]
        for i, (lo, hi) in enumerate(cum_ranges(carries)):
            r = pos.RunnersPosition + 1 + i
            c(row=r, column=2).value = rb_names[i]
            c(row=r, column=3).value = carries[i]
            c(row=r, column=4).value = round(rng.uniform(3.8, 6.4), 1)
            c(row=r, column=5).value = 1
            c(row=r, column=6).value = carries[i]
            c(row=r, column=7).value = lo
            c(row=r, column=8).value = hi
            c(row=r, column=9).value = types[i]
            c(row=r, column=10).value = lo
            c(row=r, column=11).value = hi
            c(row=r, column=12).value = 0 if i < 2 else 1

        # ---- QBs: B name C comp% D int% E avail F sack% J PassOriented L RunOriented
        qb_names = names(2, rng)
        pass_oriented = rng.choice([0, 1])
        for i in range(2):
            r = pos.QBsPosition + 1 + i
            c(row=r, column=2).value = qb_names[i]
            c(row=r, column=3).value = round(rng.uniform(58, 68), 1)
            c(row=r, column=4).value = round(rng.uniform(1.5, 3.5), 2)
            c(row=r, column=5).value = 1
            c(row=r, column=6).value = round(rng.uniform(4, 8), 1)
            c(row=r, column=10).value = pass_oriented
            c(row=r, column=12).value = 0 if pass_oriented else rng.choice([0, 1])

        # ---- Receivers: B name C YPC D receptions E avail F adj G CP1 H CP2 I type J BCP1 K BCP2
        rec_names = names(n_rec, rng)
        recs = [70, 55, 40, 30, 25, 18, 12, 8]
        rtypes = ["Receiver", "Receiver", "Receiver", "Receiver", "RB", "Receiver", "Receiver", "RB"]
        for i, (lo, hi) in enumerate(cum_ranges(recs)):
            r = pos.ReceiversPosition + 1 + i
            c(row=r, column=2).value = rec_names[i]
            c(row=r, column=3).value = round(rng.uniform(8.5, 16.5), 1)
            c(row=r, column=4).value = recs[i]
            c(row=r, column=5).value = 1
            c(row=r, column=6).value = recs[i]
            c(row=r, column=7).value = lo
            c(row=r, column=8).value = hi
            c(row=r, column=9).value = rtypes[i]
            c(row=r, column=10).value = lo
            c(row=r, column=11).value = hi
            c(row=r, column=12).value = 0 if i < 4 else 1

        # ---- Kicker row: B name C #KO D KO ave E TB F OB G PAT% H-L FG% by range
        kr = pos.KickersPosition + 1
        kick_name, punt_name = names(2, rng)
        c(row=kr, column=2).value = kick_name
        c(row=kr, column=3).value = 60
        c(row=kr, column=4).value = 62.5
        c(row=kr, column=5).value = 30
        c(row=kr, column=6).value = 1
        c(row=kr, column=7).value = 97
        for col, pct in zip(range(8, 13), [99, 92, 82, 65, 40]):
            c(row=kr, column=col).value = pct
        # ---- Punter row (Kickers + 2): B name D ave E long F FC%
        pr = pos.KickersPosition + pos.Offset + pos.PuntersOffset
        c(row=pr, column=2).value = punt_name
        c(row=pr, column=4).value = round(rng.uniform(40, 45), 1)
        c(row=pr, column=5).value = 62
        c(row=pr, column=6).value = 25

        # ---- Defensive Team Stats (3 data rows under the label)
        d = pos.DStatsPosition
        c(row=d + 1, column=3).value = round(rng.uniform(3.6, 5.2), 2)   # rush yds/att allowed
        c(row=d + 1, column=6).value = 1                                # kick block %
        c(row=d + 1, column=8).value = 1                                # punt block %
        c(row=d + 1, column=10).value = round(rng.uniform(2.0, 3.5), 2) # INT %
        c(row=d + 2, column=3).value = round(rng.uniform(55, 64), 1)    # completion % allowed
        c(row=d + 2, column=6).value = round(rng.uniform(5, 8), 1)      # sack %
        c(row=d + 2, column=10).value = rng.randint(80, 140)            # fumble rec per 10000
        c(row=d + 3, column=3).value = round(rng.uniform(11, 14), 1)    # yds/catch allowed

        # ---- Kick returner (KRs + 1) and punt returner (KRs + 4)
        kr_name, pr_name = names(2, rng)
        k = pos.KRsPosition + 1
        c(row=k, column=2).value = kr_name
        c(row=k, column=3).value = 25
        c(row=k, column=4).value = round(rng.uniform(20, 26), 1)
        c(row=k, column=5).value = 58
        p = pos.KRsPosition + pos.PROffset
        c(row=p, column=2).value = pr_name
        c(row=p, column=4).value = round(rng.uniform(7, 12), 1)
        c(row=p, column=5).value = 41

        # ---- INTs: B name C # D PMin E PMax F ave return
        def_names = names(n_def, rng)
        ints = [4, 3, 2, 2, 1, 1]
        for i, (lo, hi) in enumerate(cum_ranges(ints)):
            r = pos.INTsPosition + 1 + i
            c(row=r, column=2).value = def_names[i]
            c(row=r, column=3).value = ints[i]
            c(row=r, column=4).value = lo
            c(row=r, column=5).value = hi
            c(row=r, column=6).value = round(rng.uniform(5, 20), 1)

        # ---- Fumbles lost (value sits on the label row, column B)
        c(row=pos.OFumblesLostPosition, column=2).value = rng.randint(70, 130)

        # ---- Fumble recoveries: 18 names
        for i in range(18):
            c(row=pos.FumbleRecoveriesPosition + 1 + i, column=2).value = def_names[i % n_def]

        # ---- Team stats: B penalties/game C conference factor
        c(row=pos.TeamStatsPosition + 1, column=2).value = round(rng.uniform(5, 8), 1)
        c(row=pos.TeamStatsPosition + 1, column=3).value = 5.0

        # ---- Tackles (B name C # D CPmin E CPmax) and Sacks (H name I # J CPmin K CPmax)
        tackles = [rng.randint(20, 90) for _ in range(n_def)]
        for i, (lo, hi) in enumerate(cum_ranges(tackles)):
            r = pos.TacklesPosition + 1 + i
            c(row=r, column=2).value = def_names[i]
            c(row=r, column=3).value = tackles[i]
            c(row=r, column=4).value = lo
            c(row=r, column=5).value = hi
        sacks = [6, 5, 4, 3, 2, 1]
        for i, (lo, hi) in enumerate(cum_ranges(sacks)):
            r = pos.TacklesPosition + 1 + i
            c(row=r, column=8).value = def_names[i]
            c(row=r, column=9).value = sacks[i]
            c(row=r, column=10).value = lo
            c(row=r, column=11).value = hi

        # ---- Injury impacts: OL, DL, LB, DB counts in column C
        for i in range(4):
            c(row=pos.InjuryImpactsPosition + 1 + i, column=3).value = 0

        wb.save(team + ".xlsx")
        return os.path.join(out_dir, team + ".xlsx")
    finally:
        os.chdir(cwd)


def seed_for(name):
    """Stable per-name seed (hash() is randomised per process in Python 3)."""
    return sum((i + 1) * ord(ch) for i, ch in enumerate(name))


if __name__ == "__main__":
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data"))
    os.makedirs(out, exist_ok=True)
    team_names = sys.argv[2:]
    pairs = [(n, seed_for(n)) for n in team_names] if team_names else [("SampleHome", 1), ("SampleAway", 2)]
    for team, seed in pairs:
        print("wrote", build_team(team, out, seed))
