import streamlit as st
import asyncio
import ollama
from ollama import ChatResponse

st.set_page_config(page_title="Async Tools", page_icon="🛠️", layout="wide")

st.title("🛠️ Asynchronous Function Calling")
st.markdown("Use async function calling for better performance")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract_two_numbers(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

async def async_tool_call(model: str, prompt: str):
    """Async function to handle tool calling"""
    messages = [{'role': 'user', 'content': prompt}]
    
    available_functions = {
        'add_two_numbers': add_two_numbers,
        'subtract_two_numbers': subtract_two_numbers,
    }
    
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
    
    client = ollama.AsyncClient()
    
    response: ChatResponse = await client.chat(
        model,
        messages=messages,
        tools=[add_two_numbers, subtract_tool],
    )
    
    results = []
    
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if function_to_call := available_functions.get(tool.function.name):
                results.append({
                    'function': tool.function.name,
                    'arguments': tool.function.arguments,
                    'output': function_to_call(**tool.function.arguments)
                })
                messages.append(response.message)
                messages.append({'role': 'tool', 'content': str(results[-1]['output']), 'tool_name': tool.function.name})
        
        final_response = await client.chat(model, messages=messages)
        return results, final_response.message.content
    
    return None, None

with tab1:
    st.header("Interactive Demo")
    
    st.info("Async function calling allows for non-blocking operations")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["llama3.1", "llama3.2", "qwen2.5"], index=0)
    
    # User input
    prompt = st.text_input("Ask a math question:", value="What is three plus one?", key="prompt")
    
    if st.button("Send", key="send_btn"):
        with st.spinner("Processing asynchronously..."):
            results, final_response = asyncio.run(async_tool_call(model, prompt))
            
            if results:
                st.subheader("Tool Calls:")
                for result in results:
                    st.write(f"🔧 **Function:** `{result['function']}`")
                    st.write(f"**Arguments:** {result['arguments']}")
                    st.write(f"**Output:** {result['output']}")
                    st.divider()
                
                st.success("**Final Response:**")
                st.write(final_response)
            else:
                st.warning("No tool calls returned from model")

with tab2:
    st.header("Source Code")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/async-tools.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
