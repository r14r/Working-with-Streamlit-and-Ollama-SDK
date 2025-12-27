import streamlit as st
from ollama import Client
from ollama._types import ChatResponse
from typing import Iterator
import random

st.set_page_config(page_title="GPT-OSS Tools Stream", page_icon="🛠️", layout="wide")

st.title("🛠️ GPT-OSS Tools with Streaming")
st.markdown("Function calling with streaming responses")

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
    
    if st.button("Get Weather with Streaming", key="weather_btn"):
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
            st.subheader(f"Iteration {iteration}")
            
            response_stream: Iterator[ChatResponse] = client.chat(
                model=model,
                messages=messages,
                tools=[get_weather, get_weather_conditions],
                stream=True
            )
            
            tool_calls = []
            thinking = ''
            content = ''
            
            thinking_placeholder = st.empty()
            content_placeholder = st.empty()
            
            for chunk in response_stream:
                if chunk.message.tool_calls:
                    tool_calls.extend(chunk.message.tool_calls)
                
                if chunk.message.content:
                    content += chunk.message.content
                    content_placeholder.markdown(f"**Content:** {content}▌")
                
                if chunk.message.thinking:
                    thinking += chunk.message.thinking
                    with thinking_placeholder:
                        with st.expander("🤔 Thinking", expanded=False):
                            st.text(thinking)
            
            if content:
                content_placeholder.markdown(f"**Content:** {content}")
            
            if thinking != '' or content != '' or len(tool_calls) > 0:
                messages.append({
                    'role': 'assistant',
                    'thinking': thinking,
                    'content': content,
                    'tool_calls': tool_calls
                })
            
            if tool_calls:
                st.write("**🔧 Tool Calls:**")
                for tool_call in tool_calls:
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
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/gpt-oss-tools-stream.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
