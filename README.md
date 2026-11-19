# Class Participation Tracker

**Live App:** [https://streamlit.app](https://streamlit.app)

A Python and Streamlit web app for tracking student class participation across multiple classes using clickable roll number buttons, flexible fractional grading, and automated Excel logging.

## Features
- **Multi-Class Management:** Upload one or multiple class Excel files (`ECOM_A.xlsx`, `ECOM_B.xlsx`, etc.) at once. Each file automatically creates its own dedicated class tab and separate Excel record workbook (`records_<ClassName>.xlsx`).
- **Flexible Mark Values:** Choose between **0.25**, **0.5**, **0.75**, or **1.0** marks per click to award partial or full participation points.
- **Class Date Selector & Fresh Daily Grid:** Pick any class date—the button grid resets cleanly to `0 pts` for each new day while cumulative semester totals keep accumulating in Excel.
- **Instant One-Click Undo:** Clicked the wrong roll number? Use the **Undo** button above the grid to immediately remove the entry and recalculate totals in the Excel file.
- **Two-Sheet Excel Storage:** Automatically updates each class's Excel workbook with two tabs:
  - **Summary:** Cumulative total marks across all dates and last updated timestamp per student.
  - **Click Log:** Detailed history of every click with exact date, time, and marks awarded.
- **View, Download & Delete:** Inspect records directly in the browser, download any class's `.xlsx` file, or delete old class records individually.

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
