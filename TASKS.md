# TASKS.md — ordered backlog for autonomous work

Work top to bottom, one item at a time. After finishing an item: tick its box, commit, move on.
Read `CLAUDE.md` first. COS (Lectures 6 and 10) comes first because the professor invented it.

For each LECTURE task, produce:
- A complete LaTeX study note (~10 pages from ~50 slides) with full derivations worked out (not bullet points), clear structure, key concepts and pitfalls. Compile to PDF in `notes/` as `Lecture<NN>-notes.pdf` (keep the `.tex` too).
- A matching set of exam-style questions in `question-bank/` (append to `theory-questions.md`, and to `cos-deep-dive.md` for COS).

For each ASSIGNMENT task, produce:
- A filled defense sheet in `defense-sheets/<set>.md` drafted from my ACTUAL code and report (task, approach, key code sections by file+line, results, hardest likely question). Leave a clearly marked TODO wherever the *reason* for a design choice needs my input — you can describe what the code does, but not why I chose it.
- Code-level "open your file and explain line X" questions in `question-bank/assignment-defense-questions.md`.

## Priority — COS
- [x] Lecture 06 — Fourier family, COS for density recovery, COS for option pricing
- [ ] Lecture 10 — pricing problem, analytical under GBM, PDE + COS for Barrier options

## Lectures (numeric order)
- [ ] Lecture 01
- [ ] Lecture 02
- [ ] Lecture 03
- [ ] Lecture 04 — Monte Carlo integration, MC for SDEs, variance reduction
- [ ] Lecture 05 — Binomial, finite differences, BS PDE, binomial-as-FD
- [ ] Lecture 07 — Heston, CIR variance, affine structure & characteristic function, MC under Heston
- [ ] Lecture 08 — Poisson, jump diffusion, affine jump diffusion
- [ ] Lecture 09 — American options (call/put, Euro/Am equivalence, FD/MC/COS/binomial-tree)
- [ ] Lecture 11 — exotics overview (barrier/Asian/digital/basket/cliquet)

## Assignments (defense sheets)
- [ ] exercise-set-1
- [ ] assignment-set-1
- [ ] exercise-set-2
- [ ] assignment-set-2

## Rules
- Commit after each item with a clear message.
- Stop and ask me only if a slide PDF is unreadable or a file is missing.
- Do not invent the reasoning behind my code choices — mark those as TODO for me.
