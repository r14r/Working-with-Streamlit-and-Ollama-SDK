import streamlit as st
from ollama import chat

st.set_page_config(page_title="Chat Logprobs", page_icon="💬", layout="wide")

st.title("💬 Chat with Logprobs")
st.markdown("View the model's confidence in its token predictions")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    user_input = st.text_input("Ask a question:", value="What is the capital of France?", key="user_input")
    
    if st.button("Send with Logprobs", key="send_btn"):
        with st.spinner("Processing..."):
            messages = [{'role': 'user', 'content': user_input}]
            response = chat(model, messages=messages, options={'num_predict': 50, 'temperature': 0.7})
            
            st.success("Response:")
            st.write(response.message.content)
            
            # Note: Logprobs display would require the actual response structure
            with st.expander("View Response Details"):
                st.json(response.model_dump())

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'What is the capital of France?',
  },
]

response = chat('gemma3', messages=messages, options={'num_predict': 50, 'temperature': 0.7})
print(response.message.content)
''', language='python')
    
    st.markdown("**Original file:** `src/chat-logprobs.py`")
