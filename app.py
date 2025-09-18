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
    "103": "Electrical Engineering(EE)",
    "105": "Computer Science Engineering (CSE)",
    "110": "Electrical and Electronics Engineering (EEE)"
}

college_codes = {
    "110": "Gaya College of Engineering, Gaya",
    "108": "Bhagalpur College of Engineering, Bhagalpur",
    "107": "Muzaffarpur Institute of Technology, Muzaffarpur",
    "109": "Nalanda College of Engineering, Nalanda",
    "111": "Darbhanga College of Engineering, Darbhanga",
    "113": "Motihari College Of Engineering, Mothihari",
    "117": "Lok Nayak Jai Prakash Institute of Technology, Chhapra",
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
    "165": "Shri Phanishwar Nath Renu Engineering College, Araria",
    "102": "Vidya Vihar Institute of Technology, Purnia",
    "103": "Netaji Subhash Institute of Technology, Patna",
    "106": "Sityog Institute of Technology, Aurangabad",
    "115": "Azmet Institute of Technology, Kishanganj",
    "118": "Buddha Institute of Technology, Gaya",
    "119": "Adwaita Mission Institute of Technology, Banka",
    "121": "Moti Babu Institute of Technology, Forbesganj",
    "122": "Exalt College of Engineering & Technology, Vaishali",
    "123": "Siwan Engineering & Technical Institute, Siwan",
    "136": "Mother's Institute of Technology, Bihta, Patna",
    "139": "R.P. Sharma Institute of Technology, Patna",
    "140": "Maulana Azad College of Engineering & Technology, Patna"
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
    # year = st.number_input("Exam Year (e.g. 2024)", min_value=2020, max_value=2030, value=2024)
    branch = st.selectbox("Branch", options=list(branch_codes.keys()), format_func=lambda x: branch_codes[x])
    college = st.selectbox("College", options=list(college_codes.keys()), format_func=lambda x: college_codes[x])
    start_reg = st.number_input("Start Registration No. (Short Reg No.)", min_value=1, max_value=999, value=1)
    end_reg = st.number_input("End Registration No. (Short Reg No.)", min_value=1, max_value=999, value=10)
    is_lateral = st.selectbox("Are You Want to Combine LE Student Results also?", options=list(lateral.keys()))
    view_mode = st.selectbox("View Mode", options=["regno", "cgpa", "semester"], format_func=lambda x: {
        "regno": "Registration No. wise",
        "cgpa": "Sort by CGPA (High to Low)",
        "semester": "Sort by Latest Semester Grade"
    }[x])
    export_format = st.selectbox("Export Format", options=["pdf", "txt", "csv", "xlsx"], format_func=lambda x: x.upper())
    submitted = st.form_submit_button("Fetch Results")

if submitted:
    reg_batch = batch
    if start_reg > end_reg:
        st.error("Start Registration No. cannot be greater than End Registration No.")
        st.stop()


    st.info("Fetching results... This might take some time depending on the range.")
    year = int(2000 + batch + (0.5 * semester))

    start_full_reg_no = f"{reg_batch}{branch}{college}{start_reg:03d}"
    end_full_reg_no = f"{reg_batch}{branch}{college}{end_reg:03d}"

    # ---- START: NEW OPTIMIZED LOGIC ----

    # Define the two possible URL formats
    url_primary = f"https://results.beup.ac.in/ResultsBTech{sem_words[semester]}Sem{year}_B20{batch}Pub.aspx?Sem={sem_romans[semester]}&RegNo="
    url_secondary = f"https://results.beup.ac.in/ResultsBTech{sem_words[semester]}Sem{year}Pub.aspx?Sem={sem_romans[semester]}&RegNo="

    # Define a small test range (up to 5 students)
    test_end_no = min(int(start_full_reg_no) + 4, int(end_full_reg_no))

    # 1. Test the primary URL with the small range first
    # st.info(f"Testing primary URL with registration numbers {start_full_reg_no} to {test_end_no}...")
    test_results = fetch_all_results(url_primary, int(start_full_reg_no), test_end_no)

    # 2. Based on the test, decide which URL to use for the full scrape
    if test_results:
        # st.success("Primary URL test successful! Fetching all results with this format.")
        # If the test passes, use the primary URL for the full range.
        results = fetch_all_results(url_primary, int(start_full_reg_no), int(end_full_reg_no))
        if semester > 2 and lateral[is_lateral]:
            le_start_full_reg_no = f"{reg_batch+1}{branch}{college}901"
            le_end_full_reg_no = f"{reg_batch+1}{branch}{college}930"
            le_results = fetch_all_results(url_primary, int(le_start_full_reg_no), int(le_end_full_reg_no))
    else:
        # st.warning("Primary URL test failed. Switching to secondary URL for all results.")
        # If the test fails, use the secondary URL for the full range directly.
        results = fetch_all_results(url_secondary, int(start_full_reg_no), int(end_full_reg_no))
        if semester > 2:
            le_start_full_reg_no = f"{reg_batch+1}{branch}{college}901"
            le_end_full_reg_no = f"{reg_batch+1}{branch}{college}930"
            le_results = fetch_all_results(url_secondary, int(le_start_full_reg_no), int(le_end_full_reg_no))
        
    # ---- END: NEW OPTIMIZED LOGIC ----


    if not results:
        st.error("Data Not Found. Both primary and secondary URL formats failed to fetch results. Please verify your inputs and the current URL structure on the university website.")
        st.stop()

    df = pd.DataFrame(results)
    if semester > 2:
        le_df = pd.DataFrame(le_results)
        df = pd.concat([df, le_df], ignore_index=True)

    # Sort data if required
    if view_mode == "cgpa":
        df["Sem Cur. CGPA"] = pd.to_numeric(df["Sem Cur. CGPA"], errors='coerce')
        df = df.sort_values(by="Sem Cur. CGPA", ascending=False)
    elif view_mode == "semester":
        df["Current SGPA"] = pd.to_numeric(df["Current SGPA"], errors="coerce")
        df = df.sort_values(by="Current SGPA", ascending=False)

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


