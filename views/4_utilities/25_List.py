import streamlit as st
from ollama import ListResponse, list

st.set_page_config(page_title="List Models", page_icon="⚙️", layout="wide")

st.title("⚙️ List Models")
st.markdown("List all available Ollama models")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    if st.button("Refresh Model List", key="refresh_btn"):
        with st.spinner("Loading models..."):
            response: ListResponse = list()
            
            st.success(f"Found {len(response.models)} models")
            
            for model in response.models:
                with st.expander(f"📦 {model.model}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Size:** {(model.size.real / 1024 / 1024):.2f} MB")
                        st.write(f"**Modified:** {model.modified_at}")
                    
                    with col2:
                        if model.details:
                            st.write(f"**Format:** {model.details.format}")
                            st.write(f"**Family:** {model.details.family}")
                            st.write(f"**Parameter Size:** {model.details.parameter_size}")
                            st.write(f"**Quantization:** {model.details.quantization_level}")

with tab2:
    st.header("Source Code")
    st.code('''from ollama import ListResponse, list

response: ListResponse = list()

for model in response.models:
  print('Name:', model.model)
  print('  Size (MB):', f'{(model.size.real / 1024 / 1024):.2f}')
  if model.details:
    print('  Format:', model.details.format)
    print('  Family:', model.details.family)
    print('  Parameter Size:', model.details.parameter_size)
    print('  Quantization Level:', model.details.quantization_level)
  print('\\n')
''', language='python')
