# Plot Twist

A short mystery game where clues unlock paths and choices change the ending.
Team project for Introduction to Programming, Nova SBE 2026/27.

## Play online

**https://plot-twist.streamlit.app/**

The online app runs `app_3d.py` (the 3D campus game) from the `main` branch. Its saved games are temporary: they can be lost when the app restarts.
The plain version without 3D is `app.py`.

## Team

| Name | Student number |
|---|---|
| Afonso Mendo Dias | 78097 |
| Guilherme Osório | 56699 |
| Maria da Cunha | 62123 |
| _(add your name)_ | _(add)_ |

## Getting started

1. Clone this repository with GitHub Desktop.
2. Open a terminal in the project folder and run `uv sync` (installs Python and the libraries).
3. Start the 3D game: `uv run streamlit run app_3d.py`
   (the plain version without 3D is `uv run streamlit run app.py`)
4. Run the tests: `uv run pytest`

## How we work

- `main` only changes through pull requests.
- Each feature has a spec in `specs/`, its own branch, and tests.
- Another team member reviews every pull request before it is merged.
