import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from core_systems import inject_enterprise_css, run_query, render_live_ticker
from datetime import datetime

st.set_page_config(page_title="Master Database", layout="wide")
inject_enterprise_css()
render_live_ticker()

if not st.session_state.get('authenticated', False): st.stop()

st.markdown("<h2 style='text-align: center;'>🗄️ CENTRAL INTELLIGENCE REGISTRY</h2>", unsafe_allow_html=True)

with st.container(border=True):
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1: search_query = st.text_input("📡 SYSTEM-WIDE SEARCH", placeholder="Type any keyword (e.g. Visakhapatnam, UPI, Fraud)...")
    with col_s2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**STATUS:** 🟢 DATABASE ONLINE")

df = run_query("SELECT Tracking_ID, Timestamp, Jurisdiction, Crime_Category, Financial_Loss_Lakhs, Suspect_Info, Modus_Operandi, Status FROM intel_records ORDER BY Timestamp DESC")

if search_query:
    mask = df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
    df = df[mask]
    st.info(f"Search isolated {len(df)} matching records.")

st.dataframe(df, use_container_width=True, hide_index=True, height=400)

# ==================== AUTOMATED PDF DOSSIER GENERATOR ====================
st.markdown("<h3 style='color:#00E5FF; margin-top: 30px;'>📑 EXPORT OFFICIAL DOSSIER</h3>", unsafe_allow_html=True)
st.markdown("Generate a classified PDF report for legal routing or field agents.")

col_pdf1, col_pdf2 = st.columns([2, 1])
with col_pdf1:
    selected_id = st.selectbox("Select Tracking ID to Export:", df['Tracking_ID'].tolist())

with col_pdf2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GENERATE PDF DOSSIER", use_container_width=True):
        case_data = df[df['Tracking_ID'] == selected_id].iloc[0]
        
        # Build the PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="STATE CYBER INTELLIGENCE AGENCY", ln=True, align='C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 10, txt="OFFICIAL CASE DOSSIER - CONFIDENTIAL", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"TRACKING ID: {case_data['Tracking_ID']}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Timestamp: {case_data['Timestamp']}", ln=True)
        pdf.cell(200, 10, txt=f"Jurisdiction: {case_data['Jurisdiction']}", ln=True)
        pdf.cell(200, 10, txt=f"Classification: {case_data['Crime_Category']}", ln=True)
        pdf.cell(200, 10, txt=f"Financial Impact: Rs. {case_data['Financial_Loss_Lakhs']} Lakhs", ln=True)
        pdf.cell(200, 10, txt=f"Current Status: {case_data['Status']}", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="SUSPECT INTELLIGENCE:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt=case_data['Suspect_Info'])
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="MODUS OPERANDI (M.O.):", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt=case_data['Modus_Operandi'])
        
        # Output PDF to download
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label=f"⬇️ DOWNLOAD {selected_id}_DOSSIER.pdf",
            data=pdf_bytes,
            file_name=f"{selected_id}_Classified_Dossier.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
        st.success("PDF Generated Successfully. Ready for download.")
        # ==================== SYSTEM BACKUP EXPORT ====================
st.markdown("<hr style='border-color: #1F2937;'>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#94A3B8;'>💾 SYSTEM ADMINISTRATOR COMMANDS</h4>", unsafe_allow_html=True)

csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ DOWNLOAD ENTIRE MAINFRAME BACKUP (.CSV)",
    data=csv_data,
    file_name=f"Cyber_Command_Backup_{datetime.now().strftime('%Y-%m-%d')}.csv",
    mime="text/csv",
    type="secondary"
)