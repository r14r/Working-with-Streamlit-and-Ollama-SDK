"""
Example: Using the Helper Libraries

This demonstrates how to use the helper_ollama and helper_streamlit modules
in your Streamlit pages.
"""

import streamlit as st

from lib.helper_ollama import OllamaHelper, get_installed_models
from lib.helper_streamlit import StreamlitOllamaHelper, select_model, render_settings, chat

st.set_page_config(page_title="Helper Example", page_icon="🔧", layout="wide")

st.title("🔧 Helper Libraries Example")
st.markdown("Demonstrating the use of helper_ollama and helper_streamlit modules")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Model Selector", "💬 Chat Helper", "⚙️ Ollama Helper", "📄 Usage Examples"])

# Initialize helpers
ollama_helper = OllamaHelper()
streamlit_helper = StreamlitOllamaHelper()

with tab1:
    st.header("Model Selector Helper")
    st.markdown("Easy model selection with automatic installed model detection")
    
    # Using the helper function
    with st.sidebar:
        st.subheader("Settings")
        selected_model = select_model(
            key="demo_model",
            label="Select Model",
            use_installed=True,
            location="sidebar"
        )
    
    st.success(f"Selected model: **{selected_model}**")
    
    # Show installed models
    st.subheader("Installed Models")
    models = get_installed_models()
    if models:
        st.write(", ".join(models))
    else:
        st.warning("No models installed")
    
    # Model settings
    st.subheader("Model Settings Helper")
    settings = render_settings(
        key_prefix="demo_settings",
        show_temperature=True,
        show_max_tokens=True,
        show_top_p=True,
        location="sidebar"
    )
    
    st.write("**Current Settings:**")
    st.json(settings)

with tab2:
    st.header("Chat Interface Helper")
    st.markdown("Pre-built chat interface with history management")
    
    # Simple chat interface
    model = select_model(key="chat_model", location="main")
    
    st.divider()
    
    # Use the chat helper
    chat(model=model, session_key="helper_chat_history")
    
    # Clear button
    if st.button("Clear Chat History"):
        streamlit_helper.clear_chat_history("helper_chat_history")
        st.rerun()

with tab3:
    st.header("Ollama Helper Functions")
    st.markdown("Direct access to Ollama SDK functionality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Installed Models")
        if st.button("Refresh Models", key="refresh_models"):
            models = ollama_helper.list_models()
            
            for model in models:
                with st.expander(f"📦 {model['name']}"):
                    st.write(f"**Size:** {model['size_mb']} MB")
                    if model['details']:
                        st.write(f"**Family:** {model['details']['family']}")
                        st.write(f"**Format:** {model['details']['format']}")
    
    with col2:
        st.subheader("🚀 Running Models")
        if st.button("Check Running", key="check_running"):
            running = ollama_helper.list_running_models()
            
            if running:
                for model in running:
                    st.info(f"**{model['name']}** - {model['size_mb']:.1f} MB")
            else:
                st.warning("No models running")
    
    st.divider()
    
    # Pull model UI
    streamlit_helper.render_model_pull_ui()

with tab4:
    st.header("Usage Examples")
    
    st.subheader("1. Model Selection")
    st.code('''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lib'))

from helper_streamlit import select_model, render_settings

# Simple model selector in sidebar
model = select_model(key="my_model", location="sidebar")

# Get model settings
settings = render_settings(
    key_prefix="my_settings",
    show_temperature=True,
    show_max_tokens=True
)
''', language='python')
    
    st.subheader("2. Chat Interface")
    st.code('''
from helper_streamlit import chat_interface

# Pre-built chat with history
chat_interface(
    model="gemma3",
    session_key="my_chat_history"
)
''', language='python')
    
    st.subheader("3. Generate Text")
    st.code('''
from helper_streamlit import generate_text

# Generate with streaming
response = generate_text(
    model="gemma3",
    prompt="Write a haiku about coding",
    stream=True
)
''', language='python')
    
    st.subheader("4. Ollama Helper")
    st.code('''
from helper_ollama import OllamaHelper

helper = OllamaHelper()

# List models
models = helper.get_model_names()

# Pull a model
for progress in helper.pull_model("gemma3", stream=True):
    print(progress)

# Check if model exists
if helper.is_model_installed("gemma3"):
    print("Model is ready!")

# Get model info
info = helper.show_model("gemma3")
''', language='python')
    
    st.subheader("5. Custom Chat")
    st.code('''
from helper_streamlit import StreamlitOllamaHelper

helper = StreamlitOllamaHelper()

# Custom chat with options
response = helper.run_chat(
    model="gemma3",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True,
    options={"temperature": 0.7, "num_predict": 100}
)
''', language='python')

st.markdown("---")
st.info("💡 **Tip**: Use these helpers in your pages to reduce boilerplate code!")
