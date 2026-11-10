# Plot Twist — notes for the coding agent

Team project (4 people) for Introduction to Programming, Nova SBE 2026/27. The team members are **beginners** and every one of them must be able to explain any part of this code in the walkthrough, including code they did not write. Teach, don't just do.

## Running things

- Install / update libraries: `uv sync`.
- Run the app: `uv run streamlit run app.py` (opens http://localhost:8501, stop with Ctrl+C).
- Tests: `uv run pytest`.
- Never use `pip` or `python -m venv` — uv handles Python and libraries.

## Structure

- `app.py` — the screens (Streamlit). Reads input, calls `logic.py`, shows results.
- `logic.py` — the rules (moving between scenes, items, conditions, endings). No Streamlit and no database code here.
- `db.py` — saving and loading the game in SQLite (`data/*.db`, not committed to git).
- `tests/` — pytest tests. They are the acceptance checks.
- `specs/` — one spec per feature, written before the code.
- `docs/plot-twist-brd.md` — the product brief from the course.
- `docs/plano-do-projeto.md` — the team plan (in Portuguese): course requirements, decisions, phases, current status and feature ideas. Read it first and keep its status table up to date.

The team speaks Portuguese (PT-PT): explain in Portuguese, keep code and specs in English.

## Rules

- `main` is the version everyone trusts. Nobody pushes to `main` directly.
- Every feature: its own branch → pull request → reviewed by another team member → merge.
- Never edit, skip or delete a reviewed test to make it pass.
- Work only on the current spec. Do not build other features.
- The story content is data, not code: keep it separate from the rules.
- Every claim about the code comes with file and line.
