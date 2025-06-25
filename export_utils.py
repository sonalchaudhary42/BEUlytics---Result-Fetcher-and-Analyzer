from xhtml2pdf import pisa
import pandas as pd

HTML_TEMPLATE = """
<html>
<head>
<style>
    @page {{
        size: A4 landscape;
    }}
    body {{
        font-family: Arial, sans-serif;
        font-size: 12px;
        margin: 20px;
    }}
    h2 {{
        text-align: center;
        margin-bottom: 20px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        word-wrap: break-word;
    }}
    th, td {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 6px;
        font-size: 10px;
    }}
    th {{
        background-color: #f2f2f2;
    }}
</style>
</head>
<body>
    <h2>Student Result Report</h2>
    <table>
        <thead>
            <tr>
                {header_cells}
            </tr>
        </thead>
        <tbody>
            {row_cells}
        </tbody>
    </table>
</body>
</html>
"""

def export_to_pdf(df, output_file):
    df = df.copy()
    df.insert(0, "Sl. No.", range(1, len(df) + 1))

    header_cells = ""
    for col in df.columns:
        if "SGPA" in col or "Semester" in col:
            header_cells += f'<th style="width:6%">{col}</th>'
        elif col == "Sl. No.":
            header_cells += f'<th style="width:5%; text-align:center;">{col}</th>'
        else:
            header_cells += f"<th>{col}</th>"

    row_cells = ""
    for _, row in df.iterrows():
        row_html = ""
        for col in df.columns:
            value = row[col]
            if "SGPA" in col or "Semester" in col:
                row_html += f'<td style="width:6%">{value}</td>'
            elif col == "Sl. No.":
                row_html += f'<td style="width:5%; text-align:center;">{value}</td>'
            else:
                row_html += f"<td>{value}</td>"
        row_cells += f"<tr>{row_html}</tr>"

    html = HTML_TEMPLATE.format(header_cells=header_cells, row_cells=row_cells)

    with open(output_file, "w+b") as result_file:
        pisa.CreatePDF(html, dest=result_file)
