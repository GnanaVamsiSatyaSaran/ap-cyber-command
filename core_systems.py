import streamlit as st
import pandas as pd
import sqlite3
import random
from datetime import datetime

# Changed database name for a fresh start
DB_FILE = 'cyber_command_core.db'

ap_coords = {
    'Visakhapatnam': (17.6868, 83.2185), 'Vijayawada': (16.5062, 80.6480), 'Guntur': (16.3067, 80.4365), 
    'Tirupati': (13.6288, 79.4192), 'Kurnool': (15.8281, 78.8353), 'Nellore': (14.4426, 79.9864), 
    'Kakinada': (16.9891, 82.2475), 'Rajahmundry': (17.0005, 81.8040), 'Anantapur': (14.6819, 77.6006), 
    'Kadapa': (14.4673, 78.8242)
}

def inject_enterprise_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&display=swap');
        
        .block-container { padding: 1.5rem 3rem !important; max-width: 100% !important; }
        
        @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
        .stApp { 
            background: linear-gradient(-45deg, #020617, #050A15, #0F172A, #020617); background-size: 400% 400%;
            animation: gradientBG 15s ease infinite; font-family: 'Inter', sans-serif; color: #E2E8F0;
        }
        .stApp::before {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
            background-size: 40px 40px; pointer-events: none; z-index: -1;
        }
        
        h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; color: #00E5FF; text-shadow: 0 0 15px rgba(0,229,255,0.4); }
        [data-testid="stHeader"], footer { display: none !important; }
        
        .ticker-wrap { width: 100%; overflow: hidden; background-color: rgba(2, 6, 23, 0.9); border-bottom: 1px solid #00E5FF; padding: 8px 0; box-shadow: 0 4px 15px rgba(0, 229, 255, 0.2); margin-bottom: 20px; }
        .ticker { display: inline-block; white-space: nowrap; padding-right: 100%; animation: ticker 30s linear infinite; }
        .ticker-item { display: inline-block; padding: 0 2rem; font-family: 'Orbitron', monospace; font-size: 0.9rem; color: #10B981; }
        .ticker-alert { color: #EF4444; font-weight: bold; text-shadow: 0 0 10px rgba(239, 68, 68, 0.6); }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        
        [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 8px; border: 1px solid rgba(0,229,255,0.2) !important; background: rgba(10,15,28,0.7) !important; backdrop-filter: blur(10px); box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .stTextInput>div>div, .stSelectbox>div>div, .stNumberInput>div>div, .stTextArea>div>div, .stDateInput>div>div { background-color: rgba(2,6,23,0.8) !important; border: 1px solid #00E5FF !important; color: #00E5FF !important; border-radius: 6px; }
        
        .kpi-card { background: linear-gradient(145deg, rgba(15,23,42,0.8), rgba(2,6,23,0.9)); border: 1px solid rgba(0, 229, 255, 0.2); border-left: 4px solid #00E5FF; border-radius: 8px; padding: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: all 0.3s; }
        .kpi-card:hover { transform: translateY(-5px); border-left: 4px solid #E11D48; box-shadow: 0 0 25px rgba(225, 29, 72, 0.4); }
        .kpi-title { color: #94A3B8; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; font-weight: 600;}
        .kpi-val { color: #F8FAFC; font-size: 2.8rem; font-weight: 700; margin: 0; text-shadow: 0 0 20px rgba(0,229,255,0.5);}
        
        [data-testid="stSidebar"] { background-color: rgba(10,15,28,0.95) !important; border-right: 1px solid rgba(0,229,255,0.2); backdrop-filter: blur(20px);}
        .gov-alert { background: rgba(225,29,72,0.1); border-left: 4px solid #E11D48; padding: 15px; border-radius: 4px; margin-bottom: 20px; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

def render_live_ticker():
    facts = [
        "<span class='ticker-alert'>[CRITICAL]</span> Ransomware attacks globally occur every 11 seconds.",
        "Dial 1930 immediately for Financial Fraud reporting.",
        "<span class='ticker-alert'>[WARNING]</span> 95% of cybersecurity breaches are caused by human error.",
        "Always check the 'Suspect Repository' before transferring funds.",
        "State Cyber Command intercepted 12,000+ threat vectors this month."
    ]
    ticker_content = " ••• ".join([f"<div class='ticker-item'>{fact}</div>" for fact in facts])
    st.markdown(f"<div class='ticker-wrap'><div class='ticker'>{ticker_content}</div></div>", unsafe_allow_html=True)

def generate_tracking_id():
    return f"CYB-{random.randint(10000000, 99999999)}"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS intel_records (
        Tracking_ID TEXT PRIMARY KEY, Report_Type TEXT, Jurisdiction TEXT, Crime_Category TEXT, 
        Incident_Count INTEGER, Financial_Loss_Lakhs REAL, Suspect_Info TEXT, Platform TEXT, 
        Lat REAL, Lon REAL, Modus_Operandi TEXT, Status TEXT, Timestamp TEXT)''')
    
    if c.execute("SELECT count(*) FROM intel_records").fetchone()[0] == 0:
        data = []
        crimes = ['Financial Fraud (UPI/Bank)', 'Crimes Against Women/Children', 'Ransomware / Hacking', 'Identity Theft', 'Social Media Impersonation']
        platforms = ['WhatsApp', 'Telegram', 'Instagram/Facebook', 'Fake Website', 'Phone Call', 'Email']
        suspects = ["UPI: rahul.sharma@ybl", "Ph: +91-9876543210", "UPI: crypto.desk@okicici", "Telegram ID: @InvestPro_Admin", "Website: secure-bank-update.com"]
        mos = ["Victim received SMS claiming electricity disconnection. Clicked link, downloaded AnyDesk. OTP stolen.", "Fake Skype call from 'Customs Officer'. Threatened with digital arrest. Extorted funds.", "Hospital network breached via phishing email. Ransomware deployed.", "Victim added to Telegram trading group. Promised 200% returns.", "Downloaded instant loan app. App stole contacts. Blackmailed with photos."]
        
        for city, (lat, lon) in ap_coords.items():
            for _ in range(random.randint(5, 12)):
                data.append((
                    generate_tracking_id(), "Registered", city, random.choice(crimes), random.randint(1, 5), random.uniform(0.5, 25.0), 
                    random.choice(suspects), random.choice(platforms), lat, lon, random.choice(mos), 
                    random.choice(["Pending Review", "Active Investigation", "Resolved"]), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
        c.executemany("INSERT INTO intel_records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        conn.commit()
    conn.close()

def run_query(query):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df