from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContributorStats:
    name: str
    commits: int


@dataclass
class GitStats:
    commit_count: int = 0
    contributor_count: int = 0
    first_commit_date: str | None = None
    latest_commit_date: str | None = None
    contributors: list[ContributorStats] = field(default_factory=list)
    commits_by_month: list[dict[str, int | str]] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)


@dataclass
class FileStats:
    file_count: int = 0
    directory_count: int = 0
    files_by_extension: dict[str, int] = field(default_factory=dict)
    large_files: list[dict[str, int | str]] = field(default_factory=list)
    generated_candidates: list[dict[str, str]] = field(default_factory=list)
    excluded_directories: list[str] = field(default_factory=list)


@dataclass
class CodeQuality:
    python_file_count: int = 0
    syntax_errors: list[dict[str, int | str]] = field(default_factory=list)
    long_python_files: list[dict[str, int | str]] = field(default_factory=list)
    functions_over_50_lines: list[dict[str, int | str]] = field(default_factory=list)


@dataclass
class TodoFinding:
    path: str
    line: int
    marker: str
    text: str


@dataclass
class RepositoryReport:
    repository_name: str
    repository_path: str
    git: GitStats
    files: FileStats
    quality: CodeQuality
    todos: list[TodoFinding]
    health_summary: str
