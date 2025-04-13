import streamlit as st
from db import load_payments
import pandas as pd
from utils.emailer import send_email
from datetime import datetime

def dashboard():
    st.title("📊 Dashboard")

    payments = load_payments()
    df = pd.DataFrame(payments)

    if df.empty:
        st.info("No data yet.")
    else:
        df["submitted_at"] = pd.to_datetime(df["submitted_at"])
        df["week"] = df["submitted_at"].dt.strftime("%Y-W%U")
        df["month"] = df["submitted_at"].dt.strftime("%B")

        summary = df.groupby("contractor").agg({
            "amount": ["sum"],
            "week": lambda x: df.loc[x.index].groupby("week")["amount"].sum().max(),
            "month": lambda x: df.loc[x.index].groupby("month")["amount"].sum().max()
        })

        st.dataframe(summary)

        st.markdown("### Status Summary")
        st.write(f"🕒 Pending: {len(df[df['status'] == 'Pending'])}")
        st.write(f"✅ Approved: {len(df[df['status'] == 'Approve'])}")
        st.write(f"❌ Rejected/Returned: {len(df[df['status'].isin(['Reject', 'Return'])])}")

        st.markdown("---")
        st.subheader("🧾 Export Reports")

        # Excel Export
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name="Payments")
        excel_data = excel_buffer.getvalue()
        b64_excel = base64.b64encode(excel_data).decode()
        st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="payments.xlsx">📥 Download Excel Report</a>', unsafe_allow_html=True)

        # PDF Export
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, "Payment Summary Report", ln=True, align="C")

            def chapter_title(self, title):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, title, ln=True)

            def chapter_body(self, text):
                self.set_font("Arial", "", 10)
                self.multi_cell(0, 10, text)

        pdf = PDF()
        pdf.add_page()
        pdf.chapter_title("Submitted Payments")

        for i, row in df.iterrows():
            text = f"Contractor: {row['contractor']}\nAmount: ${row['amount']}\nStatus: {row['status']}\nDescription: {row['description']}\nWork Period: {row['work_period']}\nSubmitted By: {row['submitted_by']}\nDate: {row['submitted_at'].strftime('%Y-%m-%d')}\n"
            pdf.chapter_body(text + "\n---------------------\n")

        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_data = pdf_buffer.getvalue()
        b64_pdf = base64.b64encode(pdf_data).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="payments_report.pdf">📥 Download PDF Report</a>', unsafe_allow_html=True)

