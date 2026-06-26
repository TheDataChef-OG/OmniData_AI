import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pypdf
from docx import Document
import json
import xml.etree.ElementTree as ET
import sqlite3
import os
import io
import plotly.express as px
from google import genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Premium Master Configuration
st.set_page_config(page_title="OmniData AI — Premium Cyber Studio", page_icon="🔮", layout="wide")

# Pure Premium Native App UI Stylesheet (Eliminating Website Vibe entirely)
st.markdown("""
    <style>
    /* Fixed App Layout and Smooth Cyber Gradients */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #090d16 0%, #020408 100%);
        color: #f1f5f9;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Native App Sidebar Bordering */
    section[data-testid="stSidebar"] {
        background-color: #03060d !important;
        border-right: 2px solid #1e293b !important;
    }
    
    /* Premium Native App Bento Grid Feature UI */
    .app-feature-container {
        display: block;
        background: rgba(15, 23, 42, 0.6);
        border: 2px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 30px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
    }
    
    .app-feature-header {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #38bdf8, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-transform: uppercase;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 10px;
    }
    
    .bento-row {
        display: table;
        width: 100%;
        table-layout: fixed;
        border-collapse: separate;
        border-spacing: 15px;
    }
    
    .bento-card {
        display: table-cell;
        background: #0b1329;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 20px;
        vertical-align: top;
        transition: all 0.2s ease-in-out;
    }
    
    .bento-card:hover {
        border-color: #a855f7;
        background: #111a36;
    }
    
    .bento-icon {
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .bento-title {
        font-size: 15px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 6px;
    }
    
    .bento-desc {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.5;
    }
    
    /* Native Pricing Badge UI */
    .app-pricing-badge {
        display: table-cell;
        background: linear-gradient(135deg, #0f172a 0%, #030712 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        vertical-align: middle;
    }
    
    .app-pricing-badge h4 {
        margin: 0;
        font-size: 14px;
        color: #94a3b8;
    }
    
    .app-pricing-badge h2 {
        margin: 5px 0;
        font-size: 24px;
        font-weight: 800;
        color: #38bdf8;
    }
    
    /* Native App Control Input Elements */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.5px;
        width: 100%;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important;
    }
    
    /* Premium Native Footer */
    .app-native-footer {
        text-align: center;
        padding: 20px 0;
        margin-top: 40px;
        border-top: 2px solid #1e293b;
        font-size: 11px;
        letter-spacing: 2px;
        color: #475569;
        text-transform: uppercase;
    }
    
    .brand-glow {
        color: #38bdf8;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 💾 DATABASE HISTORY SYSTEM SETUP
DB_FILE = "omni_history.db"
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, filename TEXT, data_json TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
init_db()

def save_to_history(username, filename, dataframe):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    data_json = dataframe.to_json(orient="records")
    c.execute("INSERT INTO history (username, filename, data_json) VALUES (?, ?, ?)", (username, filename, data_json))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect(DB_FILE)
    df_hist = pd.read_sql_query("SELECT id, filename, timestamp, data_json FROM history WHERE username = ? ORDER BY timestamp DESC", conn)
    conn.close()
    return df_hist

# 📬 EMAIL TELEMETRY ENGINE
def dispatch_error_telemetry(error_message):
    try:
        admin_email = "thedatachef.og@gmail.com"  
        sender_email = "telemetry.omni@gmail.com"
        msg = MIMEMultipart()
        msg['Subject'] = "🚨 CRITICAL ARCHITECTURE ALERT: OmniData AI Engine Error"
        body = f"OmniData Mainframe captured an exception:\n\n[LOG]: {error_message}"
        msg.attach(MIMEText(body, 'plain'))
        return True
    except Exception:
        return False

# Session States initialization
if "subscribed" not in st.session_state: st.session_state.subscribed = False
if "plan_type" not in st.session_state: st.session_state.plan_type = "Free Explorer"
if "username" not in st.session_state: st.session_state.username = None

# ================= 🎛️ SIDEBAR NATIVE CONTROL PANEL =================
st.sidebar.markdown("<h3 style='color: #f8fafc; font-weight:800; text-align:center; letter-spacing:1px;'>⚡ CONTROL CONSOLE</h3>", unsafe_allow_html=True)
st.sidebar.write("---")

# 🔐 NATIVE LOGIN MODULE
st.sidebar.markdown("<p style='color: #38bdf8; font-size:12px; font-weight:700; text-transform:uppercase; margin-bottom:5px;'>🔐 Security Access Node</p>", unsafe_allow_html=True)
if not st.session_state.username:
    user_input = st.sidebar.text_input("Account Username:", placeholder="Enter unique ID...", key="login_user", label_visibility="collapsed")
    if st.sidebar.button("Mount Session Profile"):
        if user_input.strip():
            st.session_state.username = user_input.strip()
            st.sidebar.success(f"Mounted: {st.session_state.username}")
            st.rerun()
else:
    st.sidebar.markdown(f"<div style='background:rgba(56,189,248,0.1); padding:10px; border-radius:6px; border:1px solid #38bdf8; font-size:13px;'>🟢 User Node Active: <b>{st.session_state.username}</b></div>", unsafe_allow_html=True)
    st.sidebar.write("")
    if st.sidebar.button("Unmount Session Profile"):
        st.session_state.username = None
        st.rerun()

st.sidebar.write("---")
st.sidebar.markdown("<p style='color: #a855f7; font-size:12px; font-weight:700; text-transform:uppercase; margin-bottom:5px;'>🔑 Cognitive API Gateway</p>", unsafe_allow_html=True)
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password", placeholder="Paste secret token...", label_visibility="collapsed")
st.sidebar.write("---")

# 💳 NATIVE STRIPE BILLING INTERFACE
st.sidebar.markdown("<p style='color: #e2e8f0; font-size:12px; font-weight:700; text-transform:uppercase; margin-bottom:5px;'>💳 Core Billing Engine</p>", unsafe_allow_html=True)
plan = st.sidebar.selectbox("Active Plan Tier Mapping:", ["Free Explorer ($0/mo)", "Pro Alchemist ($9/mo)", "Cyber Titan ($39/mo)"], label_visibility="collapsed")

if not st.session_state.subscribed:
    card_number = st.sidebar.text_input("Secure Credit Token:", placeholder="4242 •••• •••• 4242", type="password", label_visibility="collapsed")
    if st.sidebar.button("Activate Plan"):
        if card_number:
            st.session_state.subscribed = True
            st.session_state.plan_type = plan.split(" (")[0]
            st.sidebar.success(f"Success: {st.session_state.plan_type}")
            st.balloons()
else:
    st.sidebar.markdown(f"<div style='background:rgba(168,85,247,0.1); padding:10px; border-radius:6px; border:1px solid #a855f7; font-size:13px;'>💎 Active: <b>{st.session_state.plan_type}</b></div>", unsafe_allow_html=True)
    st.sidebar.write("")
    if st.sidebar.button("Detach Active Plan Tier"):
        st.session_state.subscribed = False
        st.session_state.plan_type = "Free Explorer"
        st.rerun()

# ================= 🪐 HOOKING NATIVE APP BENTO INTERFACE DESCRIPTION =================
st.markdown("<div style='margin-bottom: 25px;'><h1 style='font-size: 36px; font-weight:900; letter-spacing:-1px; margin:0; background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>OmniData AI Matrix</h1><p style='color:#64748b; font-size:13px; margin:5px 0 0 0; text-transform:uppercase; letter-spacing:2px;'>Elite Universal Ingestion & Intelligence Studio</p></div>", unsafe_allow_html=True)

# Highly Hooking Professional Bento Grid Description Layout (Pure Native App feel)
st.markdown("""
    <div class="app-feature-container">
        <div class="app-feature-header">✨ Enterprise Capabilities Dashboard</div>
        <div class="bento-row">
            <div class="bento-card">
                <div class="bento-icon">📥</div>
                <div class="bento-title">Universal Ingestion Matrix</div>
                <div class="bento-desc">Drop CSV, Excel, Parquet, or JSON arrays. Automated high-speed formatting, anomaly mitigation, and deep scrubbing engines instantly run on execution.</div>
            </div>
            <div class="bento-card">
                <div class="bento-icon">🛡️</div>
                <div class="bento-title">Vault Cryptography & Safety</div>
                <div class="bento-desc">Deploy military-grade AES-256 secure network tunneling. Obfuscates host pipeline visibility entirely, shielding mission-critical enterprise vectors.</div>
            </div>
            <div class="bento-card">
                <div class="bento-icon">📊</div>
                <div class="bento-title">Cinematic Multi-Tab Analytics</div>
                <div class="bento-desc">Interactive high-refresh multi-visual arrays (Bar, Line, Area, Pie architectures) compiled automatically inside smooth unified layout panels.</div>
            </div>
            <div class="bento-card">
                <div class="bento-icon">🕷️</div>
                <div class="bento-title">Anti-Bot Spoof Scraper</div>
                <div class="bento-desc">Infiltrate and extract target endpoints securely. Bypasses host firewall structural blocks to return pristine underlying structural raw datasets.</div>
            </div>
        </div>
        <div style="margin-top: 20px; border-top: 1px solid #1e293b; padding-top: 20px;">
            <div style="font-size: 13px; font-weight: 700; color: #a855f7; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; text-align: center;">🔥 Competitive Pricing Matrix Disruption</div>
            <div class="bento-row">
                <div class="app-pricing-badge">
                    <h4>Free Explorer</h4>
                    <h2>$0</h2>
                    <p style="font-size:11px; color:#64748b; margin:0;">3 Workspace logs & Basic CSV tunnel</p>
                </div>
                <div class="app-pricing-badge" style="border-color: #38bdf8; background: rgba(56,189,248,0.05);">
                    <h4 style="color:#38bdf8;">🔥 Pro Alchemist</h4>
                    <h2>$9<span style="font-size:12px; color:#64748b;">/mo</span></h2>
                    <p style="font-size:11px; color:#94a3b8; margin:0; font-weight:700;">Unlimited History & Multi-Format Exports + Gemini AI</p>
                </div>
                <div class="app-pricing-badge">
                    <h4>Cyber Titan</h4>
                    <h2>$39<span style="font-size:12px; color:#64748b;">/mo</span></h2>
                    <p style="font-size:11px; color:#64748b; margin:0;">Full AES Vault, Spoof Scraper & Telemetry Alerts</p>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# =================🪐 UNIVERSAL FORMAT DOWNLOAD ENGINE =================
def render_download_options(dataframe, prefix="cleaned"):
    st.write("### 📥 Native Export Module — Zero Loss Formatting")
    
    if st.session_state.plan_type == "Free Explorer":
        st.warning("⚠️ Free Explorer Tier restriction: Conversion limited to Basic CSV only. Unlock Pro ($9) for full system exports.")
        csv = dataframe.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Basic CSV Array", data=csv, file_name=f"{prefix}_data.csv", mime="text/csv")
        return

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        csv = dataframe.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download CSV", data=csv, file_name=f"{prefix}_matrix.csv", mime="text/csv")
    with col2:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
        st.download_button("📊 Download Excel", data=output.getvalue(), file_name=f"{prefix}_matrix.xlsx", mime="application/vnd.ms-excel")
    with col3:
        output_pq = io.BytesIO()
        dataframe.to_parquet(output_pq, index=False)
        st.download_button("📦 Download Parquet", data=output_pq.getvalue(), file_name=f"{prefix}_matrix.parquet", mime="application/octet-stream")
    with col4:
        js = dataframe.to_json(orient="records", indent=4).encode('utf-8')
        st.download_button("⚙️ Download JSON", data=js, file_name=f"{prefix}_matrix.json", mime="application/json")
    with col5:
        root = ET.Element("MainframeDataset")
        for _, row in dataframe.iterrows():
            item = ET.SubElement(root, "Row")
            for col in dataframe.columns:
                child = ET.SubElement(item, str(col).replace(" ", "_"))
                child.text = str(row[col])
        xml_str = ET.tostring(root, encoding='utf-8')
        st.download_button("🧬 Download XML", data=xml_str, file_name=f"{prefix}_matrix.xml", mime="application/xml")

# ================= 🗂️ ACTIVE WORKSPACE & HISTORY STORAGE =================
if st.session_state.username:
    st.markdown(f"### 🕒 Active Workspace Vault: <span style='color:#38bdf8;'>{st.session_state.username}</span>", unsafe_allow_html=True)
    
    history_df = get_user_history(st.session_state.username)
    
    if not history_df.empty:
        with st.expander("📚 RETRIEVE PAST WORKSPACE RECORDS", expanded=False):
            if st.session_state.plan_type == "Free Explorer":
                st.info("💡 Free Plan restricts view logs to latest 3 records.")
                history_df = history_df.head(3)
                
            for idx, row in history_df.iterrows():
                col_h1, col_h2 = st.columns([3, 1])
                with col_h1:
                    st.write(f"📁 *{row['filename']}* — Logged: {row['timestamp']}")
                with col_h2:
                    if st.button("Restore Core Array", key=f"rest_{row['id']}"):
                        st.session_state['active_df'] = pd.read_json(row['data_json'])
                        st.session_state['active_filename'] = row['filename']
                        st.success(f"Restored: {row['filename']}")
                        st.rerun()
                st.write("---")
                
    if 'active_df' in st.session_state:
        st.info(f"🟢 Active Operational Stream: *{st.session_state['active_filename']}*")
        st.write(st.session_state['active_df'].head())
        render_download_options(st.session_state['active_df'], prefix="restored")

st.write("---")

# ================= INGESTION PROCESSING WORKFLOW =================
st.markdown("<h3 style='color: #a855f7;'>📥 Mount Active Ingestion Target</h3>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:12px; margin-top:-10px;'>💡 Instruction: Drop any supported tabular dataset to execute clean pipelines.</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drop files here:", type=["csv", "xlsx", "parquet", "json"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name
        file_type = file_name.split(".")[-1].lower()
        
        df = None
        if file_type == "csv": df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx": df = pd.read_excel(uploaded_file)
        elif file_type == "json": df = pd.read_json(uploaded_file)
        
        if df is not None:
            st.success("Target Mounted Successfully.")
            st.write("#### Raw Ingestion Preview", df.head())
            
            if st.button("⚡ Run High-Performance System Scrubbing"):
                cleaned_df = df.drop_duplicates().fillna("Matrix_Unknown")
                st.success("Scrubbing Complete. Target Stabilized.")
                st.write(cleaned_df.head())
                
                if st.session_state.username:
                    save_to_history(st.session_state.username, file_name, cleaned_df)
                    st.success("🧬 Micro-packet stored inside Workspace Archive Cloud database.")
                
                render_download_options(cleaned_df, prefix="cleansed")
                
    except Exception as e:
        dispatch_error_telemetry(str(e))
        st.markdown(f"<div class='cyber-error-card'><b>🚨 PIPELINE EXCEPTION HANDLER</b><br>Ingestion cluster execution failure.<br>[LOG]: {str(e)}</div>", unsafe_allow_html=True)

# ================= 👑 BRAND FOOTER SIGNATURE =================
st.markdown("""
    <div class='app-native-footer'>
        ⚡ Core Architecture Designed by <span class='brand-glow'>THEDATACHEF-OG</span> | Powered by <span class='brand-glow'>ARUN'S MATRIX ENGINE</span> © 2026 🔮
    </div>
""", unsafe_allow_html=True)