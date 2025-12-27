import streamlit as st
from ollama import chat

st.set_page_config(page_title="Thinking", page_icon="🧠", layout="wide")

st.title("🧠 Thinking Models")
st.markdown("Models that show their reasoning process (DeepSeek-R1)")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: This feature requires the 'deepseek-r1' model")
    
    # User input
    prompt = st.text_input("Ask a question:", value="What is 10 + 23?", key="prompt")
    
    if st.button("Generate with Thinking", key="generate_btn"):
        with st.spinner("Thinking..."):
            messages = [
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]
            
            response = chat('deepseek-r1', messages=messages, think=True)
            
            st.subheader("🤔 Thinking Process:")
            st.text_area("", value=response.message.thinking, height=200, disabled=True, key="thinking")
            
            st.subheader("💡 Response:")
            st.success(response.message.content)

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'What is 10 + 23?',
  },
]

response = chat('deepseek-r1', messages=messages, think=True)

print('Thinking:\\n========\\n\\n' + response.message.thinking)
print('\\nResponse:\\n========\\n\\n' + response.message.content)
''', language='python')
