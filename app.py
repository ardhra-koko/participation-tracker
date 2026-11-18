import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Class Participation Tracker", layout="centered")
st.title("Class Participation Tracker")

RECORD_FILE = "participation_records.xlsx"

def save_excel(summary_df, log_df):
    with pd.ExcelWriter(RECORD_FILE, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        log_df.to_excel(writer, sheet_name="Click Log", index=False)

# Show uploader inside an expander if records already exist, or open if starting fresh
file_exists = os.path.exists(RECORD_FILE)
with st.expander("Upload New Student List (.xlsx)", expanded=not file_exists):
    uploaded_file = st.file_uploader("Choose Excel File", type=["xlsx"])
    st.caption("Note: The uploaded Excel file should contain the columns: Roll No, Name")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        if not file_exists or st.button("Initialize / Overwrite Class List with This File"):
            summary_df = df[["Roll No", "Name"]].copy()
            summary_df["Total Marks"] = 0
            summary_df["Last Updated"] = "-"
            log_df = pd.DataFrame(columns=["Roll No", "Name", "Date", "Time", "Marks Added"])
            save_excel(summary_df, log_df)
            st.success("Student list loaded and saved!")
            st.rerun()

# Automatically load buttons if participation_records.xlsx exists
if os.path.exists(RECORD_FILE):
    summary_df = pd.read_excel(RECORD_FILE, sheet_name="Summary")
    students = summary_df.to_dict("records")

    st.divider()
    st.subheader("Click a Roll Number (+1 Mark)")

    cols_per_row = 4
    for i in range(0, len(students), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(students):
                roll = students[i + j]["Roll No"]
                name = students[i + j]["Name"]
                pts = students[i + j]["Total Marks"]

                if cols[j].button(f"Roll {roll}\n({pts} pts)", key=f"btn_{roll}", use_container_width=True):
                    now = datetime.now()
                    date_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H:%M:%S")

                    summary_df = pd.read_excel(RECORD_FILE, sheet_name="Summary")
                    log_df = pd.read_excel(RECORD_FILE, sheet_name="Click Log")

                    summary_df.loc[summary_df["Roll No"] == roll, "Total Marks"] += 1
                    summary_df.loc[summary_df["Roll No"] == roll, "Last Updated"] = f"{date_str} {time_str}"

                    new_entry = pd.DataFrame([{
                        "Roll No": roll,
                        "Name": name,
                        "Date": date_str,
                        "Time": time_str,
                        "Marks Added": 1
                    }])
                    log_df = pd.concat([log_df, new_entry], ignore_index=True)

                    save_excel(summary_df, log_df)
                    st.toast(f"+1 Mark saved for Roll {roll} ({name})")
                    st.rerun()

    # View, Download, and Reset Section
    st.divider()
    if st.button("View Saved Participation Excel Sheet", use_container_width=True):
        log_df = pd.read_excel(RECORD_FILE, sheet_name="Click Log")
        st.subheader("Summary (Total Marks per Student)")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        st.subheader("Detailed Click Log (Date & Time)")
        st.dataframe(log_df[::-1], use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with open(RECORD_FILE, "rb") as f:
        col1.download_button(
            label="Download Excel File",
            data=f,
            file_name="participation_records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    if col2.button("Reset / Clear All Records", use_container_width=True):
        os.remove(RECORD_FILE)
        st.toast("All records cleared!")
        st.rerun()
