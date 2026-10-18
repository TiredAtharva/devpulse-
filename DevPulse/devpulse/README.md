# DevPulse

DevPulse is a local-first Python + Streamlit tool that summarizes the health of a Git repository.

## Features

- Commit count and commit counts by author
- Current branch and working-tree status
- Tracked file counts and file-type distribution
- Large tracked-file candidates (5 MiB or larger)
- TODO/FIXME markers in common text-based files
- JSON report export

## Privacy

Analysis runs locally. DevPulse does not upload repository contents or call external APIs. Reports can contain local paths, Git author names/emails, and TODO/FIXME snippets; review a report before sharing it.

## Requirements

- Python 3.11 or newer recommended
- Git installed and available on PATH

## Run on Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Run on macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Enter the path to a local Git repository in the app. DevPulse reads Git metadata and tracked files; it does not execute code from the repository being analyzed.

## Tests

```bash
python -m pytest
```

## Limitations

- Statistics reflect the local clone and its available history.
- Git author names/emails may not represent unique people.
- Large files are flagged as candidates, not automatically judged unnecessary.
- TODO/FIXME detection is heuristic and scans selected text extensions only.
- DevPulse does not modify analyzed repositories.

## Screenshots

Add screenshots of the running application here.
