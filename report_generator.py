import pandas as pd
from fpdf import FPDF

# Step 1: Load data from CSV
df = pd.read_csv("data.csv")

# Step 2: Analyze the data
summary = df.groupby("Department")["Score"].agg(["mean", "max", "min", "count"]).reset_index()
summary.columns = ["Department", "Average Score", "Max Score", "Min Score", "Count"]

# Step 3: Create a PDF class
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Automated Department-wise Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_table(self, df):
        self.set_font("Arial", "B", 12)
        col_width = 40
        row_height = 10

        # Table header
        for column in df.columns:
            self.cell(col_width, row_height, str(column), border=1)
        self.ln()

        # Table rows
        self.set_font("Arial", "", 12)
        for _, row in df.iterrows():
            for item in row:
                # Safely handle string and numeric data
                if isinstance(item, (int, float)):
                    text = str(round(item, 2))
                else:
                    text = str(item)
                self.cell(col_width, row_height, text, border=1)
            self.ln()

# Step 4: Create and save the PDF
pdf = PDFReport()
pdf.add_page()
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, "This PDF report contains department-wise score analysis including average, max, and min scores.")
pdf.ln(5)
pdf.add_table(summary)
pdf.output("report.pdf")

print("✅ Report has been generated as 'report.pdf'")
