import streamlit as st
from ollama import generate

st.set_page_config(page_title="Fill in Middle", page_icon="💻", layout="wide")

st.title("💻 Fill in Middle")
st.markdown("Code completion - generate code between prefix and suffix")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: This feature works best with code models like 'codellama:7b-code'")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
        num_predict = st.slider("Max tokens", 32, 512, 128, 32)
    
    # User input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prefix (before cursor)")
        prefix = st.text_area("", value='def remove_non_ascii(s: str) -> str:\n    """ ', height=150, key="prefix")
    
    with col2:
        st.subheader("Suffix (after cursor)")
        suffix = st.text_area("", value='\n    return result\n', height=150, key="suffix")
    
    if st.button("Fill in Middle", key="generate_btn"):
        with st.spinner("Generating code..."):
            response = generate(
                model='codellama:7b-code',
                prompt=prefix,
                suffix=suffix,
                options={
                    'num_predict': num_predict,
                    'temperature': temperature,
                    'top_p': 0.9,
                    'stop': ['<EOT>'],
                },
            )
            
            st.subheader("Generated Code:")
            full_code = prefix + response['response'] + suffix
            st.code(full_code, language='python')

with tab2:
    st.header("Source Code")
    st.code('''from ollama import generate

prompt = \'\'\'def remove_non_ascii(s: str) -> str:
    """ \'\'\'

suffix = """
    return result
"""

response = generate(
  model='codellama:7b-code',
  prompt=prompt,
  suffix=suffix,
  options={
    'num_predict': 128,
    'temperature': 0,
    'top_p': 0.9,
    'stop': ['<EOT>'],
  },
)

print(response['response'])
''', language='python')
