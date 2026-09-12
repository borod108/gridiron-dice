# gridiron-dice user manual

gridiron-dice is a college football simulator that runs in your browser. You
upload each team's statistics as an Excel workbook, pick two teams, and play
the game one button at a time. Dice rolls weighted by the teams' real numbers
decide every play.

The pages are titled *Rick's College Football Simulator*. The top of every
page has three links: **Data & teams**, **Game** and **History**.

---

## 1. Sign in

Open the server address in a browser. The browser asks for a user name and
password; use the ones you were given. It remembers them until you close the
browser.

## 2. Add team data

Each team is one Excel workbook named after the team, for example
`Eagles.xlsx`. The part before `.xlsx` is the name you will see in the team
lists. Workbooks must use the simulator's stat-sheet layout. The original
stats extractor produces it, and `webapp/sample_data/` has two examples.

### Upload

On **Data & teams**, under **Upload data**:

1. Choose what to send:
   - **Files or a .zip**: pick one or more workbooks, or one zip file.
   - **…or a whole folder**: pick a folder. Sub-folders are included.
2. Click **Upload**.

A yellow note says how many files were added and names anything skipped. Only
`.xlsx` and `.txt` files are kept. A file with the same name as an existing
one replaces it.

### See, download and delete files

The **Files** table lists every file with its type:

- **team**: a workbook you can pick for a game.
- **output**: a working file the simulator writes during a game.
- **other**: anything else, such as `General Info.txt`.

Click a name to download that file. Click **Delete** next to a file and
confirm to remove it. A team playing in the current game cannot be deleted.
**Download everything (zip)** saves all files, including finished games.

## 3. Play a game

### Start

Under **Start a game**, choose **Home** and **Visitor**, then click
**Start game**. The game page shows the scoreboard, a green strip with the
ball's position, the buttons, and the result of the coin toss.

The scoreboard's **Ball on** reads from the offense's point of view: "own 30"
is the offense's own 30-yard line, "opp 30" is the opponent's.

### How a game goes

1. Press **Kickoff**.
2. Press **Call Play** for each down. The simulator chooses run or pass and who
   gets the ball. The result appears in the white box and in the play log.
3. On 4th down, press **Punt**, **FG**, or **Call Play** to go for it.
4. After a touchdown, press **XPt** or **Go For 2**, then **Kickoff**.
5. After a field goal or a safety, press **Kickoff**. After a safety it is
   taken as a free kick automatically.
6. At the start of the third quarter, press **Kickoff** again.

The clock and quarters run on their own. If a button does not fit the
situation, a blue notice names the right one and the game is unchanged.
Such presses are not recorded, so **Undo last action** skips them.

### Buttons

| Button | What it does |
|---|---|
| Kickoff | Kicks off. Needed at the start of each half and after every score. |
| Call Play | Runs one play. |
| Punt | Punts. 4th down only. |
| FG | Tries a field goal. The ball must be on "opp 38" or closer. |
| XPt | Kicks the extra point after a touchdown. |
| Go For 2 | Tries a two-point conversion after a touchdown. Works about 4 times in 10. |
| HTO / VTO | Home or visitor timeout. Gives back half the time the last play used. Three per half. |
| OT | Starts the next overtime possession. See section 4. |

### Options

Tick a box before pressing a button.

- **Run-Oriented** / **Pass-Oriented**: call more runs or more passes. Ticking
  both cancels both.
- **Hurry-Up**: pass more and use less clock.
- **Spike the Ball**: throw the ball into the ground to stop the clock.
- **Hail Mary Pass**: throw deep.
- **Take a Knee**: the quarterback kneels to run the clock.
- **Squib Kick**, **Onside Kick**: the kind of kickoff. Tick one. Onside kicks
  are recovered about 1 time in 5.
- **Free Kick**: kick from your own 20. Set for you after a safety.
- **Placement Punt**: a punt aimed at the corner to pin the other team deep.
- **HT Blowout** / **VT Blowout**: that team plays its backups on offense.
- **Force (debug)**: for testing only. Leave it unticked.

Kick and play-calling boxes clear themselves after a kickoff, a punt or a
change of possession. **Take a Knee** and the **Blowout** boxes stay ticked
until you untick them.

### Notices you may see

- **Penalty. Do you wish to accept?**: information only. The web version
  always accepts the penalty.
- **Fumble Debug Message**, **Int Debug Message**: leftovers from the original
  program. Ignore them.
- **Button Press Infraction**: tells you which button to press instead.
- A red **Engine error** box: something failed inside the simulator. Press
  **Undo last action**.

### Undo, auto-play and finishing

- **Undo last action** takes back the last button press. Press it again to go
  further back.
- **Auto-play to the end** plays the rest of the game with a simple coach. You
  can still undo afterwards.
- When the game ends, the scoreboard shows **FINAL** and a yellow banner
  appears. Press **Quit / compile stats** and confirm. The next page shows
  the final score and download links for each team's stats, defensive stats
  and play log. Press **Back to start** when done.
- **Abandon game** discards the game without stats. History lists it as
  abandoned.

Only one game can be in progress at a time. If the server restarts, the game
comes back exactly where it was.

## 4. Overtime

If the fourth quarter ends tied, a notice says overtime has started and which
team has the ball. In each overtime series both teams get one possession,
starting at the opponent's 25.

1. Press **Call Play**, and **FG** if you want, until the possession ends: a
   touchdown and its conversion, a field goal try, or a turnover.
2. Press **OT**. The other team gets the ball.
3. After both teams have had the ball, **OT** checks the score. If one team
   leads, the game is over. If not, the next series starts.

From the third series, teams must go for 2 after a touchdown. There are no
kickoffs or punts in overtime.

## 5. History

**History** has two tables.

- **Standings**: wins, losses and ties per team, games played, and points for
  (PF) and against (PA). Only finished games count.
- **Games**: every game with its start time, teams, score and status
  (finished, abandoned or in progress). Click a start time to see the play
  log and download the workbooks.
  **Delete** removes a game and its files.

## 6. Good to know

- Your data is backed up automatically after every finished game and once a
  day.
- Undo and restart recovery replay the game from its recorded button presses,
  so they can take a moment late in a game.
