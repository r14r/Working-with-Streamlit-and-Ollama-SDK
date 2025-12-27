import streamlit as st
from ollama import pull

st.set_page_config(page_title="Pull Model", page_icon="⚙️", layout="wide")

st.title("⚙️ Pull Model")
st.markdown("Download a model from Ollama registry")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.text_input("Model to pull:", value="gemma3")
    
    if st.button("Pull Model", key="pull_btn"):
        st.info(f"Pulling model: {model}")
        
        progress_container = st.container()
        status_placeholder = st.empty()
        
        with progress_container:
            progress_bar = st.progress(0)
            
            try:
                progress_states = {}
                total_progress = 0
                
                for progress in pull(model, stream=True):
                    status = progress.get('status', '')
                    digest = progress.get('digest', '')
                    completed = progress.get('completed', 0)
                    total = progress.get('total', 0)
                    
                    # Update status
                    status_placeholder.text(f"Status: {status}")
                    
                    # Track progress per digest
                    if digest and total > 0:
                        progress_states[digest] = (completed, total)
                        
                        # Calculate overall progress
                        total_completed = sum(c for c, t in progress_states.values())
                        total_size = sum(t for c, t in progress_states.values())
                        
                        if total_size > 0:
                            total_progress = total_completed / total_size
                            progress_bar.progress(min(total_progress, 1.0))
                    
                    # Show status changes without digest
                    elif status and not digest:
                        st.text(status)
                
                progress_bar.progress(1.0)
                status_placeholder.success(f"✅ Successfully pulled {model}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.header("Source Code")
    st.code('''from tqdm import tqdm

from ollama import pull

current_digest, bars = '', {}
for progress in pull('gemma3', stream=True):
  digest = progress.get('digest', '')
  if digest != current_digest and current_digest in bars:
    bars[current_digest].close()

  if not digest:
    print(progress.get('status'))
    continue

  if digest not in bars and (total := progress.get('total')):
    bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

  if completed := progress.get('completed'):
    bars[digest].update(completed - bars[digest].n)

  current_digest = digest
''', language='python')
