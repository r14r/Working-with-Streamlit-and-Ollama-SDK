import streamlit as st
from ollama import generate

st.set_page_config(page_title="Generate Stream", page_icon="✨", layout="wide")

st.title("✨ Generate with Streaming")
st.markdown("Text generation with streaming output")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    prompt = st.text_area("Enter your prompt:", value="Why is the sky blue?", height=100, key="prompt")
    
    if st.button("Generate with Streaming", key="generate_btn"):
        response_placeholder = st.empty()
        full_response = ""
        
        for part in generate(model, prompt, stream=True):
            full_response += part['response']
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)

with tab2:
    st.header("Source Code")
    st.code('''from ollama import generate

for part in generate('gemma3', 'Why is the sky blue?', stream=True):
  print(part['response'], end='', flush=True)
''', language='python')
