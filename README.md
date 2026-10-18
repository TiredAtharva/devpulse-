# DevPulse 📈

**A local-first Git repository health analyzer built with Python and Streamlit.**

DevPulse helps developers understand their repositories through commit statistics, contributor activity, file-type distribution, large-file detection, and TODO/FIXME tracking.

## Features

- 📊 Commit and contributor statistics
- 🌿 Current branch and working-tree status
- 📁 Tracked file and file-type analysis
- 🔍 Large-file detection
- 📝 TODO/FIXME comment tracking
- 📥 JSON report export
- 🔒 Local analysis without uploading repository contents

## Tech Stack

- Python
- Streamlit
- Pandas
- Git
- Pytest

## Getting Started

```bash
git clone https://github.com/checkmate-open/devpulse-.git
cd devpulse-
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r DevPulse/requirements.txt
streamlit run DevPulse/app.py
```

## Testing

```bash
pip install pytest
python -m pytest DevPulse/tests
```

## License

This project is licensed under the MIT License.
