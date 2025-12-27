import streamlit as st
from ollama import ShowResponse, show

st.set_page_config(page_title="Show Model Info", page_icon="⚙️", layout="wide")

st.title("⚙️ Show Model Information")
st.markdown("Display detailed information about a specific model")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.text_input("Model name:", value="gemma3")
    
    if st.button("Show Model Info", key="show_btn"):
        with st.spinner(f"Loading info for {model}..."):
            try:
                response: ShowResponse = show(model)
                
                st.success(f"Model Information: {model}")
                
                tab_general, tab_modelfile, tab_template, tab_params = st.tabs(
                    ["📋 General", "📝 Modelfile", "🔧 Template", "⚙️ Parameters"]
                )
                
                with tab_general:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Basic Info")
                        st.write(f"**Modified at:** {response.modified_at}")
                        if response.details:
                            st.write(f"**Details:**")
                            st.json(response.details.model_dump() if hasattr(response.details, 'model_dump') else str(response.details))
                    
                    with col2:
                        st.subheader("Capabilities")
                        if response.capabilities:
                            st.json(response.capabilities)
                        else:
                            st.info("No capabilities information available")
                
                with tab_modelfile:
                    st.subheader("Modelfile")
                    st.code(response.modelfile if response.modelfile else "No modelfile available", language='dockerfile')
                
                with tab_template:
                    st.subheader("Template")
                    st.code(response.template if response.template else "No template available", language='jinja2')
                
                with tab_params:
                    st.subheader("Parameters")
                    if response.parameters:
                        st.code(response.parameters, language='text')
                    else:
                        st.info("No parameters information available")
                    
                    st.subheader("Model Info")
                    if response.modelinfo:
                        st.json(response.modelinfo)
                    else:
                        st.info("No model info available")
                
                with st.expander("📜 License"):
                    st.text(response.license if response.license else "No license information available")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.header("Source Code")
    st.code('''from ollama import ShowResponse, show

response: ShowResponse = show('gemma3')
print('Model Information:')
print(f'Modified at:   {response.modified_at}')
print(f'Template:      {response.template}')
print(f'Modelfile:     {response.modelfile}')
print(f'License:       {response.license}')
print(f'Details:       {response.details}')
print(f'Model Info:    {response.modelinfo}')
print(f'Parameters:    {response.parameters}')
print(f'Capabilities:  {response.capabilities}')
''', language='python')
