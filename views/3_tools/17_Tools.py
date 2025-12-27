import streamlit as st
from ollama import ChatResponse, chat

st.set_page_config(page_title="Tools", page_icon="🛠️", layout="wide")

st.title("🛠️ Function Calling / Tools")
st.markdown("Use function calling to extend model capabilities")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return int(a) + int(b)

def subtract_two_numbers(a: int, b: int) -> int:
    """Subtract two numbers"""
    return int(a) - int(b)

with tab1:
    st.header("Interactive Demo")
    
    st.info("The model can call functions to perform calculations")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    prompt = st.text_input("Ask a math question:", value="What is three plus one?", key="prompt")
    
    if st.button("Send", key="send_btn"):
        with st.spinner("Processing..."):
            messages = [{'role': 'user', 'content': prompt}]
            
            available_functions = {
                'add_two_numbers': add_two_numbers,
                'subtract_two_numbers': subtract_two_numbers,
            }
            
            # Create manual tool definition for subtract
            subtract_tool = {
                'type': 'function',
                'function': {
                    'name': 'subtract_two_numbers',
                    'description': 'Subtract two numbers',
                    'parameters': {
                        'type': 'object',
                        'required': ['a', 'b'],
                        'properties': {
                            'a': {'type': 'integer', 'description': 'The first number'},
                            'b': {'type': 'integer', 'description': 'The second number'},
                        },
                    },
                },
            }
            
            response: ChatResponse = chat(
                model,
                messages=messages,
                tools=[add_two_numbers, subtract_tool],
            )
            
            st.subheader("Model Response:")
            
            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    if function_to_call := available_functions.get(tool.function.name):
                        st.write(f"🔧 **Calling function:** `{tool.function.name}`")
                        st.write(f"**Arguments:** {tool.function.arguments}")
                        output = function_to_call(**tool.function.arguments)
                        st.write(f"**Function output:** {output}")
                        
                        # Add function response to messages
                        messages.append(response.message)
                        messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
                
                # Get final response
                final_response = chat(model, messages=messages)
                st.success("**Final Response:**")
                st.write(final_response.message.content)
            else:
                st.warning("No tool calls returned from model")

with tab2:
    st.header("Source Code")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/tools.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
