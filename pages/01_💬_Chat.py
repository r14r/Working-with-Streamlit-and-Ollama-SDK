import streamlit as st
from ollama import chat

from lib.helper_streamlit import select_model

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

st.title("💬 Chat")
st.markdown("Simple question-answer interaction with the model")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = select_model()
        print(f"model={model}")
    
    # User input
    user_input = st.text_input("Ask a question:", value="Why is the sky blue?", key="user_input")
    
    if st.button("Send", key="send_btn"):
        with st.spinner("Thinking..."):
            messages = [
                {
                    'role': 'user',
                    'content': user_input,
                },
            ]
            
            response = chat(model, messages=messages)
            
            st.success("Response:")
            st.write(response['message']['content'])

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
]

response = chat('gemma3', messages=messages)
print(response['message']['content'])
''', language='python')
    
    st.markdown("**Original file:** `src/chat.py`")
