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
import plotly.express as px
from google import genai

# Premium Master Configuration
st.set_page_config(page_title="OmniData AI — Premium Cyber Studio", page_icon="🔮", layout="wide")

# Deep Psychological Dark UI Style Sheets (Premium Cyberpunk Neon Palette)
st.markdown("""
    <style>
    /* Main Background & Text Color Tweaks */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Neon Cyberpunk Style Cards for Master Guide */
    .master-guide {
        background: linear-gradient(145deg, #111827 0%, #030712 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.15);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 30px;
    }
    
    .guide-title {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .feature-badge {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid #06b6d4;
        color: #06b6d4;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* Premium Button Overrides */
    .stButton>button {
        background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(217, 70, 239, 0.5) !important;
    }
    
    /* Modern Form Borders */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0b0f19 !important;
        border: 1px solid #1e293b !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Render Stylish Emblem & Tagline
st.markdown("""
    <div style='text-align: center; padding: 20px 0; margin-bottom: 10px;'>
        <div style='font-size: 55px; font-weight: 900; letter-spacing: 4px; background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 50%, #d946ef 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⌁ OMNIDATA AI ⌁</div>
        <div style='color: #94a3b8; font-size: 14px; font-weight: 500; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px;'>Universal Ingestion. Intelligent Insights.</div>
    </div>
""", unsafe_allow_html=True)
st.write("---")

# ================= 📖 THE ULTIMATE MASTER USER GUIDE (INTERNATIONALIZED) =================
with st.expander("👑 ULTIMATE SYSTEM USER GUIDE (CLICK TO EXPAND)", expanded=True):
    st.markdown("""
    <div class='master-guide'>
        <div class='guide-title'>🌌 Master OmniData AI in 10 Seconds</div>
        <p style='color: #94a3b8; font-size: 14px;'>Get the most out of this premium cyber studio with our quick-start operational workflow:</p>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;'>
            <div style='background: #0f172a; padding: 15px; border-radius: 10px; border-top: 3px solid #06b6d4;'>
                <span class='feature-badge'>STEP 01</span>
                <h5 style='color: #f1f5f9;'>Universal Data Ingestion</h5>
                <p style='color: #94a3b8; font-size: 13px;'>Drop any <b>CSV, Excel, Word, PDF</b>, or a massive <b>SQL Database (.db)</b> into the secure mainframe. The engine extracts the architecture instantly.</p>
            </div>
            <div style='background: #0f172a; padding: 15px; border-radius: 10px; border-top: 3px solid #8b5cf6;'>
                <span class='feature-badge'>STEP 02</span>
                <h5 style='color: #f1f5f9;'>Interactive Visualizer</h5>
                <p style='color: #94a3b8; font-size: 13px;'>Once uploaded, the <b>Live Visualizer</b> unlocks below. Dynamically change X and Y axes to plot stunning interactive charts.</p>
            </div>
            <div style='background: #0f172a; padding: 15px; border-radius: 10px; border-top: 3px solid #d946ef;'>
                <span class='feature-badge'>STEP 03</span>
                <h5 style='color: #f1f5f9;'>Advanced Web Extraction</h5>
                <p style='color: #94a3b8; font-size: 13px;'>Inject any target web URL. The automated scraper bypasses basic firewalls to pull critical structural content.</p>
            </div>
            <div style='background: #0f172a; padding: 15px; border-radius: 10px; border-top: 3px solid #10b981;'>
                <span class='feature-badge'>STEP 04</span>
                <h5 style='color: #f1f5f9;'>Cognitive Gemini AI</h5>
                <p style='color: #94a3b8; font-size: 13px;'>Provide your secure <b>Gemini API Key</b> and trigger the engine to run exhaustive deep analytics, predictions, and predictive modeling.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Global variables for data passing to AI
data_summary_for_ai = ""

# Helper function to render Visual Dashboard
def render_dashboard(dataframe):
    st.write("---")
    st.markdown("<h3 style='color: #06b6d4;'>📊 2. Premium Interactive Dashboard</h3>", unsafe_allow_html=True)
    numeric_cols = dataframe.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = dataframe.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(numeric_cols) > 0:
        dash_col1, dash_col2 = st.columns(2)
        with dash_col1:
            x_axis = st.selectbox("Select X-Axis Parameters:", categorical_cols if categorical_cols else numeric_cols, key="x_ax")
            y_axis = st.selectbox("Select Y-Axis Metrics:", numeric_cols, key="y_ax")
            chart_type = st.radio("Select Cinematic Chart Architecture:", ["Bar Chart", "Line Chart", "Scatter Plot"], horizontal=True)
            
            if chart_type == "Bar Chart":
                fig = px.bar(dataframe, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#06b6d4'])
            elif chart_type == "Line Chart":
                fig = px.line(dataframe, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#8b5cf6'])
            else:
                fig = px.scatter(dataframe, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#d946ef'])
        with dash_col2:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No tabular columns metrics found to map advanced dashboard visuals.")

# ================= SECTION 1: UNIVERSAL DATA PROCESSOR =================
st.markdown("<h3 style='color: #8b5cf6;'>📥 1. High-Performance Universal Data Ingestion</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop any data variant array (CSV, XLSX, PARQUET, PDF, DOCX, TXT, JSON, XML, DB, SQLITE) into the secure mainframe:", 
    type=["csv", "xlsx", "parquet", "pdf", "docx", "txt", "json", "xml", "db", "sqlite"], 
    key="universal_uploader"
)

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_type = file_name.split(".")[-1].lower()
    st.balloons() 
    st.success(f"⚡ Secure Stream Connection Verified: {file_name}")
    
    try:
        df = None
        # Handle Tabular Architectures
        if file_type in ["csv", "xlsx", "parquet"]:
            if file_type == "csv": df = pd.read_csv(uploaded_file)
            elif file_type == "xlsx": df = pd.read_excel(uploaded_file)
            else: df = pd.read_parquet(uploaded_file)
            
        elif file_type in ["db", "sqlite"]:
            with open(file_name, "wb") as f: f.write(uploaded_file.getbuffer())
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            if tables:
                selected_table = st.selectbox("Choose Mainframe Target Database Table:", tables)
                df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
            conn.close()
            if os.path.exists(file_name): os.remove(file_name)
            
        elif file_type == "json":
            df = pd.read_json(uploaded_file)
            
        # Display and Clean Data if it's Tabular
        if df is not None:
            st.write("### Mainframe Data Preview", df.head())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Purge Overlapping Duplicates"):
                    df = df.drop_duplicates()
                    st.success("Mainframe Data Purged!")
            with col2:
                if st.button("Auto-Fill Empty Nodes"):
                    for col in df.columns:
                        df[col] = df[col].fillna("Unknown") if df[col].dtype == "object" else df[col].fillna(df[col].mean())
                    st.success("Empty Nodes Restored!")
            with col3:
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Cleaned CSV", data=csv_data, file_name="cleaned_mainframe_data.csv", mime="text/csv")
                
            st.write("### Refined Core Analytics Output", df)
            render_dashboard(df)
            data_summary_for_ai = f"Tabular Data Summary:\nColumns: {list(df.columns)}\nRows: {len(df)}\nSample Data:\n{df.head(10).to_string()}"

        # Handle Document Text Streams
        elif file_type == "pdf":
            pdf_reader = pypdf.PdfReader(uploaded_file)
            extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
            st.text_area("Extracted System PDF Text Data Stream", extracted_text, height=200)
            data_summary_for_ai = f"PDF Text:\n{extracted_text[:3000]}"

        elif file_type == "docx":
            doc = Document(uploaded_file)
            extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text])
            st.text_area("Extracted System Word Text Data Stream", extracted_text, height=200)
            data_summary_for_ai = f"Word Document Text:\n{extracted_text[:3000]}"
            
        elif file_type == "txt":
            extracted_text = uploaded_file.read().decode("utf-8")
            st.text_area("Extracted Plain Text Data Stream", extracted_text, height=200)
            data_summary_for_ai = f"Text File Content:\n{extracted_text[:3000]}"

    except Exception as e:
        st.error(f"Ingestion Core Matrix Engine Failure: {str(e)}")

st.write("---")

# ================= SECTION 2: SMART WEB SCRAPER =================
st.markdown("<h3 style='color: #d946ef;'>🕷️ 2. Premium Anti-Bot Spoofing Web Scraper</h3>", unsafe_allow_html=True)
url_input = st.text_input("Inject target endpoint URL to extract structural matrix:", placeholder="https://example.com")

if st.button("Initialize Secure Infiltration"):
    if url_input:
        with st.spinner("Cracking host server firewall filters..."):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
                response = requests.get(url_input, headers=headers, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3']) if h.text.strip()]
                    paragraphs = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]
                    st.success("Mainframe Data Decrypted Successfully!")
                    st.write("#### Captured Host Headings", headings[:10])
                    data_summary_for_ai = f"Scraped Data from {url_input}:\nHeadings: {headings[:20]}\nParagraphs: {paragraphs[:10]}"
                else:
                    st.error(f"Infiltration Aborted. Status Code Check: {response.status_code}")
            except Exception as e:
                st.error(f"Network Infiltration Timeout: {str(e)}")

st.write("---")

# ================= SECTION 3: GEMINI AI INSIGHTS =================
st.markdown("<h3 style='color: #10b981;'>🧠 3. Gemini Deep Cognitive Intelligence Engine</h3>", unsafe_allow_html=True)
api_key_input = st.text_input("Enter secure Gemini API Key to initialize cognitive matrix:", type="password")

if api_key_input:
    st.write("#### ⚡ AI Intelligence System Presets:")
    preset_col1, preset_col2, preset_col3 = st.columns(3)
    
    chosen_preset = ""
    with preset_col1:
        if st.button("🚀 Forecast Future Trends"):
            chosen_preset = "Analyze the provided dataset and predict the top 5 critical micro and macro trends for the upcoming quarters with high probability matrices."
    with preset_col2:
        if st.button("💼 Build Business Scaling Roadmap"):
            chosen_preset = "Based on this structural data, build an exhaustive corporate scaling roadmap outlining critical growth loops and optimization points."
    with preset_col3:
        if st.button("🔍 Detect Hidden Anomaly & Flaws"):
            chosen_preset = "Perform a deep behavioral forensic check on this data text. Identify hidden logical anomalies, vulnerabilities, or potential mathematical errors."

    # Prompt text area loaded dynamically if a preset is clicked
    custom_prompt = st.text_area("Direct Prompt Directive Callout Parameter:", value=chosen_preset if chosen_preset else "Analyze this entire data structured context and provide comprehensive business insights, key trends, and potential flaws.")
    
    if st.button("Launch AI Intelligence Core"):
        if data_summary_for_ai:
            with st.spinner("Gemini Cognitive Synapses Firing..."):
                try:
                    client = genai.Client(api_key=api_key_input)
                    full_prompt = f"Data Content:\n{data_summary_for_ai}\n\nUser Request: {custom_prompt}"
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=full_prompt)
                    st.markdown("<h4 style='color: #10b981;'>💎 Gemini AI Strategic Core Report:</h4>", unsafe_allow_html=True)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Cognitive Synapses Matrix Halted: {str(e)}")
        else:
            st.warning("Data parameter buffer empty. Ingest a file first.")
else:
    st.info("💡 Input your secure Gemini API Key above to unlock the Deep Intelligence Engine Mainframe Dashboard.") 