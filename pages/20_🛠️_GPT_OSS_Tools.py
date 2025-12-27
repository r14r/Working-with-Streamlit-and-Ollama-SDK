import streamlit as st
from ollama import Client
from ollama._types import ChatResponse
import random

st.set_page_config(page_title="GPT-OSS Tools", page_icon="🛠️", layout="wide")

st.title("🛠️ GPT-OSS Tools")
st.markdown("Function calling with GPT-OSS models")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def get_weather(city: str) -> str:
    """Get the current temperature for a city"""
    temperatures = list(range(-10, 35))
    temp = random.choice(temperatures)
    return f'The temperature in {city} is {temp}°C'

def get_weather_conditions(city: str) -> str:
    """Get the weather conditions for a city"""
    conditions = ['sunny', 'cloudy', 'rainy', 'snowy', 'foggy']
    return random.choice(conditions)

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: This requires the 'gpt-oss:20b' model")
    
    # City selection
    cities = ['London', 'Paris', 'New York', 'Tokyo', 'Sydney', 'Toronto', 'Berlin']
    col1, col2 = st.columns(2)
    with col1:
        city1 = st.selectbox("First city:", cities, index=0)
    with col2:
        city2 = st.selectbox("Second city:", cities, index=5)
    
    if st.button("Get Weather", key="weather_btn"):
        with st.spinner("Processing..."):
            available_tools = {
                'get_weather': get_weather,
                'get_weather_conditions': get_weather_conditions
            }
            
            messages = [{'role': 'user', 'content': f'What is the weather like in {city1}? What are the conditions in {city2}?'}]
            
            st.write(f"**Query:** {messages[0]['content']}")
            st.divider()
            
            client = Client()
            model = 'gpt-oss:20b'
            
            iteration = 0
            max_iterations = 5
            
            while iteration < max_iterations:
                iteration += 1
                
                response: ChatResponse = client.chat(
                    model=model,
                    messages=messages,
                    tools=[get_weather, get_weather_conditions]
                )
                
                if response.message.content:
                    st.write(f"**Content (iteration {iteration}):**")
                    st.write(response.message.content)
                
                if response.message.thinking:
                    with st.expander(f"🤔 Thinking (iteration {iteration})"):
                        st.text(response.message.thinking)
                
                messages.append(response.message)
                
                if response.message.tool_calls:
                    st.write(f"**🔧 Tool Calls (iteration {iteration}):**")
                    for tool_call in response.message.tool_calls:
                        function_to_call = available_tools.get(tool_call.function.name)
                        if function_to_call:
                            result = function_to_call(**tool_call.function.arguments)
                            st.write(f"- `{tool_call.function.name}` with args `{tool_call.function.arguments}` → {result}")
                            messages.append({'role': 'tool', 'content': result, 'tool_name': tool_call.function.name})
                        else:
                            st.error(f"Tool {tool_call.function.name} not found")
                            messages.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
                    st.divider()
                else:
                    st.success("✅ Completed - No more tool calls")
                    break

with tab2:
    st.header("Source Code")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/gpt-oss-tools.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
