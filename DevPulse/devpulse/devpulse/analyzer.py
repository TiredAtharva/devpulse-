from collections import Counter
from pathlib import Path
import subprocess

TEXT_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sh", ".sql"}
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build", ".next"}
LARGE_FILE_BYTES = 5 * 1024 * 1024


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True,
        text=True, timeout=15, encoding="utf-8", errors="replace"
    )
    return completed.stdout.strip()


def analyze_repository(repo: Path) -> dict:
    repo = repo.expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        return {"error": f"Directory does not exist: {repo}"}
    try:
        _git(repo, "rev-parse", "--show-toplevel")
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return {"error": "The selected path is not a Git repository, or Git is unavailable."}

    try:
        branch = _git(repo, "branch", "--show-current")
        status = _git(repo, "status", "--porcelain")
        tracked = [p for p in _git(repo, "ls-files", "-z").split("\0") if p]
        log = _git(repo, "log", "--format=%an%x09%ae", "--all")
        author_counts = Counter()
        for line in log.splitlines():
            parts = line.split("\t", 1)
            if parts:
                author_counts[parts[0]] += 1
        commit_count = int(_git(repo, "rev-list", "--count", "--all") or "0")
    except subprocess.SubprocessError as exc:
        return {"error": f"Git could not analyze this repository: {exc}"}

    file_types, large_files, todos = Counter(), [], []
    for relative in tracked:
        path = repo / relative
        if any(part in IGNORED_DIRS for part in Path(relative).parts):
            continue
        try:
            if not path.is_file():
                continue
            size = path.stat().st_size
            file_types[path.suffix.lower() or "[no extension]"] += 1
            if size >= LARGE_FILE_BYTES:
                large_files.append({"file": relative, "size_mb": round(size / 1048576, 2)})
            if path.suffix.lower() in TEXT_SUFFIXES and size <= 1_000_000:
                for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    upper = line.upper()
                    if "TODO" in upper or "FIXME" in upper:
                        todos.append({"file": relative, "line": line_no, "marker": "FIXME" if "FIXME" in upper else "TODO", "text": line.strip()[:240]})
        except OSError:
            continue

    authors = [{"author": name, "commits": count} for name, count in author_counts.most_common()]
    large_files.sort(key=lambda item: item["size_mb"], reverse=True)
    return {
        "path": str(repo), "branch": branch, "working_tree_clean": not bool(status),
        "metrics": {"commits": commit_count, "contributors": len(author_counts), "tracked_files": len(tracked), "todo_markers": len(todos)},
        "authors": authors, "largest_files": large_files[:20], "file_types": dict(file_types.most_common()),
        "todo_items": todos,
    }
