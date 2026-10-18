
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devpulse.analyzer import analyze_repository


def _git(repository: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )


def test_analyzes_git_activity_structure_todos_and_code_quality(
    tmp_path: Path,
) -> None:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.name", "Test Contributor")
    _git(tmp_path, "config", "user.email", "test@example.invalid")

    source = tmp_path / "sample.py"
    source.write_text(
        "# TODO: make this clearer\n\ndef ready():\n    return True\n",
        encoding="utf-8",
    )
    (tmp_path / "notes.txt").write_text(
        "Repository notes\n", encoding="utf-8"
    )

    _git(tmp_path, "add", "sample.py", "notes.txt")
    _git(tmp_path, "commit", "-q", "-m", "Add sample files")

    report = analyze_repository(tmp_path)

    assert report.git.commit_count == 1
    assert report.git.contributor_count == 1
    assert report.git.contributors[0].name == "Test Contributor"
    assert report.files.file_count == 2
    assert report.files.files_by_extension[".py"] == 1
    assert report.quality.python_file_count == 1
    assert report.quality.syntax_errors == []
    assert [
        (finding.marker, finding.line) for finding in report.todos
    ] == [("TODO", 1)]


def test_handles_repository_without_commits(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    (tmp_path / "readme.txt").write_text(
        "No commits yet\n", encoding="utf-8"
    )

    report = analyze_repository(tmp_path)

    assert report.git.commit_count == 0
    assert report.git.contributors == []
    assert report.git.diagnostics == []
    assert "no commits yet" in report.health_summary.lower()


def test_analyzes_directory_without_git_history(tmp_path: Path) -> None:
    (tmp_path / "module.py").write_text(
        "def valid():\n    return 1\n", encoding="utf-8"
    )

    report = analyze_repository(tmp_path)

    assert report.files.file_count == 1
    assert report.git.commit_count == 0
    assert report.git.diagnostics


def test_reports_syntax_errors_and_large_files(tmp_path: Path) -> None:
    (tmp_path / "broken.py").write_text(
        "def broken(:\n", encoding="utf-8"
    )
    (tmp_path / "payload.bin").write_bytes(b"x" * 20)

    report = analyze_repository(
        tmp_path, large_file_threshold_bytes=10
    )

    assert report.quality.syntax_errors[0]["path"] == "broken.py"
    assert report.files.large_files == [
        {"path": "payload.bin", "size_bytes": 20}
    ]


def test_skips_virtual_environments_and_private_environment_contents(
    tmp_path: Path,
) -> None:
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "ignored.py").write_text(
        "# TODO: hidden\n", encoding="utf-8"
    )
    (tmp_path / ".env").write_text(
        "TOKEN=do-not-display\n", encoding="utf-8"
    )
    (tmp_path / "app.py").write_text(
        "print('ok')\n", encoding="utf-8"
    )

    report = analyze_repository(tmp_path)

    assert report.files.file_count == 2
    assert ".venv" in report.files.excluded_directories
    assert report.todos == []
    assert all(
        "do-not-display" not in finding.text
        for finding in report.todos
    )


@pytest.mark.parametrize("path", ["missing-folder", ""])
def test_rejects_missing_or_empty_path(
    path: str, tmp_path: Path
) -> None:
    candidate = tmp_path / path if path else Path(path)

    with pytest.raises(ValueError, match="cannot be resolved"):
        analyze_repository(candidate)


def test_rejects_non_directory_path(tmp_path: Path) -> None:
    file_path = tmp_path / "not-a-directory.txt"
    file_path.write_text("content", encoding="utf-8")

    with pytest.raises(ValueError, match="not a directory"):
        analyze_repository(file_path)


def test_rejects_non_positive_large_file_threshold(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        analyze_repository(tmp_path, large_file_threshold_bytes=0)


def test_caps_todo_findings_at_1000(tmp_path: Path) -> None:
    source = tmp_path / "many_todos.py"
    source.write_text(
        "".join(
            f"# TODO: item {number}\n"
            for number in range(1005)
        ),
        encoding="utf-8",
    )

    report = analyze_repository(tmp_path)

    assert len(report.todos) == 1000
    assert all(finding.marker == "TODO" for finding in report.todos)
