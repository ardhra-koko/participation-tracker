import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime, date

st.set_page_config(page_title="Class Participation Tracker", layout="centered")
st.title("Class Participation Tracker")

def save_excel(filepath, summary_df, log_df):
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        log_df.to_excel(writer, sheet_name="Click Log", index=False)

def rebuild_summary(summary_df, log_df):
    summary_df["Total Marks"] = 0.0
    summary_df["Last Updated"] = "-"
    if not log_df.empty:
        totals = log_df.groupby("Roll No")["Marks Added"].sum()
        for roll, total in totals.items():
            summary_df.loc[summary_df["Roll No"] == roll, "Total Marks"] = float(total)
            student_logs = log_df[log_df["Roll No"] == roll]
            last_row = student_logs.iloc[-1]
            summary_df.loc[summary_df["Roll No"] == roll, "Last Updated"] = f"{last_row['Date']} {last_row['Time']}"
    return summary_df

# 1. Batch upload new classes
existing_files = sorted(glob.glob("records_*.xlsx"))
with st.expander("➕ Add New Classes (Upload One or Multiple .xlsx Files)", expanded=len(existing_files) == 0):
    uploaded_files = st.file_uploader(
        "Select one or more Excel files (File names become Class Names)",
        type=["xlsx"],
        accept_multiple_files=True
    )
    st.caption("Note: Name each Excel file after its class (e.g., ECOM_A.xlsx). Columns must be: Roll No, Name")

    if uploaded_files:
        if st.button(f"Save {len(uploaded_files)} Class(es) to Tracker", type="primary"):
            for file in uploaded_files:
                raw_name = file.name.removesuffix(".xlsx").removesuffix(".XLSX")
                safe_class_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in raw_name).strip("_")
                target_file = f"records_{safe_class_name}.xlsx"

                df = pd.read_excel(file)
                summary_df = df[["Roll No", "Name"]].copy()
                summary_df["Total Marks"] = 0.0
                summary_df["Last Updated"] = "-"
                log_df = pd.DataFrame(columns=["Roll No", "Name", "Date", "Time", "Marks Added"])
                save_excel(target_file, summary_df, log_df)

            st.success("All selected classes saved!")
            st.rerun()

# 2. Session Date & Mark Value Controls
existing_files = sorted(glob.glob("records_*.xlsx"))
class_names = [f.removeprefix("records_").removesuffix(".xlsx") for f in existing_files]

if class_names:
    st.divider()
    ctrl_col1, ctrl_col2 = st.columns([1, 2])
    selected_date = ctrl_col1.date_input("Class Date", value=date.today())
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    mark_choice = ctrl_col2.radio(
        "Marks to Award per Click",
        options=[0.25, 0.5, 0.75, 1.0],
        index=3,
        horizontal=True
    )

    st.subheader(f"All Classes ({len(class_names)}) — {selected_date_str}")
    tabs = st.tabs(class_names)

    for idx, selected_class in enumerate(class_names):
        with tabs[idx]:
            record_file = f"records_{selected_class}.xlsx"
            summary_df = pd.read_excel(record_file, sheet_name="Summary")
            log_df = pd.read_excel(record_file, sheet_name="Click Log")

            if not log_df.empty:
                log_df["Date"] = log_df["Date"].astype(str)

            # Fresh marks for the selected date only
            day_logs = log_df[log_df["Date"] == selected_date_str] if not log_df.empty else pd.DataFrame()
            day_totals = day_logs.groupby("Roll No")["Marks Added"].sum().to_dict() if not day_logs.empty else {}

            # Single-click Undo button at the top (directly deletes last entry from Excel)
            top_left, top_right = st.columns([2, 1])
            top_left.caption(f"Fresh marks for **{selected_date_str}** (All-time totals are saved in Excel)")
            if not log_df.empty:
                last_entry = log_df.iloc[-1]
                if top_right.button(f"↩️ Undo Roll {last_entry['Roll No']} (+{last_entry['Marks Added']:g})", key=f"undo_{selected_class}", use_container_width=True):
                    log_df = log_df.iloc[:-1]
                    summary_df = rebuild_summary(summary_df, log_df)
                    save_excel(record_file, summary_df, log_df)
                    st.toast(f"Removed Roll {last_entry['Roll No']} (+{last_entry['Marks Added']:g}) from records")
                    st.rerun()

            # 4-Column Roll Number Grid
            students = summary_df.to_dict("records")
            cols_per_row = 4
            for i in range(0, len(students), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(students):
                        roll = students[i + j]["Roll No"]
                        name = students[i + j]["Name"]
                        today_pts = day_totals.get(roll, 0)
                        pts_display = f"{today_pts:g}"

                        if cols[j].button(f"Roll {roll}\n({pts_display} pts)", key=f"btn_{selected_class}_{roll}", use_container_width=True):
                            time_str = datetime.now().strftime("%H:%M:%S")

                            new_entry = pd.DataFrame([{
                                "Roll No": roll,
                                "Name": name,
                                "Date": selected_date_str,
                                "Time": time_str,
                                "Marks Added": float(mark_choice)
                            }])
                            log_df = pd.concat([log_df, new_entry], ignore_index=True)
                            summary_df = rebuild_summary(summary_df, log_df)

                            save_excel(record_file, summary_df, log_df)
                            st.toast(f"+{mark_choice:g} saved for Roll {roll} ({name}) on {selected_date_str}")
                            st.rerun()

            # Clean Read-Only View, Download & Delete Class
            st.divider()
            if st.button(f"View '{selected_class}' Participation Sheet", key=f"view_{selected_class}", use_container_width=True):
                st.markdown(f"**{selected_class} — Cumulative Summary (All Dates)**")
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

