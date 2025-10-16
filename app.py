import streamlit as st
import pandas as pd
import os
from readFile import extract_text_from_pdf
from parser import extract_info
from generate_statements import generate_statements

st.set_page_config(page_title="Credit Card Analyzer", layout="wide", page_icon="💳")

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    * {
        font-family: 'Poppins', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 48px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #444;
        font-size: 20px;
        margin-bottom: 50px;
    }
    .centered {
        text-align: center;
    }
    div[data-testid="stFileUploader"] {
        display: flex;
        justify-content: center;
    }
    div.block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-title'>💳 Credit Card Statement Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Upload or Generate Statements & Get Instant Insights</div>", unsafe_allow_html=True)

mode = st.segmented_control("Select Mode", options=["📤 Upload Statement", "🧾 Generate Fake Statements"])

st.divider()

if mode == "📤 Upload Statement":
    uploaded_file = st.file_uploader("📁 Upload Your PDF Statement", type=["pdf"], label_visibility="collapsed")
    if uploaded_file is not None:
        with st.spinner("Extracting details..."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())
            text = extract_text_from_pdf("temp.pdf")
            info = extract_info(text)
        st.markdown("<h3 class='centered' style='color:#2E7D32;'>✅ Extraction Complete</h3>", unsafe_allow_html=True)
        st.json(info)
        df = pd.DataFrame([info])
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Extracted Data (CSV)",
            data=csv,
            file_name="credit_card_summary.csv",
            mime="text/csv",
            use_container_width=True
        )
else:
    st.markdown("<h3 class='centered'>🧠 Generate Realistic Fake Credit Card Statements</h3>", unsafe_allow_html=True)
    if st.button("🚀 Generate Now", use_container_width=True):
        os.makedirs("statements", exist_ok=True)
        with st.spinner("Generating fake statements..."):
            generate_statements()
        st.markdown("<h4 class='centered' style='color:#2E7D32;'>✅ Fake Statements Generated Successfully</h4>", unsafe_allow_html=True)
        pdfs = [f for f in os.listdir("statements") if f.endswith(".pdf")]
        extracted_data = []
        for pdf in pdfs:
            text = extract_text_from_pdf(os.path.join("statements", pdf))
            info = extract_info(text)
            extracted_data.append(info)
        if extracted_data:
            df = pd.DataFrame(extracted_data)
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "⬇️ Download All Extracted Data (CSV)",
                df.to_csv(index=False).encode("utf-8"),
                "all_statements_data.csv",
                "text/csv",
                use_container_width=True
            )
