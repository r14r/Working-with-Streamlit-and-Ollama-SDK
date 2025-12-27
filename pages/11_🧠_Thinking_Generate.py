import streamlit as st
from ollama import generate

st.set_page_config(page_title="Thinking Generate", page_icon="🧠", layout="wide")

st.title("🧠 Thinking Generate")
st.markdown("Generation with thinking process")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: This feature requires the 'deepseek-r1' model")
    
    # User input
    prompt = st.text_input("Enter your prompt:", value="why is the sky blue", key="prompt")
    
    if st.button("Generate with Thinking", key="generate_btn"):
        with st.spinner("Thinking..."):
            response = generate('deepseek-r1', prompt, think=True)
            
            st.subheader("🤔 Thinking Process:")
            st.text_area("", value=response.thinking, height=200, disabled=True, key="thinking")
            
            st.subheader("💡 Response:")
            st.success(response.response)

with tab2:
    st.header("Source Code")
    st.code('''from ollama import generate

response = generate('deepseek-r1', 'why is the sky blue', think=True)

print('Thinking:\\n========\\n\\n' + response.thinking)
print('\\nResponse:\\n========\\n\\n' + response.response)
''', language='python')
