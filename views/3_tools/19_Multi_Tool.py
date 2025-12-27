import streamlit as st
from ollama import ChatResponse, Client
import random

st.set_page_config(page_title="Multi Tool", page_icon="🛠️", layout="wide")

st.title("🛠️ Multi-Tool Calling")
st.markdown("Models can call multiple tools in a single interaction")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def get_temperature(city: str) -> int:
    """Get the temperature for a city in Celsius"""
    if city not in ['London', 'Paris', 'New York', 'Tokyo', 'Sydney']:
        return 'Unknown city'
    return str(random.randint(0, 35)) + ' degrees Celsius'

def get_conditions(city: str) -> str:
    """Get the weather conditions for a city"""
    if city not in ['London', 'Paris', 'New York', 'Tokyo', 'Sydney']:
        return 'Unknown city'
    conditions = ['sunny', 'cloudy', 'rainy', 'snowy']
    return random.choice(conditions)

with tab1:
    st.header("Interactive Demo")
    
    st.info("The model can call multiple tools to answer complex questions")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["qwen3", "llama3.1"], index=0)
    
    # City selection
    cities = ['London', 'Paris', 'New York', 'Tokyo', 'Sydney']
    col1, col2 = st.columns(2)
    with col1:
        city1 = st.selectbox("First city:", cities, index=0)
    with col2:
        city2 = st.selectbox("Second city:", cities, index=1)
    
    if st.button("Get Weather Info", key="weather_btn"):
        with st.spinner("Processing..."):
            available_functions = {
                'get_temperature': get_temperature,
                'get_conditions': get_conditions,
            }
            
            messages = [{'role': 'user', 'content': f'What is the temperature in {city1}? and what are the weather conditions in {city2}?'}]
            
            st.write(f"**Prompt:** {messages[0]['content']}")
            
            client = Client()
            response = client.chat(
                model,
                stream=True,
                messages=messages,
                tools=[get_temperature, get_conditions],
                think=True
            )
            
            thinking_text = ""
            content_text = ""
            tool_calls_list = []
            
            thinking_placeholder = st.empty()
            
            for chunk in response:
                if chunk.message.thinking:
                    thinking_text += chunk.message.thinking
                    with thinking_placeholder.container():
                        st.subheader("🤔 Thinking:")
                        st.text(thinking_text)
                
                if chunk.message.content:
                    content_text += chunk.message.content
                
                if chunk.message.tool_calls:
                    for tool in chunk.message.tool_calls:
                        if function_to_call := available_functions.get(tool.function.name):
                            output = function_to_call(**tool.function.arguments)
                            tool_calls_list.append({
                                'function': tool.function.name,
                                'arguments': tool.function.arguments,
                                'output': output
                            })
                            messages.append(chunk.message)
                            messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
            
            if tool_calls_list:
                st.subheader("🔧 Tool Calls:")
                for tc in tool_calls_list:
                    st.write(f"**Function:** `{tc['function']}` with arguments: {tc['arguments']}")
                    st.write(f"**Output:** {tc['output']}")
                    st.divider()
                
                st.subheader("Getting final result...")
                res = client.chat(model, stream=True, tools=[get_temperature, get_conditions], messages=messages, think=True)
                
                final_response = ""
                for chunk in res:
                    if chunk.message.content:
                        final_response += chunk.message.content
                
                st.success("**Final Result:**")
                st.write(final_response)

with tab2:
    st.header("Source Code")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/multi-tool.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
