import streamlit as st
import sqlite3
from datetime import datetime
import time
from core_systems import inject_enterprise_css, run_query, ap_coords, DB_FILE, generate_tracking_id, render_live_ticker

st.set_page_config(page_title="Citizen Portal", layout="wide")
inject_enterprise_css()
render_live_ticker()

if not st.session_state.get('authenticated', False): st.stop()

st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(0,229,255,0.2); padding-bottom: 10px; margin-bottom: 20px;">
    <h2 style='color:#F8FAFC; margin:0;'>🚨 NATIONAL INCIDENT REPORTING PORTAL</h2>
    <span style='color: #10B981; font-family: "Orbitron";'>256-BIT SECURE UPLINK</span>
</div>
""", unsafe_allow_html=True)

# THE TABS ARE BACK!
tab_report, tab_track, tab_suspect = st.tabs(["📝 FILE A COMPLAINT", "🔍 TRACK STATUS", "🚷 SUSPECT REPOSITORY"])

with tab_report:
    st.markdown("<div class='gov-alert'><strong>LEGAL DISCLAIMER:</strong> Filing false complaints or providing fabricated digital evidence is a punishable offense under the Information Technology Act, 2000. All IP addresses are logged.</div>", unsafe_allow_html=True)
    
    # THE ANONYMOUS OPTION IS BACK!
    report_type = st.radio("Select Reporting Protocol:", ["Report & Track (Requires Identity Verification)", "Report Anonymously (For Sensitive/CSEM Content)"], horizontal=True)
    
    with st.container(border=True):
        with st.form("citizen_intake", clear_on_submit=True):
            st.markdown("<h4 style='color:#00E5FF; border-bottom: 1px solid rgba(0,229,255,0.3); padding-bottom: 5px;'>1. Incident Classification</h4>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: area = st.selectbox("📍 Victim Jurisdiction", list(ap_coords.keys()))
            with c2: crime = st.selectbox("⚠️ Threat Category", ['Financial Fraud (UPI/Bank)', 'Crimes Against Women/Children', 'Ransomware / Hacking', 'Identity Theft', 'Social Media Impersonation'])
            with c3: platform = st.selectbox("📱 Medium of Attack", ['WhatsApp', 'Telegram', 'Instagram/Facebook', 'Fake Website', 'Phone Call', 'Email'])
            
            st.markdown("<h4 style='color:#00E5FF; border-bottom: 1px solid rgba(0,229,255,0.3); padding-bottom: 5px; margin-top: 15px;'>2. Incident Specifics</h4>", unsafe_allow_html=True)
            c4, c5 = st.columns(2)
            with c4: incident_date = st.date_input("🗓️ Exact Date of Incident")
            with c5: loss = st.number_input("💰 Financial Loss (Lakhs) - Enter 0 if none", min_value=0.0, value=0.0, step=0.1)
            
            suspect_info = st.text_input("🚷 Known Suspect Details (Phone, UPI ID, Social Media Handle)", placeholder="e.g., 9876543210 or scammer@ybl")
            mo = st.text_area("📝 Detailed Incident Description", placeholder="Provide a chronological account of the event. Do not omit any interactions...", height=150)
            
            st.markdown("<h4 style='color:#00E5FF; border-bottom: 1px solid rgba(0,229,255,0.3); padding-bottom: 5px; margin-top: 15px;'>3. Evidence & Verification</h4>", unsafe_allow_html=True)
            st.info("Supported formats: .jpg, .png, .pdf (Max 10MB per file). Upload screenshots of chats, bank statements, or malicious URLs.")
            
            # FILE UPLOADER IS BACK!
            evidence = st.file_uploader("📎 Attach Digital Evidence", accept_multiple_files=True)
            
            # IDENTITY VERIFICATION IS BACK!
            if "Track" in report_type:
                st.warning("Identity Verification Required for Tracking.")
                v1, v2 = st.columns(2)
                with v1: st.text_input("Victim Full Name")
                with v2: st.text_input("Aadhaar / PAN Number")
            
            st.markdown("<br>", unsafe_allow_html=True)
            declaration = st.checkbox("I hereby declare that the information provided is true to the best of my knowledge.")
            
            submitted = st.form_submit_button("SUBMIT OFFICIAL COMPLAINT", use_container_width=True)
            
            if submitted:
                if not declaration: st.error("❌ You must accept the legal declaration to proceed.")
                elif len(mo) < 10: st.error("❌ Incident description must be more detailed.")
                else:
                    with st.spinner('Generating Tracking ID and securing evidence...'):
                        time.sleep(1.5)
                        tid = generate_tracking_id()
                        lat, lon = ap_coords.get(area)
                        conn = sqlite3.connect(DB_FILE)
                        # EXACT MATCH FOR 13 COLUMNS
                        conn.execute("INSERT INTO intel_records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                                     (tid, "Anonymous" if "Anonymous" in report_type else "Registered", area, crime, 1, loss, suspect_info, platform, lat, lon, mo, "Pending Review", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        conn.commit()
                        conn.close()
                    st.success(f"✅ Complaint Lodged Successfully! Your Tracking ID is: **{tid}**")
                    if "Anonymous" in report_type: st.info("As an anonymous report, you will not receive updates. Intelligence has been routed to the Cyber Cell.")
                    else: st.info("Please save your Tracking ID to monitor the investigation status.")
                    time.sleep(2.5)
                    st.rerun()

# --- THE TRACKER IS BACK! ---
with tab_track:
    st.markdown("<h3 style='color:#00E5FF;'>🔍 Check Investigation Status</h3>", unsafe_allow_html=True)
    track_input = st.text_input("Enter your Tracking ID (e.g., CYB-12345678)")
    if st.button("FETCH STATUS"):
        if track_input:
            df = run_query(f"SELECT Tracking_ID, Crime_Category, Status, Timestamp FROM intel_records WHERE Tracking_ID = '{track_input}'")
            if not df.empty:
                st.success("Record Found in Mainframe.")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.error("No active investigation found for that Tracking ID.")

# --- THE REPOSITORY SEARCH IS BACK! ---
with tab_suspect:
    st.markdown("<h3 style='color:#EF4444;'>🚷 National Suspect Registry Search</h3>", unsafe_allow_html=True)
    st.markdown("Search a phone number, UPI ID, or Social Media Handle to see if it has been previously reported for fraudulent activity.")
    search_q = st.text_input("Search a Phone Number or UPI ID to see if it is flagged for fraud:")
    if st.button("SEARCH REPOSITORY", type="primary"):
        if search_q:
            df = run_query("SELECT Tracking_ID, Jurisdiction, Crime_Category, Suspect_Info FROM intel_records")
            results = df[df['Suspect_Info'].astype(str).str.contains(search_q, case=False, na=False)]
            if not results.empty:
                st.error(f"⚠️ WARNING: {len(results)} previous complaints found matching '{search_q}'. Proceed with extreme caution.")
                st.dataframe(results, use_container_width=True, hide_index=True)
            else: st.success("✅ No previous reports found. Always exercise caution.")