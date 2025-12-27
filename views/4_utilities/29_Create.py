import streamlit as st
from ollama import Client

st.set_page_config(page_title="Create Model", page_icon="⚙️", layout="wide")

st.title("⚙️ Create Custom Model")
st.markdown("Create a customized model from an existing one")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("Create a custom model by modifying an existing model's system prompt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_name = st.text_input("New model name:", value="my-assistant", key="model_name")
        base_model = st.selectbox("Base model:", ["gemma3", "llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    with col2:
        system_prompt = st.text_area(
            "System prompt:",
            value="You are mario from Super Mario Bros.",
            height=150,
            key="system_prompt"
        )
    
    if st.button("Create Model", key="create_btn"):
        with st.spinner(f"Creating model {model_name}..."):
            try:
                client = Client()
                response = client.create(
                    model=model_name,
                    from_=base_model,
                    system=system_prompt,
                    stream=False,
                )
                
                st.success(f"✅ Model created successfully!")
                st.write(f"**Status:** {response.status}")
                
                st.info("You can now use this model in other demos")
                
                # Test the model
                if st.button("Test Model", key="test_btn"):
                    from ollama import chat
                    
                    test_response = chat(
                        model=model_name,
                        messages=[{'role': 'user', 'content': 'Hello! Who are you?'}]
                    )
                    
                    st.subheader("Test Response:")
                    st.write(test_response.message.content)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.divider()
    
    st.markdown("""
    ### About Custom Models
    
    Custom models allow you to:
    - Modify the system prompt
    - Change model behavior and personality
    - Create specialized assistants
    - Fine-tune responses for specific use cases
    
    The created model is saved locally and can be used like any other Ollama model.
    """)

with tab2:
    st.header("Source Code")
    st.code('''from ollama import Client

client = Client()
response = client.create(
  model='my-assistant',
  from_='gemma3',
  system='You are mario from Super Mario Bros.',
  stream=False,
)
print(response.status)
''', language='python')
