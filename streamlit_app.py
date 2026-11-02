"""Standalone read-only EC-AI public viewer — no DB connection."""
import streamlit as st
from public_six_workspace_viewer import run

st.set_page_config(page_title="EC-AI | Institutional Public Viewer",page_icon="🏦",layout="wide",initial_sidebar_state="expanded")
run()
