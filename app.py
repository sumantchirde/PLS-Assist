# app.py
import streamlit as st

st.set_page_config(
    page_title="PLS-Assist",
    page_icon="📊",
    layout="wide"
)

from ui.upload_page import show as show_upload
from ui.report_page import show as show_report    # ← ADD
from ui.chat_page   import show as show_chat

tab1, tab2, tab3 = st.tabs(["📁 Model Setup", "📄 Report", "💬 Chatbot"])   # ← 3 tabs

with tab1:
    show_upload()

with tab2:
    show_report()                                  # ← ADD

with tab3:
    show_chat()