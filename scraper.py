import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def fetch_and_parse_result(base_url, registration_no, retries=3, backoff_factor=1):
    url = f"{base_url}{registration_no}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            result = {
                "Registration No.": soup.select_one(
                    "#ContentPlaceHolder1_DataList1_RegistrationNoLabel_0").text.strip(),
                "Student Name": soup.select_one("#ContentPlaceHolder1_DataList1_StudentNameLabel_0").text.strip(),
                "Father's Name": soup.select_one("#ContentPlaceHolder1_DataList1_FatherNameLabel_0").text.strip(),
                "Mother's Name": soup.select_one("#ContentPlaceHolder1_DataList1_MotherNameLabel_0").text.strip(),
                "Current SGPA": soup.select_one("#ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0").text.strip()
            }
            table = soup.select_one("#ContentPlaceHolder1_GridView3")
            if table:
                headers = [th.text.strip() for th in table.select("tr")[0].find_all("th")]
                values = [td.text.strip() for td in table.select("tr")[1].find_all("td")]
                for header, value in zip(headers, values):
                    result[f"Sem {header}"] = value
            return result
        except (requests.exceptions.RequestException, AttributeError) as e:
            print(f"Attempt {attempt + 1} failed for Registration No: {registration_no} - {e}")
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))
            else:
                print(f"Failed to fetch data for Registration No: {registration_no} after {retries} attempts.")
                return None


def fetch_all_results(base_url, start_reg, end_reg):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_and_parse_result, base_url, reg_no) for reg_no in
                   range(start_reg, end_reg + 1)]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    return results


def sort_by_current_cgpa(df):
    df["Sem Cur. CGPA"] = pd.to_numeric(df["Sem Cur. CGPA"], errors="coerce")
    return df.sort_values(by="Sem Cur. CGPA", ascending=False)


def sort_by_latest_semester_grade(df):
    sem_columns = [col for col in df.columns if col.startswith("Sem ")]

    def get_latest_grade(row):
        for col in reversed(sem_columns):
            try:
                val = float(row[col])
                return val
            except:
                continue
        return -1

    df["Latest Semester Grade"] = df.apply(get_latest_grade, axis=1)
    sorted_df = df.sort_values(by="Latest Semester Grade", ascending=False).drop(columns=["Latest Semester Grade"])
    return sorted_df




