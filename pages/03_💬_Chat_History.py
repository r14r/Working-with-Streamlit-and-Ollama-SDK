import streamlit as st
from ollama import chat

st.set_page_config(page_title="Chat with History", page_icon="💬", layout="wide")

st.title("💬 Chat with History")
st.markdown("Maintain conversation context across multiple exchanges")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                'role': 'user',
                'content': 'Why is the sky blue?',
            },
            {
                'role': 'assistant',
                'content': "The sky is blue because of the way the Earth's atmosphere scatters sunlight.",
            },
            {
                'role': 'user',
                'content': 'What is the weather in Tokyo?',
            },
            {
                'role': 'assistant',
                'content': """The weather in Tokyo is typically warm and humid during the summer months, with temperatures often exceeding 30°C (86°F). The city experiences a rainy season from June to September, with heavy rainfall and occasional typhoons. Winter is mild, with temperatures rarely dropping below freezing.""",
            },
        ]
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
    
    # Chat input
    if user_input := st.chat_input("Continue the conversation..."):
        # Add user message to history
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(model, messages=st.session_state.chat_history)
                st.write(response.message.content)
                
                # Add assistant response to history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response.message.content
                })
    
    if st.button("Clear History", key="clear_history"):
        st.session_state.chat_history = []
        st.rerun()

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
  {
    'role': 'assistant',
    'content': "The sky is blue because of the way the Earth's atmosphere scatters sunlight.",
  },
  {
    'role': 'user',
    'content': 'What is the weather in Tokyo?',
  },
  {
    'role': 'assistant',
    'content': """The weather in Tokyo is typically warm and humid during the summer months, with temperatures often exceeding 30°C (86°F). The city experiences a rainy season from June to September, with heavy rainfall and occasional typhoons. Winter is mild, with temperatures
    rarely dropping below freezing. The city is known for its high-tech and vibrant culture, with many popular tourist attractions such as the Tokyo Tower, Senso-ji Temple, and the bustling Shibuya district.""",
  },
]

while True:
  user_input = input('Chat with history: ')
  response = chat(
    'gemma3',
    messages=[*messages, {'role': 'user', 'content': user_input}],
  )

  # Add the response to the messages to maintain the history
  messages += [
    {'role': 'user', 'content': user_input},
    {'role': 'assistant', 'content': response.message.content},
  ]
  print(response.message.content + '\\n')
''', language='python')
    
    st.markdown("**Original file:** `src/chat-with-history.py`")
