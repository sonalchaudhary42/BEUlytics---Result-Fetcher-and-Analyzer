import streamlit as st
import pandas as pd
from scraper import fetch_all_results
from export_utils import export_to_pdf
from analytics import show_analytics
from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Branch and College mappings from tera data
branch_codes = {
    "101": "Civil Engineering (CE)",
    "102": "Mechanical Engineering (ME)",
    "105": "Computer Science Engineering (CSE)",
    "110": "Electrical and Electronics Engineering (EEE)"
}

college_codes = {
    "102": "Vidya Vihar Institute of Technology, Purnia",
    "103": "Netaji Subhash Institute of Technology, Patna",
    "106": "Sityog Institute of Technology, Aurangabad",
    "107": "Muzaffarpur Institute of Technology, Muzaffarpur",
    "108": "Bhagalpur College of Engineering, Bhagalpur",
    "109": "Nalanda College of Engineering, Nalanda",
    "110": "Gaya College of Engineering, Gaya",
    "111": "Darbhanga College of Engineering, Darbhanga",
    "113": "Motihari College Of Engineering, Mothihari",
    "115": "Azmet Institute of Technology, Kishanganj",
    "117": "Lok Nayak Jai Prakash Institute of Technology, Chhapra",
    "118": "Buddha Institute of Technology, Gaya",
    "119": "Adwaita Mission Institute of Technology, Banka",
    "121": "Moti Babu Institute of Technology, Forbesganj",
    "122": "Exalt College of Engineering & Technology, Vaishali",
    "123": "Siwan Engineering & Technical Institute, Siwan",
    "124": "Sershah Engineering College, Sasaram, Rohtas",
    "125": "Rashtrakavi Ramdhari Singh Dinkar College of Engineering, Begusarai",
    "126": "Bakhtiyarpur College of Engineering, Patna",
    "127": "Sitamarhi Institute of Technology, Sitamarhi",
    "128": "B.P. Mandal College of Engineering, Madhepura",
    "129": "Katihar Engineering of College, Katihar",
    "130": "Supaul College of Engineering, Supaul",
    "131": "Purnea College of Engineering, Purnea",
    "132": "Saharsa College of Engineering, Saharsa",
    "133": "Government Engineering College, Jamui",
    "134": "Government Engineering College, Banka",
    "135": "Government Engineering College, Vaishali",
    "136": "Mother's Institute of Technology, Bihta, Patna",
    "139": "R.P. Sharma Institute of Technology, Patna",
    "140": "Maulana Azad College of Engineering & Technology, Patna",
    "141": "Government Engineering College, Nawada",
    "142": "Government Engineering College, Kishanganj",
    "144": "Government Engineering College, Munger",
    "145": "Government Engineering College, Sheohar",
    "146": "Government Engineering College, West Champaran",
    "147": "Government Engineering College, Aurangabad",
    "148": "Government Engineering College, Kaimur",
    "149": "Government Engineering College, Gopalganj",
    "150": "Government Engineering College, Madhubani",
    "151": "Government Engineering College, Siwan",
    "152": "Government Engineering College, Jehanabad",
    "153": "Government Engineering College, Arwal",
    "154": "Government Engineering College, Khagaria",
    "155": "Government Engineering College, Buxar",
    "156": "Government Engineering College, Bhojpur",
    "157": "Government Engineering College, Sheikhpura",
    "158": "Government Engineering College, Lakhisarai",
    "159": "Government Engineering College, Samastipur",
    "165": "Shri Phanishwar Nath Renu Engineering College, Araria"
}

# Semester mappings
sem_words = {
    1: "1st", 2: "2nd", 3: "3rd", 4: "4th",
    5: "5th", 6: "6th", 7: "7th", 8: "8th"
}

sem_romans = {
    1: "I", 2: "II", 3: "III", 4: "IV",
    5: "V", 6: "VI", 7: "VII", 8: "VIII"
}

lateral = {
    "No": False,
    "Yes": True
}

col1, col2 = st.columns([2, 5])

with col1:
    logo = Image.open("beu_logo.jpeg")
    st.image(logo, width=180)

with col2:
    # st.markdown(
    #     "<h1 style='padding-top: 20px;'>BEU Result Fetcher & Analyzer</h1>", 
    #     unsafe_allow_html=True
    # )
    st.markdown(
    "<div style='font-size: 48px; font-weight: bold; padding-top: 20px;'>BEU Result Fetcher & Analyzer</div>",
    unsafe_allow_html=True
    )
    st.markdown(
        """<p style='color: grey; font-size: 16px; margin-top: -10px;'>
        Visualize. Analyze. Automate. — A Data Project by 
        <a href='https://adityakr.me' target='_blank' style='text-decoration: none;'>
            <span style='font-size: 16px;'><b>Aditya Kumar</b> </span>
        </a></p>""",
        unsafe_allow_html=True
    )



with st.form("result_form"):
    semester = st.selectbox("Semester", options=list(range(1, 9)), format_func=lambda x: f"{x} ({sem_words[x]})")
    batch = st.number_input("Batch Year (Last two digits, e.g. 23 for 2023-27)", min_value=20, max_value=30, value=23)
    year = st.number_input("Exam Year (e.g. 2024)", min_value=2020, max_value=2030, value=2024)
    branch = st.selectbox("Branch", options=list(branch_codes.keys()), format_func=lambda x: branch_codes[x])
    college = st.selectbox("College", options=list(college_codes.keys()), format_func=lambda x: college_codes[x])
    start_reg = st.number_input("Start Registration No. (Short Reg No.)", min_value=1, max_value=999, value=1)
    end_reg = st.number_input("End Registration No. (Short Reg No.)", min_value=1, max_value=999, value=10)
    is_lateral = st.selectbox("Is this for Lateral Entry Students?", options=list(lateral.keys()))
    view_mode = st.selectbox("View Mode", options=["regno", "cgpa", "semester"], format_func=lambda x: {
        "regno": "Registration No. wise",
        "cgpa": "Sort by CGPA (High to Low)",
        "semester": "Sort by Latest Semester Grade"
    }[x])
    export_format = st.selectbox("Export Format", options=["csv", "xlsx", "txt", "pdf"], format_func=lambda x: x.upper())
    submitted = st.form_submit_button("Fetch Results")

if submitted:
    reg_batch = batch
    if start_reg > end_reg:
        st.error("Start Registration No. cannot be greater than End Registration No.")
        st.stop()

    if lateral[is_lateral]:
        if semester < 3:
            st.error("Lateral Entry students' results are available only from Semester 3 onwards.")
            st.stop()
        reg_batch += 1
        start_reg += 900
        end_reg += 900

    results = []
    st.info("Fetching results... This might take some time depending on the range.")

    start_full_reg_no = f"{reg_batch}{branch}{college}{start_reg:03d}"
    end_full_reg_no = f"{reg_batch}{branch}{college}{end_reg:03d}"
    url = f"https://results.beup.ac.in/ResultsBTech{sem_words[semester]}Sem{year}_B20{batch}Pub.aspx?Sem={sem_romans[semester]}&RegNo="
    results = fetch_all_results(url, int(start_full_reg_no), int(end_full_reg_no))

    if not results:
        st.warning("No results fetched. Please check inputs.")
        st.stop()

    df = pd.DataFrame(results)

    # Sort data if required
    if view_mode == "cgpa":
        df["Sem Cur. CGPA"] = pd.to_numeric(df["Sem Cur. CGPA"], errors='coerce')
        df = df.sort_values(by="Sem Cur. CGPA", ascending=False)
    elif view_mode == "semester":
        sem_cols = [c for c in df.columns if c.startswith("Sem ")]
        def latest_sem_grade(row):
            for col in reversed(sem_cols):
                try:
                    val = float(row[col])
                    return val
                except:
                    continue
            return -1
        df["Latest Semester Grade"] = df.apply(latest_sem_grade, axis=1)
        df = df.sort_values(by="Latest Semester Grade", ascending=False).drop(columns=["Latest Semester Grade"])

    st.success("Results fetched successfully!")
    st.dataframe(df)
    show_analytics(df)


    # Export options
    if export_format in ["csv", "xlsx", "txt"]:
        export_path = f"results.{export_format}"
        if export_format == "csv":
            df.to_csv(export_path, index=False)
        elif export_format == "xlsx":
            df.to_excel(export_path, index=False, engine="openpyxl")
        elif export_format == "txt":
            df.to_csv(export_path, sep="\t", index=False)
        with open(export_path, "rb") as f:
            st.download_button(label=f"Download {export_format.upper()}", data=f, file_name=export_path)
            st.markdown("---")
            st.markdown(
                "<div style='text-align: center; color: grey;'>"
                "Made with ❤️ by <b>Aditya Kumar</b><br>"
                "Department of Computer Science & Engineering<br>"
                "Gaya College of Engineering (GCE), under BEU Patna"
                "</div>",
                unsafe_allow_html=True
            )
        os.remove(export_path)
    elif export_format == "pdf":
        export_path = "results.pdf"
        export_to_pdf(df, export_path)
        with open(export_path, "rb") as f:
            st.download_button(label="Download PDF", data=f, file_name=export_path)
        os.remove(export_path)
