"""The tests run on GitHub (specs/tests-on-github.md).

The workflow is read as text: the project has no YAML library, and the checks only need its lines.
"""

from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
WORKFLOW = PROJECT / ".github" / "workflows" / "tests.yml"
README = (PROJECT / "README.md").read_text(encoding="utf-8")


def lines():
    return [line.strip() for line in WORKFLOW.read_text(encoding="utf-8").splitlines()]


def test_the_workflow_exists_and_is_named():
    assert WORKFLOW.exists()
    assert "name: Tests" in lines()


def test_it_runs_on_every_push_and_pull_request():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "on:" in lines()
    assert "push:" in lines() and "pull_request:" in lines()
    assert "branches" not in text   # every branch, so a pull request's branch is checked too


def test_it_can_only_read_the_repository():
    found = lines()
    assert found[found.index("permissions:") + 1] == "contents: read"


def test_it_installs_the_locked_libraries_and_runs_pytest():
    found = lines()
    assert "runs-on: ubuntu-latest" in found
    assert "- uses: actions/checkout@v4" in found
    assert "- uses: astral-sh/setup-uv@v6" in found
    assert "- run: uv sync --frozen" in found
    assert "- run: uv run pytest" in found


def test_it_checks_the_javascript():
    found = lines()
    assert "- uses: actions/setup-node@v4" in found
    assert "node-version: 22" in found
    for name in ("play.js", "table.js", "photo.js"):
        assert f"- run: node --check prototypes/campus-3d/{name}" in found
    assert "- run: node tests/continuous-conversations.cjs" in found


def test_the_readme_shows_the_badge_of_main():
    badge = ("[![Tests](https://github.com/afonsodias119-cpu/Plot-Twist---Group-Assignment/actions/workflows/tests.yml/badge.svg"
             "?branch=main)](https://github.com/afonsodias119-cpu/Plot-Twist---Group-Assignment/actions/workflows/tests.yml)")
    assert badge in README
    assert README.index(badge) < README.index("## Play online")


def test_the_readme_draws_one_command():
    start = README.index("```mermaid")
    diagram = README[start:README.index("```", start + 3)]
    for step in ("play.js", "bridge", "keyed_command", "command", "logic.py", "db.py"):
        assert step in diagram, step
