# Computational Finance — oral exam prep

Working repo for a 25–30 min oral exam with Prof. Fang Fang (TU Delft). See `CLAUDE.md` for the full context that Claude Code reads automatically.

## Folder map

```
compfin-oral-prep/
├── CLAUDE.md              # context Claude Code reads every session (the important file)
├── README.md             # this file
├── .gitignore
├── slides/               # drop Lecture01.pdf … Lecture11.pdf here
├── assignments/
│   ├── exercise-set-1/    # PDF + my code + my LaTeX, per graded item
│   ├── assignment-set-1/
│   ├── exercise-set-2/
│   └── assignment-set-2/
├── notes/                # distilled per-cluster notes (generated on request)
├── defense-sheets/       # one per assignment — fill these and rehearse them
├── question-bank/        # self-test questions; cos-deep-dive.md is priority
└── mock-orals/           # simulated oral logs + gaps-log.md
```

## What goes where

1. Put each lecture's slide PDF in `slides/`, named `Lecture01.pdf` … `Lecture11.pdf`.
2. For each graded item, put into its `assignments/<set>/` folder: the assignment PDF, every `.py` file you wrote, and your LaTeX report (`.tex` and the compiled `.pdf`).
3. Everything else (`notes/`, `defense-sheets/`, `question-bank/`, `mock-orals/`) starts as templates and gets filled in as you work with Claude Code.

## How the pieces relate (this trips people up)

- **Claude Code reads your LOCAL folder**, not GitHub. GitHub is only backup/sync. You do not need GitHub for Claude Code to work — you could skip it entirely. It is useful if you want a safety net or to work from two machines.
- The repo itself is your memory across sessions. Anything important must end up written into a file here, or it's gone when the session ends.

## Git + GitHub setup (one time)

Open a terminal in this folder. **Keep the repo private** — it has graded coursework and course slides.

If you have the GitHub CLI (`gh`) installed, this is the whole thing:

```bash
git init
git add .
git commit -m "Initial scaffold"
gh repo create compfin-oral-prep --private --source=. --remote=origin --push
```

If you don't have `gh`: create an empty **private** repo on github.com named `compfin-oral-prep` (do NOT let it add a README), then:

```bash
git init
git add .
git commit -m "Initial scaffold"
git branch -M main
git remote add origin https://github.com/<your-username>/compfin-oral-prep.git
git push -u origin main
```

After that, to save progress any time:

```bash
git add .
git commit -m "what I did this session"
git push
```

## Daily workflow

1. `cd` into this folder and start Claude Code. It reads `CLAUDE.md` automatically.
2. Tell it what to work on, e.g. "Quiz me on the COS cluster" or "Open my Assignment 2 Heston code and grill me on it."
3. When you miss something, it logs to `mock-orals/gaps-log.md`.
4. End of session: commit and push.

## The plan in one screen

- **Days 1–2** — setup, generate cluster notes, write a defense sheet per assignment, re-read your own code until you can narrate every non-trivial line.
- **Days 3–5** — content mastery cluster by cluster (active recall, closed-book). Spend a full block on COS.
- **Days 6–7** — timed mock orals out loud, COS-heavy plus assignment defense. Drill the gaps log.
