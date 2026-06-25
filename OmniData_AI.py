import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google import genai

# Page Configuration
st.set_page_config(page_title="OmniData AI", page_icon="📊", layout="wide")
st.title("📊 OmniData AI — Smart Data Hub")

# Initialize Session State for Data
if "main_df" not in st.session_state:
    st.session_state.main_df = None

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["🧹 Data Cleaner", "🕸️ Web Scraper", "🤖 Gemini AI Insights"])

# ==========================================
# 1. DATA CLEANER PAGE
# ==========================================
if page == "🧹 Data Cleaner":
    st.header("Data Cleaning & Processing")
    
    uploaded_file = st.file_uploader("Upload Client File", type=["csv", "xlsx"])

    if uploaded_file:
        if st.session_state.main_df is None:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.main_df = pd.read_csv(uploaded_file)
            else:
                st.session_state.main_df = pd.read_excel(uploaded_file)
    
    if st.session_state.main_df is not None:
        df = st.session_state.main_df
        
        st.write(f"📊 *File Stats:* {df.shape[0]} rows | {df.shape[1]} columns")
        
        st.sidebar.header("Standard Cleaning")
        
        if st.sidebar.button("Remove Duplicates"):
            st.session_state.main_df = df.drop_duplicates()
            st.rerun()
            
        if st.sidebar.button("Clean Text Whitespaces"):
            st.session_state.main_df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            st.rerun()

        if st.sidebar.button("Fill Empty Cells"):
            for col in df.columns:
                if df[col].dtype == "object":
                    st.session_state.main_df[col] = df[col].fillna("Unknown")
                else:
                    st.session_state.main_df[col] = df[col].fillna(0)
            st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.header("Advanced Processing")
        
        date_col = st.sidebar.selectbox("Select Date Column", options=["None"] + list(df.columns))
        
        if date_col != "None":
            if st.sidebar.button("Standardize Date Format"):
                st.session_state.main_df[date_col] = pd.to_datetime(df[date_col], errors='coerce', format='mixed').dt.strftime('%Y-%m-%d')
                st.rerun()

        st.subheader("Current Data Preview")
        st.write(st.session_state.main_df.head())
        
        cleaned_csv = st.session_state.main_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned File",
            data=cleaned_csv,
            file_name="omnidata_output.csv",
            mime="text/csv"
        )

# ==========================================
# 2. WEB SCRAPER PAGE
# ==========================================
elif page == "🕸️ Web Scraper":
    st.header("Simple Web Scraper")
    url = st.text_input("Enter Website URL to Scrape:")
    if st.button("Start Scraping"):
        if url:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                headings = [h1.text.strip() for h1 in soup.find_all('h1')]
                if headings:
                    scrape_df = pd.DataFrame(headings, columns=["Headings Found"])
                    st.write(scrape_df)
                    st.success("Scraping Completed!")
                else:
                    st.warning("No H1 tags found.")
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# 3. GEMINI AI INSIGHTS PAGE
# ==========================================
elif page == "🤖 Gemini AI Insights":
    st.header("Gemini AI Data Insights")
    
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    
    if st.session_state.main_df is not None:
        df_summary = st.session_state.main_df.head(10).to_string() # Context for Gemini
        user_question = st.text_input("Ask Gemini about your data (e.g., 'Summarize this data', 'Find top trends'):")
        
        if st.button("Analyze with Gemini"):
            if api_key and user_question:
                with st.spinner("Gemini ആലോചിച്ചുകൊണ്ടിരിക്കുകയാണ്... 🤖"):
                    try:
                        # Initialize GenAI Client
                        client = genai.Client(api_key=api_key)
                        
                        prompt = f"""
                        You are a professional data analyst. Analyze the following data sample and answer the user's question.
                        
                        Data Sample:
                        {df_summary}
                        
                        User Question: {user_question}
                        """
                        
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        st.subheader("🤖 Gemini Analysis:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error with Gemini API: {e}")
            else:
                st.warning("Please enter both your API Key and a question.")
    else:
        st.warning("⚠️ Please upload a file in the 'Data Cleaner' section first to let Gemini analyze it.")
        import requests
from bs4 import BeautifulSoup

# --- WEB SCRAPER SECTION ---
st.markdown("---")
st.header("🕸️ Smart Web Scraper")

url = st.text_input("Enter Web URL to Scrape data:")

if st.button("Start Scraping"):
    if url:
        try:
            with st.spinner("Scraping data from website..."):
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
                    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
                    
                    scrape_data = {"Type": ["Heading"]*len(headings) + ["Link"]*len(links),
                                   "Content": headings + links}
                    
                    scrape_df = pd.DataFrame(scrape_data)
                    st.success("Data Scraped Successfully!")
                    st.dataframe(scrape_df)
                    
                    st.session_state['df'] = scrape_df
                else:
                    st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
        # --- DATA VISUALIZER SECTION ---
st.markdown("---")
st.header("📊 Smart Data Visualizer")

if 'df' in st.session_state and st.session_state['df'] is not None:
    df_visual = st.session_state['df']
    
    numeric_cols = df_visual.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df_visual.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if numeric_cols:
        st.subheader("Generate Custom Charts")
        
        chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Line Chart", "Area Chart"])
        
        x_axis = st.selectbox("Select X-Axis (Category):", categorical_cols if categorical_cols else df_visual.columns.tolist())
        y_axis = st.selectbox("Select Y-Axis (Value):", numeric_cols)
        
        if st.button("Generate Chart"):
            if chart_type == "Bar Chart":
                st.bar_chart(df_visual.set_index(x_axis)[y_axis])
            elif chart_type == "Line Chart":
                st.line_chart(df_visual.set_index(x_axis)[y_axis])
            elif chart_type == "Area Chart":
                st.area_chart(df_visual.set_index(x_axis)[y_axis])
    else:
        st.subheader("Data Distribution (Scraped Content Summary)")
        if 'Type' in df_visual.columns:
            type_counts = df_visual['Type'].value_counts()
            st.bar_chart(type_counts)
        else:
            st.info("Upload a file with numeric columns or scrape a website to see advanced graphical charts.")
else:
    st.info("Please upload a file or scrape data above to unlock the Visualizer Dashboard.")