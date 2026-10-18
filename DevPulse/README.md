# DevPulse

**DevPulse — Developer Productivity & Repository Health Analyzer** is a local-first
Streamlit application for inspecting a Git repository's activity, structure, and
lightweight maintainability indicators. Analysis runs against a directory on the
machine running the app; repository contents are not uploaded to a service.

## Features

- Git commit totals, activity by month, contributor names, and first/latest commit dates.
- File and directory counts grouped by file extension.
- Large-file and potentially generated-file candidates.
- Python syntax-error, long-file, and long-function indicators.
- TODO/FIXME markers in common source files.
- A concise summary based only on observed findings.
- Graceful handling of directories without Git history or repositories with no commits.

## Requirements

- Python 3.10 or newer.
- Git installed and available on `PATH` for commit-history analysis. Git is optional
  for file and code inspection.

## Installation

From the project directory, create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Start the interface from the project directory:

```bash
streamlit run app.py
```

In the browser, enter the path to a local repository and select **Analyze repository**.
The path must be accessible to the machine running Streamlit. If Streamlit is hosted
remotely, a path on your personal computer is not accessible to that server.

Run the automated tests with:

```bash
pytest
```

## Privacy and limitations

- DevPulse does not make network requests to upload analyzed repository contents.
- Repository paths and findings are shown in the local Streamlit interface. Avoid
  sharing screenshots or reports that contain private repository names or paths.
- Git statistics come from local `git log` author names and authored dates; they do not
  verify identities and may include rewritten or incomplete history.
- Common virtual-environment, cache, and dependency directories are excluded from
  file inventory. Generated-file detection uses simple name and directory heuristics.
- TODO/FIXME scanning is limited to common source-code extensions and source files up
  to 1 MB. Environment files and common private-key filenames are not scanned.
- Python maintainability indicators are intentionally basic. This is not a linter,
  security scanner, dependency audit, or comprehensive health score.
- Large-file detection defaults to 5 MiB. The report lists at most the 100 largest
  matching files.

## Screenshots

No screenshots are bundled yet. Add screenshots of the running application here when
available; do not include private repository information.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
