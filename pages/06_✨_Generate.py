import streamlit as st
from ollama import generate

st.set_page_config(page_title="Generate", page_icon="✨", layout="wide")

st.title("✨ Generate")
st.markdown("Simple text generation from a prompt")

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
    
    if st.button("Generate", key="generate_btn"):
        with st.spinner("Generating..."):
            response = generate(model, prompt)
            
            st.success("Generated Response:")
            st.write(response['response'])

with tab2:
    st.header("Source Code")
    st.code('''from ollama import generate

response = generate('gemma3', 'Why is the sky blue?')
print(response['response'])
''', language='python')
