# The tests run on GitHub

New file `.github/workflows/tests.yml`, a badge and a diagram in `README.md`. No game code changes. No reviewed test changes.

## Before writing the spec

- **Product and user:** the teaching staff reviewing the repository on their own, and the team reviewing pull requests.
- **Trigger:** a push to any branch, or a pull request.
- **Before:** the tests only run on our own computers. Nothing on GitHub shows that they pass on `main` (course rubric, Verification: "all pass on main"), and a reviewer has to trust the pull request description.
- **After:** GitHub Actions runs every test on each push and pull request, the pull request page shows a green tick or a red cross, and the README shows a "tests passing" badge for `main`. The README also has a diagram of how one click travels through the code.

## Why

As a teammate reviewing a pull request, I want GitHub to tell me whether the tests pass, so that a broken change never reaches `main` unnoticed.

## What

1. `.github/workflows/tests.yml`, named "Tests", on `push` and `pull_request`, on `ubuntu-latest`:
   - check out the code (`actions/checkout@v4`);
   - install uv (`astral-sh/setup-uv@v6`) and the exact locked libraries (`uv sync --frozen`);
   - run `uv run pytest`;
   - install Node (`actions/setup-node@v4`, Node 22), check the syntax of `play.js`, `table.js` and `photo.js` (`node --check`) and run `tests/continuous-conversations.cjs`.
   - Read-only permission on the repository (`permissions: contents: read`): the workflow cannot change anything.
2. `README.md`: the badge `actions/workflows/tests.yml/badge.svg?branch=main` under the title, and a Mermaid diagram (GitHub draws it) of one command: page → bridge → `keyed_command` (key) → `command` (checks) → `game.py` / `logic.py` → `db.py` → reply.

## Limits

- GitHub Actions is free for public repositories; if GitHub is down, the badge is grey but the app is not affected.
- The workflow checks; it does not deploy. Streamlit Community Cloud still deploys `main` by itself.

## Out of scope

Blocking merges when the tests fail (a repository setting, the team's choice), browser tests of the 3D scene.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_tests_on_github.py`: the workflow's triggers, permission, the uv and pytest steps, the Node steps, and the README badge and diagram.
- [ ] The workflow run on GitHub for this branch is green.
