import streamlit as st
from pydantic import BaseModel
import asyncio
import ollama
import json

st.set_page_config(page_title="Async Structured Outputs", page_icon="⚙️", layout="wide")

st.title("⚙️ Asynchronous Structured Outputs")
st.markdown("Get structured JSON responses asynchronously")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

# Define the schema
class FriendInfo(BaseModel):
    name: str
    age: int
    is_available: bool

class FriendList(BaseModel):
    friends: list[FriendInfo]

async def async_structured_output(model: str, prompt: str):
    """Async function to get structured output"""
    client = ollama.AsyncClient()
    response = await client.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        format=FriendList.model_json_schema(),
        options={'temperature': 0},
    )
    
    friends_response = FriendList.model_validate_json(response.message.content)
    return friends_response

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["llama3.1:8b", "llama3.2", "qwen2.5"], index=0)
    
    st.subheader("Schema Definition")
    
    st.code('''class FriendInfo(BaseModel):
    name: str
    age: int
    is_available: bool

class FriendList(BaseModel):
    friends: list[FriendInfo]
''', language='python')
    
    st.subheader("Generate Structured Data Asynchronously")
    
    prompt = st.text_area(
        "Enter your prompt:",
        value="I have two friends. The first is Ollama 22 years old busy saving the world, and the second is Alonso 23 years old and wants to hang out. Return a list of friends in JSON format",
        height=100,
        key="prompt"
    )
    
    if st.button("Generate Async", key="generate_btn"):
        with st.spinner("Generating asynchronously..."):
            try:
                friends_response = asyncio.run(async_structured_output(model, prompt))
                
                st.success("✅ Structured data generated asynchronously!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Parsed Data")
                    for friend in friends_response.friends:
                        with st.container():
                            st.markdown(f"**{friend.name}**")
                            st.write(f"Age: {friend.age}")
                            st.write(f"Available: {'✅ Yes' if friend.is_available else '❌ No'}")
                            st.divider()
                
                with col2:
                    st.subheader("Raw JSON")
                    st.json(json.loads(friends_response.model_dump_json()))
                
                st.subheader("Schema Used")
                st.json(FriendList.model_json_schema())
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error("Make sure the model supports structured outputs")
    
    st.divider()
    
    st.markdown("""
    ### About Async Structured Outputs
    
    Async structured outputs provide:
    - Non-blocking operations
    - Better performance for multiple requests
    - Structured JSON validation
    - Type safety with Pydantic
    
    **Use Cases:**
    - High-throughput applications
    - Multiple concurrent requests
    - Responsive UIs
    - Batch processing
    """)

with tab2:
    st.header("Source Code")
    st.code('''import asyncio

from pydantic import BaseModel

from ollama import AsyncClient


# Define the schema for the response
class FriendInfo(BaseModel):
  name: str
  age: int
  is_available: bool


class FriendList(BaseModel):
  friends: list[FriendInfo]


async def main():
  client = AsyncClient()
  response = await client.chat(
    model='llama3.1:8b',
    messages=[{'role': 'user', 'content': 'I have two friends. The first is Ollama 22 years old busy saving the world, and the second is Alonso 23 years old and wants to hang out. Return a list of friends in JSON format'}],
    format=FriendList.model_json_schema(),  # Use Pydantic to generate the schema
    options={'temperature': 0},  # Make responses more deterministic
  )

  # Use Pydantic to validate the response
  friends_response = FriendList.model_validate_json(response.message.content)
  print(friends_response)


if __name__ == '__main__':
  asyncio.run(main())
''', language='python')
