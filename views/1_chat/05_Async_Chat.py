import streamlit as st
from ollama import chat
import asyncio

st.set_page_config(page_title="Async Chat", page_icon="💬", layout="wide")

st.title("💬 Async Chat")
st.markdown("Asynchronous chat operations")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("""
    ⚠️ **Note**: Async operations are not fully supported in Streamlit's synchronous execution model.
    This demo runs the synchronous version. For true async operations, use the Ollama AsyncClient in a native async environment.
    """)
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    user_input = st.text_input("Ask a question:", value="Why is the sky blue?", key="user_input")
    
    if st.button("Send (Sync Mode)", key="send_btn"):
        with st.spinner("Processing..."):
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
    st.code('''import asyncio

from ollama import AsyncClient


async def main():
  messages = [
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ]

  client = AsyncClient()
  response = await client.chat('gemma3', messages=messages)
  print(response['message']['content'])


if __name__ == '__main__':
  asyncio.run(main())
''', language='python')
    
    st.markdown("**Original file:** `src/async-chat.py`")
