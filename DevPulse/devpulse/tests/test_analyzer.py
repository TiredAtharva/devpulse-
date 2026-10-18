import subprocess
from pathlib import Path
from devpulse.analyzer import analyze_repository


def init_repo(path: Path) -> None:
    path.mkdir()
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "Test User"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "test@example.com"], check=True)


def test_missing_path(tmp_path):
    assert "error" in analyze_repository(tmp_path / "missing")


def test_non_git_directory(tmp_path):
    folder = tmp_path / "plain"
    folder.mkdir()
    assert "error" in analyze_repository(folder)


def test_analyzes_repo_and_todo(tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    (repo / "sample.py").write_text("# TODO: improve this\nprint('hello')\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "sample.py"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, capture_output=True)
    result = analyze_repository(repo)
    assert "error" not in result
    assert result["metrics"]["commits"] == 1
    assert result["metrics"]["tracked_files"] == 1
    assert result["metrics"]["todo_markers"] == 1
