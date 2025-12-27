import streamlit as st
from ollama import generate
import httpx

st.set_page_config(page_title="Multimodal Generate", page_icon="🖼️", layout="wide")

st.title("🖼️ Multimodal Generate")
st.markdown("Generate text from images - Example with XKCD comics")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("This demo fetches random XKCD comics and explains them using vision models")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["llava", "bakllava"], index=0)
    
    # User input
    comic_num = st.number_input("Comic number (0 for random):", min_value=0, max_value=3000, value=0, step=1)
    
    if st.button("Fetch & Explain Comic", key="fetch_btn"):
        with st.spinner("Fetching comic..."):
            try:
                # Get latest comic number
                latest = httpx.get('https://xkcd.com/info.0.json')
                latest.raise_for_status()
                max_num = latest.json().get('num')
                
                # Use random if 0, otherwise use specified number
                import random
                num = comic_num if comic_num > 0 else random.randint(1, max_num)
                
                # Fetch the comic
                comic = httpx.get(f'https://xkcd.com/{num}/info.0.json')
                comic.raise_for_status()
                comic_data = comic.json()
                
                st.subheader(f"xkcd #{comic_data.get('num')}: {comic_data.get('title')}")
                st.image(comic_data.get('img'), use_container_width=True)
                st.caption(comic_data.get('alt'))
                
                # Fetch image content
                raw = httpx.get(comic_data.get('img'))
                raw.raise_for_status()
                
                st.subheader("Explanation:")
                response_placeholder = st.empty()
                full_response = ""
                
                for response in generate(model, 'explain this comic:', images=[raw.content], stream=True):
                    full_response += response['response']
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.header("Source Code")
    st.code('''import random
import sys

import httpx

from ollama import generate

latest = httpx.get('https://xkcd.com/info.0.json')
latest.raise_for_status()

num = int(sys.argv[1]) if len(sys.argv) > 1 else random.randint(1, latest.json().get('num'))

comic = httpx.get(f'https://xkcd.com/{num}/info.0.json')
comic.raise_for_status()

print(f'xkcd #{comic.json().get("num")}: {comic.json().get("alt")}')
print(f'link: https://xkcd.com/{num}')
print('---')

raw = httpx.get(comic.json().get('img'))
raw.raise_for_status()

for response in generate('llava', 'explain this comic:', images=[raw.content], stream=True):
  print(response['response'], end='', flush=True)

print()
''', language='python')
