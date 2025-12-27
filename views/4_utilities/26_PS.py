import streamlit as st
from ollama import ProcessResponse, chat, ps, pull

st.set_page_config(page_title="Process Status", page_icon="⚙️", layout="wide")

st.title("⚙️ Process Status (PS)")
st.markdown("View currently loaded models in memory")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("Load Test Model", key="load_btn"):
            with st.spinner("Loading gemma3..."):
                try:
                    # Pull model first
                    response = pull('gemma3', stream=False)
                    # Load it by making a simple request
                    chat(model='gemma3', messages=[{'role': 'user', 'content': 'hi'}])
                    st.success("Model loaded!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("Refresh Status", key="refresh_btn"):
            with st.spinner("Getting process status..."):
                try:
                    response: ProcessResponse = ps()
                    
                    if response.models:
                        st.success(f"Found {len(response.models)} loaded model(s)")
                        
                        for model in response.models:
                            with st.expander(f"🔄 {model.model}", expanded=True):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Digest:** `{model.digest[:20]}...`")
                                    st.write(f"**Expires at:** {model.expires_at}")
                                    st.write(f"**Context length:** {model.context_length}")
                                
                                with col2:
                                    st.write(f"**Size:** {(model.size / 1024 / 1024):.2f} MB")
                                    st.write(f"**Size VRAM:** {(model.size_vram / 1024 / 1024):.2f} MB")
                                    if model.details:
                                        st.write(f"**Details:** {model.details}")
                    else:
                        st.info("No models currently loaded in memory")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.header("Source Code")
    st.code('''from ollama import ProcessResponse, chat, ps, pull

# Ensure at least one model is loaded
response = pull('gemma3', stream=True)
progress_states = set()
for progress in response:
  if progress.get('status') in progress_states:
    continue
  progress_states.add(progress.get('status'))
  print(progress.get('status'))

print('\\n')

print('Waiting for model to load... \\n')
chat(model='gemma3', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])


response: ProcessResponse = ps()
for model in response.models:
  print('Model: ', model.model)
  print('  Digest: ', model.digest)
  print('  Expires at: ', model.expires_at)
  print('  Size: ', model.size)
  print('  Size vram: ', model.size_vram)
  print('  Details: ', model.details)
  print('  Context length: ', model.context_length)
  print('\\n')
''', language='python')
