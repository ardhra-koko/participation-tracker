# Class Participation Tracker

**Live App:** [https://ardhra-koko-participation-tracker-app-oudkti.streamlit.app/](https://ardhra-koko-participation-tracker-app-oudkti.streamlit.app/)

A Python and Streamlit web app for tracking student class participation across multiple classes using clickable roll number buttons and automated Excel logging.

## Features
- **Multi-Class Management:** Upload one or multiple class Excel files (`ECOM_A.xlsx`, `ECOM_B.xlsx`, etc.) at once. Each file automatically creates its own dedicated class tab and separate Excel record workbook (`records_<ClassName>.xlsx`).
- **Persistent Daily Auto-Load:** Uploaded classes stay saved locally—no need to re-upload student lists every day.
- **One-Click Point Logging:** Click any student's roll number button to award `+1` mark and see live point totals directly on the grid.
- **Two-Sheet Excel Storage:** Automatically updates each class's Excel workbook with two tabs:
  - **Summary:** Running total marks and last updated timestamp per student.
  - **Click Log:** Detailed history of every click with exact date and time.
- **View, Download & Delete:** Inspect records in the browser, download any class's `.xlsx` file, or delete old class records individually.

## Input Excel Format
Your input `.xlsx` file should be named after the class (e.g., `ECOM_A.xlsx`) and contain two columns:
- `Roll No`
- `Name`

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the app:**
   ```bash
   streamlit run app.py
   ```

## Sample Template
You can use the included `sample_class.xlsx` file to test the app immediately or use it as a template for your own class lists.
