import streamlit as st
import asyncio
import ollama

st.set_page_config(page_title="Async Generate", page_icon="✨", layout="wide")

st.title("✨ Asynchronous Generate")
st.markdown("Asynchronous text generation")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

async def async_generate(model: str, prompt: str):
    client = ollama.AsyncClient()
    response = await client.generate(model, prompt)
    return response['response']

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    prompt = st.text_area("Enter your prompt:", value="Why is the sky blue?", height=100, key="prompt")
    
    if st.button("Generate Async", key="generate_btn"):
        with st.spinner("Generating asynchronously..."):
            response = asyncio.run(async_generate(model, prompt))
            
            st.success("Generated Response:")
            st.write(response)

with tab2:
    st.header("Source Code")
    st.code('''import asyncio

import ollama


async def main():
  client = ollama.AsyncClient()
  response = await client.generate('gemma3', 'Why is the sky blue?')
  print(response['response'])


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print('\\nGoodbye!')
''', language='python')
