import streamlit as st
import pandas as pd

st.set_page_config(page_title="Class Participation Tracker", layout="centered")
st.title("Class Participation Tracker")

# Upload button and format note
uploaded_file = st.file_uploader("Upload Student List (.xlsx)", type=["xlsx"])
st.caption("Note: The uploaded Excel file should contain the columns: Roll No, Name")

# Display the uploaded Excel sheet without the 0-based index column
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    st.dataframe(df, use_container_width=True, hide_index=True)
