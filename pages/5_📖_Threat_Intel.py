import streamlit as st
import time
import random
from core_systems import inject_enterprise_css, render_live_ticker

st.set_page_config(page_title="Threat Intel", layout="wide")
inject_enterprise_css()
render_live_ticker()

if not st.session_state.get('authenticated', False): st.stop()

st.markdown("<h2>📖 OFFICIAL THREAT INTELLIGENCE</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#94A3B8; margin-bottom: 20px;'>Active vectors, hygiene protocols, and deep web reconnaissance.</p>", unsafe_allow_html=True)

# WE NOW HAVE 5 TABS! The new "MODULE GUIDE" is placed in the middle.
tab_threats, tab_safety, tab_guide, tab_darkweb, tab_kali = st.tabs(["⚠️ THREAT VECTORS", "🛡️ CYBER HYGIENE", "📚 MODULE GUIDE", "🌐 DARK WEB SCANNER", "💻 KALI TERMINAL"])

# --- TAB 1: THREATS ---
with tab_threats:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='background: rgba(15,23,42,0.6); border-left: 4px solid #EF4444; padding: 25px; border-radius: 8px; margin-bottom: 20px;'><h3 style='color: #F8FAFC; margin-top:0;'>📞 Digital Arrest / Virtual Extortion</h3><p style='color: #94A3B8;'><strong>[MODUS OPERANDI]:</strong> Fake CBI officers on Skype threaten arrest for fake parcels.</p><p style='color: #10B981;'><strong>[DEFENSE SOP]:</strong> Terminate call. Police do not use Skype.</p></div>", unsafe_allow_html=True)
        st.markdown("<div style='background: rgba(15,23,42,0.6); border-left: 4px solid #8B5CF6; padding: 25px; border-radius: 8px; margin-bottom: 20px;'><h3 style='color: #F8FAFC; margin-top:0;'>📱 Predatory Loan App Blackmail</h3><p style='color: #94A3B8;'><strong>[MODUS OPERANDI]:</strong> Unverified apps steal contacts and morph photos for blackmail.</p><p style='color: #10B981;'><strong>[DEFENSE SOP]:</strong> Never grant Gallery/Contact permissions to loan apps.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='background: rgba(15,23,42,0.6); border-left: 4px solid #00E5FF; padding: 25px; border-radius: 8px; margin-bottom: 20px;'><h3 style='color: #F8FAFC; margin-top:0;'>💳 Financial Fraud (Phishing)</h3><p style='color: #94A3B8;'><strong>[MODUS OPERANDI]:</strong> Fake SMS links claiming KYC expiry or power disconnection.</p><p style='color: #10B981;'><strong>[DEFENSE SOP]:</strong> Never click unsolicited SMS links.</p></div>", unsafe_allow_html=True)
        st.markdown("<div style='background: rgba(15,23,42,0.6); border-left: 4px solid #EC4899; padding: 25px; border-radius: 8px; margin-bottom: 20px;'><h3 style='color: #F8FAFC; margin-top:0;'>🔒 Ransomware Operations</h3><p style='color: #94A3B8;'><strong>[MODUS OPERANDI]:</strong> Malware encrypts databases and demands crypto payments.</p><p style='color: #10B981;'><strong>[DEFENSE SOP]:</strong> 3-2-1 backup rule. Never pay the ransom.</p></div>", unsafe_allow_html=True)

# --- TAB 2: HYGIENE ---
with tab_safety:
    st.markdown("<div style='background: rgba(15,23,42,0.6); border: 1px solid rgba(0, 229, 255, 0.4); padding: 40px; border-radius: 8px;'><h3 style='color: #00E5FF; text-align: center;'>🛡️ MASTER CYBER HYGIENE CHECKLIST</h3><p style='color:#94A3B8; text-align:center;'>1. Enable 2FA on all accounts. <br> 2. Lock Aadhaar Biometrics via UIDAI. <br> 3. Disable International Card Transactions. <br> 4. Use a Password Manager.</p></div>", unsafe_allow_html=True)

# ==================== TAB 3: THE NEW MODULE GUIDE ====================
with tab_guide:
    st.markdown("<h3 style='color:#00E5FF;'>📚 Tactical Module Architecture</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; margin-bottom: 30px;'>An executive overview of the advanced reconnaissance tools available in this command center.</p>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background: rgba(15,23,42,0.6); border-left: 4px solid #EF4444; padding: 25px; border-radius: 8px; margin-bottom: 20px; border: 1px solid rgba(239, 68, 68, 0.2);'>
        <h4 style='color: #EF4444; margin-top:0; font-family: "Orbitron", sans-serif;'>🌐 Deep/Dark Web Asset Monitor</h4>
        <p style='color: #F8FAFC; font-size: 1.05rem;'><strong>What is it?</strong> A simulated OSINT (Open-Source Intelligence) engine that queries known data broker leaks and underground hacker forums.</p>
        <p style='color: #94A3B8; line-height: 1.6;'><strong>SOC Application:</strong> When a citizen reports a cyber crime, investigators use this tool to check if the victim's email or phone number was part of a larger, global data breach (like the LinkedIn or Canva hacks). If credentials are found on the Dark Web, it explains exactly how the attackers bypassed security to gain initial access to the victim's accounts.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background: rgba(15,23,42,0.6); border-left: 4px solid #10B981; padding: 25px; border-radius: 8px; margin-bottom: 20px; border: 1px solid rgba(16, 185, 129, 0.2);'>
        <h4 style='color: #10B981; margin-top:0; font-family: "Orbitron", sans-serif;'>💻 Tactical Recon Terminal (Kali Linux & Nmap)</h4>
        <p style='color: #F8FAFC; font-size: 1.05rem;'><strong>What is it?</strong> A simulated command-line interface running <code>nmap</code>, the industry-standard network mapping tool used by both cybersecurity professionals and threat actors.</p>
        <p style='color: #94A3B8; line-height: 1.6;'><strong>SOC Application:</strong> When a suspect IP address or server is identified, investigators run an Nmap Port Scan. It probes the hostile server to see which "doors" (ports) are open. For example, finding Port 3389 open means the server allows Remote Desktop Protocol (RDP), which is a massive security vulnerability often exploited by Ransomware gangs to hijack systems.</p>
    </div>
    """, unsafe_allow_html=True)


# --- TAB 4: DARK WEB SCANNER ---
with tab_darkweb:
    st.markdown("<h3 style='color:#EF4444;'>🌐 Deep/Dark Web Asset Monitor</h3>", unsafe_allow_html=True)
    st.markdown("Scan global data broker leaks and underground forums for compromised credentials.")
    
    with st.container(border=True):
        email_query = st.text_input("Enter Target Email Address (e.g., target@gmail.com):")
        if st.button("INITIATE DEEP WEB SCAN", type="primary"):
            if email_query:
                with st.spinner("Bypassing Tor nodes... Querying known data breaches..."):
                    time.sleep(2)
                    breaches = [
                        ("LinkedIn Data Breach", "2012", "Email Addresses, Encrypted Passwords"), 
                        ("Canva Hack", "2019", "Usernames, Email Addresses, Names"), 
                        ("Dominos India", "2021", "Phone Numbers, GPS Locations, Payment Details"), 
                        ("Russian Botnet 'Citadel'", "2023", "Cleartext Passwords, IP Addresses")
                    ]
                    num_breaches = random.randint(0, 3)
                    
                    if num_breaches == 0:
                        st.success(f"✅ SECURE: No compromised data found for '{email_query}' in known breaches.")
                    else:
                        st.error(f"⚠️ CRITICAL ALERT: '{email_query}' found in {num_breaches} known data breaches!")
                        st.markdown("<h4 style='color:#EF4444; margin-top: 20px;'>🚨 COMPROMISED ASSETS DETECTED:</h4>", unsafe_allow_html=True)
                        for b_name, b_year, b_data in random.sample(breaches, num_breaches):
                            st.markdown(f"""
                            <div style='background: rgba(15,23,42,0.8); border: 1px solid #374151; border-left: 4px solid #EF4444; padding: 15px; border-radius: 4px; margin-bottom: 10px;'>
                                <span style='color: #F8FAFC; font-weight: bold; font-size: 1.1rem;'>{b_name} ({b_year})</span><br>
                                <span style='color: #94A3B8; font-size: 0.9rem;'><strong>Data Compromised:</strong> {b_data}</span><br>
                                <span style='color: #EF4444; font-size: 0.85rem; font-family: "Courier New", monospace;'>STATUS: AVAILABLE ON DARK FORUMS</span>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style='background: #000; padding: 15px; border: 1px solid #333; margin-top: 20px; border-radius: 4px;'>
                            <code style='color:#10B981; font-size: 0.9rem;'>[SYSTEM LOG] Extracted Fragment:<br>
                            > Hash: $2b$12$x8R{random.randint(1000,9999)}...<br>
                            > Last Known Login IP: {random.randint(10,255)}.{random.randint(10,255)}.{random.randint(10,255)}.12</code>
                        </div>
                        """, unsafe_allow_html=True)

# --- TAB 5: KALI TERMINAL ---
with tab_kali:
    st.markdown("<h3 style='color:#10B981;'>💻 Tactical Recon Terminal (Kali Linux)</h3>", unsafe_allow_html=True)
    
    if st.button("RUN NMAP PORT SCAN ON THREAT ACTOR"):
        terminal_box = st.empty() 
        base_html = "<div style='background-color: #000000; padding: 20px; border-radius: 8px; border: 1px solid #333; font-family: \"Courier New\", Courier, monospace; white-space: pre-wrap; height: 350px; overflow-y: hidden; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);'>"
        
        lines = [
            "<span style='color: #10B981;'>root@kali</span><span style='color: #F8FAFC;'>:~#</span> nmap -sV -p- 192.168.45.112\n\n",
            "<span style='color: #94A3B8;'>Starting Nmap 7.93 ( https://nmap.org ) at 2026-03-25 21:42 IST</span>\n",
            "<span style='color: #94A3B8;'>Scanning 192.168.45.112 [65535 ports]</span>\n",
            "<span style='color: #10B981;'>Discovered open port 22/tcp on 192.168.45.112</span>\n",
            "<span style='color: #10B981;'>Discovered open port 80/tcp on 192.168.45.112</span>\n",
            "<span style='color: #10B981;'>Discovered open port 3389/tcp on 192.168.45.112</span>\n\n",
            "<span style='color: #E2E8F0;'>PORT     STATE  SERVICE       VERSION</span>\n",
            "<span style='color: #10B981;'>22/tcp   open   ssh           OpenSSH 8.2p1</span>\n",
            "<span style='color: #10B981;'>80/tcp   open   http          Apache httpd 2.4.41</span>\n",
            "<span style='color: #EF4444;'>3389/tcp open   ms-wbt-server Vulnerable to BlueKeep</span>\n\n",
            "<span style='color: #94A3B8;'>Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds</span>\n",
            "<span style='color: #10B981;'>root@kali</span><span style='color: #F8FAFC;'>:~#</span> █"
        ]
        
        output = ""
        for line in lines:
            output += line
            terminal_box.markdown(base_html + output + "</div>", unsafe_allow_html=True)
            time.sleep(0.4) 
            
    else:
        st.markdown("<div style='background-color: #000000; padding: 20px; border-radius: 8px; border: 1px solid #333; font-family: \"Courier New\", Courier, monospace; height: 350px;'><span style='color: #10B981;'>root@kali</span><span style='color: #F8FAFC;'>:~#</span> █</div>", unsafe_allow_html=True)