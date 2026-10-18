from pathlib import Path
import json
import pandas as pd
import streamlit as st
from devpulse.analyzer import analyze_repository

st.set_page_config(page_title="DevPulse", page_icon="📈", layout="wide")
st.title("📈 DevPulse")
st.caption("Local-first Git repository health analyzer")
repo_path = st.text_input("Local Git repository path", placeholder=r"C:\path\to\repository")
st.info("Analysis runs locally. DevPulse does not upload repository contents to an external service.")

if st.button("Analyze repository", type="primary"):
    if not repo_path.strip():
        st.error("Enter a repository path first.")
    else:
        with st.spinner("Analyzing repository..."):
            result = analyze_repository(Path(repo_path.strip()).expanduser())
        if result.get("error"):
            st.error(result["error"])
        else:
            m = result["metrics"]
            cols = st.columns(4)
            cols[0].metric("Commits", m["commits"])
            cols[1].metric("Contributors", m["contributors"])
            cols[2].metric("Tracked files", m["tracked_files"])
            cols[3].metric("TODO/FIXME", m["todo_markers"])
            st.subheader("Repository summary")
            st.write(f"**Path:** `{result['path']}`")
            st.write(f"**Branch:** {result['branch'] or 'Unavailable'}")
            st.write(f"**Working tree:** {'Clean' if result['working_tree_clean'] else 'Has uncommitted changes'}")
            left, right = st.columns(2)
            with left:
                st.subheader("Commit activity by author")
                st.dataframe(pd.DataFrame(result["authors"]), use_container_width=True, hide_index=True)
            with right:
                st.subheader("Largest tracked files (5 MiB+)")
                st.dataframe(pd.DataFrame(result["largest_files"]), use_container_width=True, hide_index=True)
            st.subheader("File-type distribution")
            st.dataframe(pd.DataFrame([{"extension": k, "count": v} for k, v in result["file_types"].items()]), use_container_width=True, hide_index=True)
            st.subheader("TODO / FIXME markers")
            st.dataframe(pd.DataFrame(result["todo_items"]), use_container_width=True, hide_index=True)
            st.download_button("Download JSON report", json.dumps(result, indent=2), "devpulse-report.json", "application/json")
