# gridiron-dice

A stat-driven college football simulator. Every play is three dice rolled into
lookup tables weighted by real team statistics kept in Excel workbooks.

- Root directory: the original Python 2 / Tkinter desktop application and the
  stats extractor (see `CODEBASE_REFERENCE.md`).
- `webapp/`: Python 3 web version (Flask) that reuses the engine unchanged and
  deploys to a single EC2 instance. See `webapp/README.md` and
  `webapp/DECISIONS.md`.

User manual for the web version: [webapp/MANUAL.md](webapp/MANUAL.md).
