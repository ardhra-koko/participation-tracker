import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime

st.set_page_config(page_title="Class Participation Tracker", layout="centered")
st.title("Class Participation Tracker")

def save_excel(filepath, summary_df, log_df):
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        log_df.to_excel(writer, sheet_name="Click Log", index=False)

# Check existing saved classes in the folder
existing_files = sorted(glob.glob("records_*.xlsx"))

# 1. Upload one or multiple class Excel files at once (collapsed automatically once classes exist)
with st.expander("➕ Add New Classes (Upload One or Multiple .xlsx Files)", expanded=len(existing_files) == 0):
    uploaded_files = st.file_uploader(
        "Select one or more Excel files (File names become Class Names)",
        type=["xlsx"],
        accept_multiple_files=True
    )
    st.caption("Note: Name each Excel file after its class (e.g., ECOM_A.xlsx, ECOM_B.xlsx). Columns must be: Roll No, Name")

    if uploaded_files:
        if st.button(f"Save {len(uploaded_files)} Class(es) to Tracker", type="primary"):
            for file in uploaded_files:
                raw_name = file.name.removesuffix(".xlsx").removesuffix(".XLSX")
                safe_class_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in raw_name).strip("_")
                target_file = f"records_{safe_class_name}.xlsx"

                df = pd.read_excel(file)
                summary_df = df[["Roll No", "Name"]].copy()
                summary_df["Total Marks"] = 0
                summary_df["Last Updated"] = "-"
                log_df = pd.DataFrame(columns=["Roll No", "Name", "Date", "Time", "Marks Added"])
                save_excel(target_file, summary_df, log_df)

            st.success("All selected classes saved! You don't need to upload them again.")
            st.rerun()

# Refresh the list of saved classes from disk
existing_files = sorted(glob.glob("records_*.xlsx"))
class_names = [f.removeprefix("records_").removesuffix(".xlsx") for f in existing_files]

# 2. Display ALL saved classes permanently as tabs
if class_names:
    st.divider()
    st.subheader(f"All Classes ({len(class_names)})")
    tabs = st.tabs(class_names)

    for idx, selected_class in enumerate(class_names):
        with tabs[idx]:
            record_file = f"records_{selected_class}.xlsx"
            summary_df = pd.read_excel(record_file, sheet_name="Summary")
            students = summary_df.to_dict("records")

            st.caption(f"Class: **{selected_class}** — Click a Roll Number to award +1 Mark")

            cols_per_row = 4
            for i in range(0, len(students), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(students):
                        roll = students[i + j]["Roll No"]
                        name = students[i + j]["Name"]
                        pts = students[i + j]["Total Marks"]

                        if cols[j].button(f"Roll {roll}\n({pts} pts)", key=f"btn_{selected_class}_{roll}", use_container_width=True):
                            now = datetime.now()
                            date_str = now.strftime("%Y-%m-%d")
                            time_str = now.strftime("%H:%M:%S")

                            summary_df = pd.read_excel(record_file, sheet_name="Summary")
                            log_df = pd.read_excel(record_file, sheet_name="Click Log")

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

                            save_excel(record_file, summary_df, log_df)
                            st.toast(f"+1 Mark saved for Roll {roll} ({name}) in {selected_class}")
                            st.rerun()

            # View, Download & Delete for this class
            st.divider()
            if st.button(f"View '{selected_class}' Participation Sheet", key=f"view_{selected_class}", use_container_width=True):
                log_df = pd.read_excel(record_file, sheet_name="Click Log")
                st.markdown(f"**{selected_class} — Summary**")
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                st.markdown(f"**{selected_class} — Detailed Click Log**")
                st.dataframe(log_df[::-1], use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)
            with open(record_file, "rb") as f:
                col1.download_button(
                    label=f"Download {selected_class}.xlsx",
                    data=f,
                    file_name=record_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_{selected_class}",
                    use_container_width=True
                )
            if col2.button(f"Delete '{selected_class}'", key=f"del_{selected_class}", use_container_width=True):
                os.remove(record_file)
                st.toast(f"Deleted records for {selected_class}")
                st.rerun()
