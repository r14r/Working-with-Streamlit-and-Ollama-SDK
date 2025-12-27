import streamlit as st
from ollama import chat

st.set_page_config(page_title="Thinking Levels", page_icon="🧠", layout="wide")

st.title("🧠 Thinking Levels")
st.markdown("Different levels of thinking detail")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: This feature requires the 'gpt-oss:20b' model")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        level = st.selectbox("Thinking Level", ["low", "medium", "high"], index=1)
    
    # User input
    prompt = st.text_input("Ask a question:", value="What is 10 + 23?", key="prompt")
    
    if st.button("Generate with Thinking Level", key="generate_btn"):
        with st.spinner(f"Thinking at {level} level..."):
            messages = [
                {'role': 'user', 'content': prompt},
            ]
            
            response = chat('gpt-oss:20b', messages=messages, think=level)
            
            st.subheader(f"🤔 Thinking ({level}):")
            st.text_area("", value=response.message.thinking, height=200, disabled=True, key="thinking")
            
            st.subheader("💡 Response:")
            st.success(response.message.content)

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat


def heading(text):
  print(text)
  print('=' * len(text))


messages = [
  {'role': 'user', 'content': 'What is 10 + 23?'},
]

# gpt-oss supports 'low', 'medium', 'high'
levels = ['low', 'medium', 'high']
for i, level in enumerate(levels):
  response = chat('gpt-oss:20b', messages=messages, think=level)

  heading(f'Thinking ({level})')
  print(response.message.thinking)
  print('\\n')
  heading('Response')
  print(response.message.content)
  print('\\n')
  if i < len(levels) - 1:
    print('-' * 20)
    print('\\n')
''', language='python')
