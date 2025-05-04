
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

st.title("IELTS Feedback Evaluation Tool")

# Upload audio and text
uploaded_audio = st.file_uploader("Upload your speaking response (audio file)", type=["mp3", "wav", "m4a"])
text_input = st.text_area("Paste your written response here")

# Input Band scores manually for demo
fluency = st.slider("Fluency & Coherence", 0.0, 9.0, 6.0, 0.5)
lexical = st.slider("Lexical Resource", 0.0, 9.0, 6.0, 0.5)
grammar = st.slider("Grammatical Range & Accuracy", 0.0, 9.0, 6.0, 0.5)
pronunciation = st.slider("Pronunciation", 0.0, 9.0, 6.0, 0.5)
overall = round((fluency + lexical + grammar + pronunciation) / 4, 1)

if st.button("Submit Feedback"):
    st.success(f"Estimated Overall Band Score: {overall}")
    st.markdown("Feedback submitted.")

    # Save to Google Sheet if configured
    if "GCREDS_JSON" in st.secrets:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(st.secrets["GCREDS_JSON"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("IELTS Feedback").sheet1
        sheet.append_row([text_input, fluency, lexical, grammar, pronunciation, overall])
