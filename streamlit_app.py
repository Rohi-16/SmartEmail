# app.py
import streamlit as st
import json
from summarizer import summarize_email
from classifier import score_priority
from utils import load_sample_emails

st.set_page_config(page_title="Smart Email Summarizer", layout="wide")

st.title("Smart Email Summarizer & Priority Sorter")
st.markdown("Upload or paste emails and get concise summaries plus urgency scores.")

with st.sidebar:
    st.header("Demo Data")
    use_sample = st.button("Load sample emails")

if use_sample:
    emails = load_sample_emails()
else:
    raw = st.text_area("Paste JSON list of emails (see sample) or leave blank to load sample", height=150)
    try:
        emails = json.loads(raw) if raw.strip() else load_sample_emails()
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        emails = load_sample_emails()

for i, em in enumerate(emails):
    st.markdown("---")
    st.subheader(f"{em.get('subject','(no subject)')} — From: {em.get('from','unknown')}")
    col1, col2 = st.columns([3,1])
    with col1:
        st.write(em.get('body',''))
    with col2:
        with st.spinner('Analyzing...'):
            summary = summarize_email(em.get('body',''))
            score, label, reasons = score_priority(em)
        st.metric("Priority", f"{label} ({score})")
        st.markdown("**Summary**")
        st.write(summary)
        st.markdown("**Why this score?**")
        for r in reasons:
            st.write(f"- {r}")

st.markdown("---")
st.info('This demo uses a mix of lightweight heuristics and optional LLM summarization. See README for setup.')