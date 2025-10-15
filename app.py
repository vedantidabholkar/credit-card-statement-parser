import streamlit as st
import tempfile
import os
import json
from parser.parser_factory import get_parser
from parser.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Credit Card Statement Parser",  layout="centered")

st.title(" Credit Card Statement Parser")
st.caption("Upload a credit card statement PDF and extract key details automatically!")

uploaded_file = st.file_uploader(" Upload your PDF file", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.info("Processing your file... please wait ")

    try:
        parser = get_parser(temp_path)
        data = parser.extract_data()
        logger.info(f"Parsed file successfully: {uploaded_file.name}")

        st.success("Data extracted successfully!")
        st.subheader(" Extracted Details")
        st.json(data)

        # Optional download option
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(data, indent=4),
            file_name="parsed_statement.json",
            mime="application/json"
        )

    except Exception as e:
        logger.error(f"Error processing {uploaded_file.name}: {e}")
        st.error(f" Error: {e}")

st.markdown("---")
st.caption("Developed by Nishita Patel • Powered by Streamlit & Python ")
