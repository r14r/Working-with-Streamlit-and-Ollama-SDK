import streamlit as st
from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from ollama import chat
import json

st.set_page_config(page_title="Structured Outputs Image", page_icon="🖼️", layout="wide")

st.title("🖼️ Structured Outputs from Images")
st.markdown("Extract structured data from images using Pydantic schemas")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

# Define the schema for image objects
class Object(BaseModel):
    name: str
    confidence: float
    attributes: str

class ImageDescription(BaseModel):
    summary: str
    objects: list[Object]
    scene: str
    colors: list[str]
    time_of_day: Literal['Morning', 'Afternoon', 'Evening', 'Night']
    setting: Literal['Indoor', 'Outdoor', 'Unknown']
    text_content: str | None = None

with tab1:
    st.header("Interactive Demo")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["gemma3", "llava", "bakllava"], index=0)
    
    # User input
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Analyze Image", key="analyze_btn") and uploaded_file:
        with st.spinner("Analyzing image..."):
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            # Read image bytes
            image_bytes = uploaded_file.read()
            
            try:
                # Set up chat
                response = chat(
                    model=model,
                    format=ImageDescription.model_json_schema(),
                    messages=[
                        {
                            'role': 'user',
                            'content': 'Analyze this image and return a detailed JSON description including objects, scene, colors and any text detected. If you cannot determine certain details, leave those fields empty.',
                            'images': [image_bytes],
                        },
                    ],
                    options={'temperature': 0},
                )
                
                # Convert received content to the schema
                image_analysis = ImageDescription.model_validate_json(response.message.content)
                
                st.success("Structured Analysis:")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Summary")
                    st.write(image_analysis.summary)
                    
                    st.subheader("Scene Information")
                    st.write(f"**Scene:** {image_analysis.scene}")
                    st.write(f"**Setting:** {image_analysis.setting}")
                    st.write(f"**Time of Day:** {image_analysis.time_of_day}")
                    
                    st.subheader("Colors")
                    st.write(", ".join(image_analysis.colors))
                
                with col2:
                    st.subheader("Detected Objects")
                    for obj in image_analysis.objects:
                        with st.expander(f"{obj.name} ({obj.confidence:.2f})"):
                            st.write(f"**Attributes:** {obj.attributes}")
                    
                    if image_analysis.text_content:
                        st.subheader("Text Content")
                        st.write(image_analysis.text_content)
                
                st.subheader("Raw JSON")
                st.json(json.loads(image_analysis.model_dump_json()))
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    elif not uploaded_file and st.session_state.get('analyze_btn'):
        st.warning("Please upload an image first.")

with tab2:
    st.header("Source Code")
    st.code('''from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from ollama import chat


# Define the schema for image objects
class Object(BaseModel):
  name: str
  confidence: float
  attributes: str


class ImageDescription(BaseModel):
  summary: str
  objects: list[Object]
  scene: str
  colors: list[str]
  time_of_day: Literal['Morning', 'Afternoon', 'Evening', 'Night']
  setting: Literal['Indoor', 'Outdoor', 'Unknown']
  text_content: str | None = None


# Get path from user input
path = input('Enter the path to your image: ')
path = Path(path)

# Verify the file exists
if not path.exists():
  raise FileNotFoundError(f'Image not found at: {path}')

# Set up chat as usual
response = chat(
  model='gemma3',
  format=ImageDescription.model_json_schema(),  # Pass in the schema for the response
  messages=[
    {
      'role': 'user',
      'content': 'Analyze this image and return a detailed JSON description including objects, scene, colors and any text detected. If you cannot determine certain details, leave those fields empty.',
      'images': [path],
    },
  ],
  options={'temperature': 0},  # Set temperature to 0 for more deterministic output
)


# Convert received content to the schema
image_analysis = ImageDescription.model_validate_json(response.message.content)
print(image_analysis)
''', language='python')
