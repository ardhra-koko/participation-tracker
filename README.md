# Class Participation Tracker

A simple Python and Streamlit web app for tracking student class participation using clickable roll number buttons and automated Excel logging.

## Features
- **Excel Student Import:** Upload a `.xlsx` file (`Roll No`, `Name`) to dynamically generate a 4-column button grid.
- **One-Click Point Logging:** Click any student's roll number to award `+1` mark.
- **Multi-Sheet Excel Storage:** Automatically saves and updates `participation_records.xlsx` with two tabs:
  - **Summary:** Running total marks and last updated timestamp per student.
  - **Click Log:** Detailed history of every click with exact date and time.
- **View, Download & Reset:** Inspect records directly in the browser, download the Excel workbook, or clear records when starting a new term.

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the app:**
   ```bash
   streamlit run app.py
   ```
