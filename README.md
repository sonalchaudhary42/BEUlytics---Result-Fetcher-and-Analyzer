# BEUlytics : Result Fetcher & Analyzer 🎓📊

## A smart and automated result scraping & analysis tool for Bihar Engineering University (BEU), designed using Python and Streamlit.⚙️ Visualize. Analyze. Automate.

---

## 📌 Features

- 🖥️ Clean Streamlit UI with dropdown-based inputs (semester, branch, college, etc.)
- 🔐 Supports Lateral Entry registration patterns
- 📊 Analytics:
  - CGPA distribution histogram
  - Top 10 performers
  - Semester-wise comparison (coming soon)
- 💾 Exports result as PDF, Excel, CSV, or TXT
- ⚡ Fast result fetching using multi-threading
- 🏷️ College & branch code mapping built-in

---

## 📸 UI Preview

![Screenshot 2025-06-25 144740](https://github.com/user-attachments/assets/77f7ca65-71ba-4a0e-a942-6bd99b49798e)
![Screenshot 2025-06-25 144752](https://github.com/user-attachments/assets/8615547d-b93e-4935-8be8-d9d617dc667e)
![Screenshot 2025-06-25 144822](https://github.com/user-attachments/assets/4a51d13c-fff5-4ea9-b483-67dbc809038f)
![Screenshot 2025-06-25 144854](https://github.com/user-attachments/assets/13f2b2ea-bad5-42a8-9150-db74c018eeb4)
![Screenshot 2025-06-25 144909](https://github.com/user-attachments/assets/751bc95e-6957-444e-89d6-fb4a70307d97)
![Screenshot 2025-06-25 144921](https://github.com/user-attachments/assets/dfec98f3-043b-4537-85e9-1a2b0d45d428)
![Screenshot 2025-06-25 144932](https://github.com/user-attachments/assets/d489abf3-6bee-43b4-ad8d-9b9b921f1865)

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/aditya-kr86/BEUlytics---Result-Fetcher-and-Analyzer.git
cd BEUlytics---Result-Fetcher-and-Analyzer
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 📁 File Structure

```
.
├── app.py                  # Streamlit main app
├── scraper.py              # Core result fetching logic
├── export_utils.py         # PDF export utility
├── analytics.py            # Create Analytics Dashboard
├── requirements.txt        # Python dependencies
├── beu_logo.jpeg           # Logo used in UI
└── README.md
```

---

## 🧠 Behind the Scenes

* **Data Scraping**: BeautifulSoup to extract result data from BEU’s official site.
* **Analytics**: Pandas + Plotly for real-time charts.
* **PDF Export**: xhtml2pdf for landscape tables.

---

## 📃 License

This project is open-source under the MIT License.

---

> Made with ❤️ by [Aditya Kumar](https://adityakr.me)
