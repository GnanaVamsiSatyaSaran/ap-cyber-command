import streamlit as st
import time
from core_systems import inject_enterprise_css, init_db, render_live_ticker

st.set_page_config(page_title="Cyber Intelligence Center", page_icon="🛡️", layout="wide")
inject_enterprise_css()
init_db()
render_live_ticker()

if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style='background: rgba(15,23,42,0.8); padding: 40px; border-radius: 12px; border: 1px solid rgba(0,229,255,0.3); text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8); backdrop-filter: blur(15px);'>
            <img src="https://cdn-icons-png.flaticon.com/512/2093/2093153.png" width="70" style="margin-bottom: 15px; filter: drop-shadow(0 0 10px #00E5FF);">
            <h4 style='color: #94A3B8; margin: 0; font-size: 0.85rem; letter-spacing: 3px;'>CENTRAL INTELLIGENCE AGENCY</h4>
            <h2 style='color: #00E5FF; margin: 5px 0 30px 0; font-family: "Orbitron", sans-serif; text-shadow: 0 0 15px rgba(0,229,255,0.5);'>SECURE GATEWAY</h2>
        """, unsafe_allow_html=True)
        
        with st.form("login"):
            user = st.text_input("Personnel ID", placeholder="admin")
            pwd = st.text_input("Clearance Code", type="password", placeholder="admin")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("INITIATE SECURE UPLINK", use_container_width=True):
                if user == 'admin' and pwd == 'admin':
                    st.success("Clearance Accepted. Decrypting Mainframe...")
                    time.sleep(1)
                    st.session_state['authenticated'] = True
                    st.rerun()
                else: 
                    st.error("Access Denied. Intrusion Logged.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1F2937; padding-bottom: 10px; margin-bottom: 20px;">
        <h1 style='color:#F8FAFC; margin:0;'>🛡️ Command Center Active</h1>
        <span style="color: #10B981; font-family: 'Courier New', monospace; box-shadow: 0 0 10px rgba(16,185,129,0.4); padding: 5px 10px; border-radius: 4px; border: 1px solid #10B981;">[SYSTEM: SECURE]</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Authentication complete. Select a tactical module from the left navigation panel.")
    if st.button("TERMINATE SECURE SESSION", type="primary"):
        st.session_state['authenticated'] = False
        st.rerun()