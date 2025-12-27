import streamlit as st
from typing import Iterable
import ollama

st.set_page_config(page_title="Generate Logprobs", page_icon="✨", layout="wide")

st.title("✨ Generate with Log Probabilities")
st.markdown("Text generation with token probabilities")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def format_logprobs(logprobs: Iterable[dict]) -> str:
    """Format log probabilities for display"""
    output = []
    for entry in logprobs:
        token = entry.get('token', '')
        logprob = entry.get('logprob')
        output.append(f"**Token:** `{token}` | **Logprob:** {logprob:.3f}")
        for alt in entry.get('top_logprobs', []):
            if alt['token'] != token:
                output.append(f"  → Alt: `{alt['token']}` (logprob: {alt['logprob']:.3f})")
    return "\n\n".join(output)

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
        top_logprobs = st.slider("Top Logprobs", 1, 5, 3)
    
    # User input
    prompt = st.text_input("Enter your prompt:", value="hi! be concise.", key="prompt")
    
    if st.button("Generate with Logprobs", key="generate_btn"):
        with st.spinner("Generating..."):
            response = ollama.generate(
                model=model,
                prompt=prompt,
                logprobs=True,
                top_logprobs=top_logprobs,
            )
            
            st.success("Generated Response:")
            st.write(response['response'])
            
            st.subheader("Token Probabilities")
            logprobs_text = format_logprobs(response.get('logprobs', []))
            st.markdown(logprobs_text)

with tab2:
    st.header("Source Code")
    st.code('''from typing import Iterable

import ollama


def print_logprobs(logprobs: Iterable[dict], label: str) -> None:
  print(f'\\n{label}:')
  for entry in logprobs:
    token = entry.get('token', '')
    logprob = entry.get('logprob')
    print(f'  token={token!r:<12} logprob={logprob:.3f}')
    for alt in entry.get('top_logprobs', []):
      if alt['token'] != token:
        print(f'    alt -> {alt["token"]!r:<12} ({alt["logprob"]:.3f})')


response = ollama.generate(
  model='gemma3',
  prompt='hi! be concise.',
  logprobs=True,
  top_logprobs=3,
)
print('Generate response:', response['response'])
print_logprobs(response.get('logprobs', []), 'generate logprobs')
''', language='python')
