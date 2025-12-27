import streamlit as st
from ollama import chat

st.set_page_config(page_title="Multimodal Chat", page_icon="🖼️", layout="wide")

st.title("🖼️ Multimodal Chat")
st.markdown("Chat with images using vision models")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llava", "bakllava"], index=0)
    
    # User input
    prompt = st.text_input("Ask about the image:", value="What is in this image? Be concise.", key="prompt")
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Analyze Image", key="analyze_btn") and uploaded_file:
        with st.spinner("Analyzing image..."):
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            # Read image bytes
            image_bytes = uploaded_file.read()
            
            response = chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_bytes],
                    }
                ],
            )
            
            st.success("Analysis:")
            st.write(response.message.content)
    elif not uploaded_file and st.session_state.get('analyze_btn'):
        st.warning("Please upload an image first.")

with tab2:
    st.header("Source Code")
    st.code('''from ollama import chat

# from pathlib import Path

# Pass in the path to the image
path = input('Please enter the path to the image: ')

# You can also pass in base64 encoded image data
# img = base64.b64encode(Path(path).read_bytes()).decode()
# or the raw bytes
# img = Path(path).read_bytes()

response = chat(
  model='gemma3',
  messages=[
    {
      'role': 'user',
      'content': 'What is in this image? Be concise.',
      'images': [path],
    }
  ],
)

print(response.message.content)
''', language='python')
