import streamlit as st
from ollama import Client

st.set_page_config(page_title="Web Search GPT-OSS", page_icon="🌐", layout="wide")

st.title("🌐 Web Search with GPT-OSS")
st.markdown("Advanced web search using GPT-OSS browser tools")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: This requires the 'gpt-oss:120b-cloud' model and the web_search_gpt_oss_helper.py module")
    st.warning("This demo requires the Browser helper class from web_search_gpt_oss_helper.py")
    
    # User input
    query = st.text_input("Enter your query:", value="what is ollama's new engine", key="query")
    
    if st.button("Search", key="search_btn"):
        st.error("This demo requires the Browser helper class which needs to be imported separately.")
        st.info("Please refer to the source code tab to see the implementation.")

with tab2:
    st.header("Source Code")
    
    st.subheader("Main Script (web-search-gpt-oss.py)")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/web-search-gpt-oss.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
    
    st.subheader("Helper Module (web_search_gpt_oss_helper.py)")
    try:
        with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/web_search_gpt_oss_helper.py', 'r') as f:
            helper_code = f.read()
        st.code(helper_code, language='python')
    except FileNotFoundError:
        st.warning("Helper file not found")
