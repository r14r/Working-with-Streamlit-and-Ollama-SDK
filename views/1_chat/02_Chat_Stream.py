import streamlit as st
from ollama import chat

st.set_page_config(page_title="Chat Stream", page_icon="💬", layout="wide")

st.title("💬 Chat with Streaming")
st.markdown("See the response as it's being generated")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    user_input = st.text_input("Ask a question:", value="Why is the sky blue?", key="user_input")
    
    if st.button("Send with Streaming", key="send_btn"):
        messages = [
            {
                'role': 'user',
                'content': user_input,
            },
        ]
        
        response_placeholder = st.empty()
        full_response = ""
        
        for part in chat(model, messages=messages, stream=True):
            full_response += part['message']['content']
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
]

for part in chat('gemma3', messages=messages, stream=True):
  print(part['message']['content'], end='', flush=True)
''', language='python')
    
    st.markdown("**Original file:** `src/chat-stream.py`")
