# Rick's College Football Simulator — Codebase Reference

> Generated 2026-06-29. All 32 files studied.

---

## What This Is

Two standalone desktop Python 2.x applications sharing some modules.

**App 1: Game Simulator** — entry point `ControlPanel.py` (Rev 4.0). Stat-driven probabilistic NCAA football play-by-play engine.

**App 2: Stats Extractor** — entry point `Executive.py`. Scrapes ESPN/NCAA HTML tables via pandas/BeautifulSoup and writes formatted Excel stat files for the simulator.

**Not part of either app:** `RecipePlanner.py` (personal recipe chooser app).

---

## Python Version Warning

This codebase is **Python 2.x only** and will not run on Python 3 without changes:
- `from Tkinter import *` → `from tkinter import *`
- `import tkMessageBox` → `from tkinter import messagebox`
- `print x` (no parens) in CalculateResult.py, CalculateYardage.py
- `from __future__ import division` in FormatStats.py

---

## Dependencies

```
openpyxl        — Excel I/O (all files)
pandas          — HTML scraping (Executive.py pipeline)
requests        — HTTP requests
beautifulsoup4  — HTML parsing
tkinter         — GUI
turtle          — Field visualization (built-in)
```

---

## Architecture

```
ControlPanel.py  (GUI + game loop)
    │
    ├── Play.py              (central Play class, instantiated each button press)
    │     ├── GameManager.py       (play selection: run/pass, player selection)
    │     ├── ResultofthePlay.py   (outcome: yards, complete/inc/sack/int/fumble)
    │     │     ├── Die.py         (dice roller)
    │     │     └── YardageTable.py (lookup tables)
    │     ├── Penalty.py           (penalty system)
    │     ├── PickAPlayer.py       (worksheet navigator / player finder)
    │     └── ScoreboardClass.py   (Tkinter scoreboard display)
    │
    ├── LogPlays.py          (per-play log write/read; also CompileStats)
    ├── TestTurtleGraphics.py (DrawField, PlaceBall)
    ├── GeneralInfoFile.py   (read/write General Info.txt)
    └── GameMaintenance.py   (UpdateYTG)

Executive.py  (Stats Extractor GUI)
    ├── TableExtraction.py   (web scraping via pandas.read_html)
    ├── StatsWorksheet.py    (creates empty team Excel file with section headers)
    ├── FormatStats.py       (fills stat worksheet with scraped data + CPs)
    └── ReWriteStats.py      (recomputes cumulative probabilities in existing file)
```

---

## Core Simulation Mechanic

All play outcomes are decided by **3-die rolls** indexing into lookup tables:
1. Roll d3 + 2d6 → `(columnIndex, rowIndex)` in an 11×3 table
2. Look up result in `YardageTable.py`
3. Result may be a number (yards) or a code (`"SG"`, `"MG"`, `"LG"`) requiring a second roll
4. Adjust yards by rush adjuster or pass yardage multiplier (based on actual team stats + conference factor)

Ball carrier / receiver selection also uses dice rolling against cumulative probability columns in the team's Excel worksheet.

---

## File Status

| File | Purpose | Status |
|------|---------|--------|
| `ControlPanel.py` | Game simulator entry point | **Active** |
| `Play.py` | Central Play class | **Active** |
| `GameManager.py` | Play selection | **Active** |
| `ResultofthePlay.py` | Outcome resolution | **Active** |
| `YardageTable.py` | Dice lookup tables | **Active** |
| `Die.py` | Dice roller class | **Active** |
| `Penalty.py` | Penalty system | **Active** |
| `PickAPlayer.py` | Worksheet navigator | **Active** |
| `ScoreboardClass.py` | Scoreboard display | **Active** |
| `LogPlays.py` | Play logging + stat compilation | **Active** |
| `TestTurtleGraphics.py` | Field visualization | **Active** |
| `GeneralInfoFile.py` | Last-game team names persistence | **Active** |
| `GameMaintenance.py` | UpdateYTG helper | **Active** |
| `Executive.py` | Stats extractor entry point | **Active** |
| `TableExtraction.py` | Web scraping class | **Active** |
| `StatsWorksheet.py` | Creates team Excel structure | **Active** |
| `FormatStats.py` | Fills team Excel with stats | **Active** |
| `ReWriteStats.py` | Recomputes cumulative probs | **Active** |
| `STP.py` | Team selection panel (newer) | **Active** |
| `SelectTeamsPanel.py` | Team selection panel (older) | Legacy |
| `LBwithWait_Window.py` | Listbox helper | Legacy |
| `Control Panel.py` | Old game simulator (with space) | Legacy |
| `ID_Team.py` | Early team loader | Dead code |
| `LoadTeam.py` | USC.xlsx prototype | Dead code |
| `LoadTeamClass.py` | USC.xlsx prototype | Dead code |
| `LoadTeamMethod.py` | USC.xlsx prototype | Dead code |
| `MDArray.py` | Commented-out class stub | Dead code |
| `GameManagement.py` | Empty class stub | Dead code |
| `CalculateResult.py` | Early yardage prototype script | Dead code |
| `CalculateYardage.py` | Early yardage prototype fn | Dead code |
| `TableExtractionClass.py` | Empty file | Dead code |
| `RecipePlanner.py` | Recipe chooser app (unrelated) | Unrelated |

---

## Key Data Structures

### Team Excel Worksheet Sections (column A = section header)
```
Runners          — RB/QB/WR stats + cumulative probability columns
QBs              — QB pass/sack stats + run/pass orientation flags
Receivers        — WR/TE/RB-as-receiver stats + CPs
Kickers          — Kickoff stats, FG% by range (0-19, 20-29, 30-39, 40-49, 50-55), PAT%
(Punter row)     — Punt ave, long, fair catch %
KRs              — Kick returner name, # returns, ave, long
PRs              — Punt returner stats
INTs             — Defensive players with INT stats + CPs
Fumble Lost      — Offensive fumble probability (per 10,000 plays)
Fumble Recoveries — 18 defensive players who can recover fumbles
Teams Stats      — Penalties/game, Conference Factor
Tackles          — Defensive player tackle counts + CPs; also sack CPs in same section
Injury Impacts   — # of starters injured at OL, DL, LBs, DBs
Defensive Team Stats — DRushYds/att, DPassComp%, DYardsPerCatch, DSack%, DPuntBlock%, DKickBlock%, DINT%, DFumRecovery%
End              — marks end of worksheet
```

### VDstats / HDstats (6-element defensive stats list)
```python
[rushAvgAllowed, passCompPercAllowed, yardsPerCatchAllowed, sackPerc, intPerc, fumbleRecoveryPer10000]
```

### GM dict (game state)
Down, YTG, YardLine, Quarter, HomeScore, VisitorScore, TeamWiththeBallFlag, HomeTimeouts, VisitorTimeouts, TimeLeftinQuarter, UntimedDownFlag, OTFlag

### GameOptions dict
RunCentric, PassCentric, Hup (hurry-up), SpiketheBall, HailMary, Blowout, ForcePenalty, QBTakesaKnee, ForcePlay

### Kicking dict
KickFlag, KickoffFlag, FGFlag, PuntFlag, XPtFlag, SquibKick, OnsideKick, FreeKick, PlacementPunt, TwoPointConvFlag, StartoftheGame, Startofthe3rdQuarter

---

## Conference Factor

Quality weight (4.2–5.0) per conference, stored in team worksheet `Teams Stats` row column C:
- 5.0: SEC, Big-10, PAC-12, ACC, Big-12
- 4.9: American; 4.7: Mountain West; 4.6: MAC; 4.5: C-USA; 4.4: Sun Belt; 4.2: FCS

Used in `ResultofthePlay.py` as both an additive rush adjuster and multiplicative pass adjuster to account for cross-conference stat quality differences.

---

## Modernization Notes

### To run on Python 3
1. Replace `Tkinter` → `tkinter` imports everywhere
2. Fix bare `print` statements in CalculateResult.py, CalculateYardage.py
3. Remove `from __future__ import division`

### To create sample data
Use `Executive.py` with a team's ESPN/NCAA stat URL (if URLs still work), or manually build a `.xlsx` file following the section structure above. Minimum viable team file needs: Runners, QBs, Receivers, Kickers, Punter rows, KRs, PRs, INTs, Fumble Lost, Fumble Recoveries, Teams Stats, Tackles, Injury Impacts, Defensive Team Stats, End.

### For online migration
- Keep the simulation algorithms (GameManager, ResultofthePlay, YardageTable, Die, Penalty) — they are the intellectual core
- Replace Tkinter → web UI (React, Streamlit, etc.)
- Replace openpyxl Excel files → database (SQLite/PostgreSQL)
- Replace global variables → a proper GameState class
- The cumulative probability mechanism (CP1/CP2 columns driving player selection) is the key design pattern to preserve
