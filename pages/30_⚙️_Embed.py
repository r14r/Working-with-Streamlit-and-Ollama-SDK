import streamlit as st
from ollama import embed
import numpy as np

st.set_page_config(page_title="Embeddings", page_icon="⚙️", layout="wide")

st.title("⚙️ Text Embeddings")
st.markdown("Generate vector embeddings from text")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["llama3.2", "nomic-embed-text", "mxbai-embed-large"], index=0)
    
    st.subheader("Generate Embeddings")
    
    text_input = st.text_area("Enter text:", value="Hello, world!", height=100, key="text_input")
    
    if st.button("Generate Embedding", key="embed_btn"):
        with st.spinner("Generating embedding..."):
            try:
                response = embed(model=model, input=text_input)
                embeddings = response['embeddings'][0]
                
                st.success("✅ Embedding generated!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Embedding Dimension", len(embeddings))
                    st.metric("First Value", f"{embeddings[0]:.6f}")
                    st.metric("Last Value", f"{embeddings[-1]:.6f}")
                
                with col2:
                    st.metric("Mean", f"{np.mean(embeddings):.6f}")
                    st.metric("Std Dev", f"{np.std(embeddings):.6f}")
                    st.metric("L2 Norm", f"{np.linalg.norm(embeddings):.6f}")
                
                with st.expander("📊 View First 20 Values"):
                    st.write(embeddings[:20])
                
                with st.expander("📈 Visualization"):
                    st.line_chart(embeddings[:100])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.divider()
    
    st.subheader("Compare Embeddings (Similarity)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        text1 = st.text_input("Text 1:", value="I love programming", key="text1")
    
    with col2:
        text2 = st.text_input("Text 2:", value="I enjoy coding", key="text2")
    
    if st.button("Compare Similarity", key="compare_btn"):
        with st.spinner("Comparing..."):
            try:
                emb1 = embed(model=model, input=text1)['embeddings'][0]
                emb2 = embed(model=model, input=text2)['embeddings'][0]
                
                similarity = cosine_similarity(emb1, emb2)
                
                st.metric("Cosine Similarity", f"{similarity:.4f}")
                
                st.progress(float(similarity))
                
                if similarity > 0.8:
                    st.success("Very similar texts!")
                elif similarity > 0.5:
                    st.info("Moderately similar texts")
                else:
                    st.warning("Different texts")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.header("Source Code")
    st.code('''from ollama import embed

response = embed(model='llama3.2', input='Hello, world!')
print(response['embeddings'])
''', language='python')
