from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd
import streamlit as st

from devpulse.analyzer import analyze_repository


st.set_page_config(page_title="DevPulse", page_icon="📈", layout="wide")
st.title("DevPulse")
st.caption("A local-first snapshot of Git activity, repository structure, and maintainability.")
st.info(
    "Analysis runs on this machine. DevPulse does not upload repository contents "
    "or contact external analysis services."
)

repository_path = st.text_input(
    "Local Git repository path",
    placeholder=r"C:\path\to\your\repository",
    help="Enter the path to a folder on the machine running this Streamlit app.",
)

if st.button("Analyze repository", type="primary", disabled=not repository_path.strip()):
    try:
        with st.spinner("Analyzing local repository..."):
            report = analyze_repository(Path(repository_path.strip()))
    except (OSError, ValueError) as error:
        st.error(str(error))
    else:
        st.session_state["devpulse_report"] = asdict(report)

report_data = st.session_state.get("devpulse_report")
if report_data:
    st.divider()
    st.subheader(f"Repository: {report_data['repository_name']}")
    st.caption(report_data["repository_path"])

    git = report_data["git"]
    file_stats = report_data["files"]
    quality = report_data["quality"]

    st.subheader("Health summary")
    st.write(report_data["health_summary"])

    if git["diagnostics"]:
        for diagnostic in git["diagnostics"]:
            st.warning(diagnostic)

    overview = st.columns(4)
    overview[0].metric("Commits", git["commit_count"])
    overview[1].metric("Contributors", git["contributor_count"])
    overview[2].metric("Files", file_stats["file_count"])
    overview[3].metric("Large files", len(file_stats["large_files"]))

    activity, contributors = st.columns(2)
    with activity:
        st.subheader("Commit activity by month")
        activity_rows = git["commits_by_month"]
        if activity_rows:
            chart_data = pd.DataFrame(activity_rows).set_index("month")
            st.bar_chart(chart_data["commits"])
        else:
            st.write("No commits are available in this repository's Git history.")
        if git["first_commit_date"]:
            st.caption(
                f"History: {git['first_commit_date']} to {git['latest_commit_date']}"
            )

    with contributors:
        st.subheader("Contributors")
        if git["contributors"]:
            st.dataframe(pd.DataFrame(git["contributors"]), hide_index=True)
        else:
            st.write("No contributor activity found.")

    structure, quality_column = st.columns(2)
    with structure:
        st.subheader("Repository structure")
        st.write(f"Directories: {file_stats['directory_count']}")
        if file_stats["files_by_extension"]:
            extensions = pd.DataFrame(
                [
                    {"Extension": extension, "Files": count}
                    for extension, count in file_stats["files_by_extension"].items()
                ]
            )
            st.dataframe(extensions, hide_index=True)
        st.write(f"Generated-file candidates: {len(file_stats['generated_candidates'])}")
        st.write(f"Excluded directories: {', '.join(file_stats['excluded_directories']) or 'None'}")

    with quality_column:
        st.subheader("Code quality indicators")
        st.write(f"Python files: {quality['python_file_count']}")
        st.write(f"Python syntax errors: {len(quality['syntax_errors'])}")
        st.write(f"Python files over 500 lines: {len(quality['long_python_files'])}")
        st.write(f"Functions over 50 lines: {len(quality['long_functions'])}")
        st.write(f"TODO/FIXME markers: {len(report_data['todos'])}")
        st.caption(
            "These are lightweight indicators, not a full linter, security audit, or quality score."
        )

    if file_stats["large_files"]:
        st.subheader("Large files (5 MiB or larger)")
        st.dataframe(pd.DataFrame(file_stats["large_files"]), hide_index=True)
    if file_stats["generated_candidates"]:
        st.subheader("Potentially generated files and directories")
        st.dataframe(pd.DataFrame(file_stats["generated_candidates"]), hide_index=True)
    if quality["syntax_errors"]:
        st.subheader("Python syntax errors")
        st.dataframe(pd.DataFrame(quality["syntax_errors"]), hide_index=True)
    if quality["long_python_files"] or quality["long_functions"]:
        st.subheader("Long Python files and functions")
        st.write("Files over 500 lines")
        st.dataframe(pd.DataFrame(quality["long_python_files"]), hide_index=True)
        st.write("Functions over 50 lines")
        st.dataframe(pd.DataFrame(quality["long_functions"]), hide_index=True)
    if report_data["todos"]:
        st.subheader("TODO/FIXME comments")
        st.dataframe(pd.DataFrame(report_data["todos"]), hide_index=True)
