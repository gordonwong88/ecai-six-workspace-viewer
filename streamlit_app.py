"""F.6.3C.1 public six-workspace viewer. No database or secrets required."""
import streamlit as st
from public_six_workspace_viewer import render
st.set_page_config(page_title='EC-AI · Public Institutional Viewer', page_icon='🏦', layout='wide')
render()
