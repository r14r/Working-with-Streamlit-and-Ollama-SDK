import streamlit as st
from streamlit import navigation

from pathlib import Path

st.set_page_config(
    page_title="Ollama SDK Examples",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🦙 Ollama SDK Examples")
st.markdown("""
Welcome to the **Ollama SDK Interactive Examples**! This application demonstrates various features 
and capabilities of the Ollama SDK through interactive Streamlit pages.

Each example includes **two tabs**:
- **🎯 Demo**: Interactive demonstration of the functionality
- **📄 Source Code**: Original source code from the example
""")

st.divider()

def show_introduction():
    with st.expander("📚 About This Application", expanded=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.header("📚 About This Application")
            st.markdown("""
            This collection contains **32 interactive examples** covering all major aspects of the Ollama SDK:
            
            - **💬 Chat** (5 examples): Basic chat, streaming, history management, logprobs, async operations
            - **✨ Generate** (8 examples): Text generation, streaming, thinking models, code completion
            - **🖼️ Vision** (3 examples): Multimodal capabilities with images and vision-language models
            - **🛠️ Tools** (5 examples): Function calling, multi-tool usage, and GPT-OSS integration
            - **🌐 Web Search** (3 examples): Web search capabilities and RAG implementations
            - **⚙️ Utilities** (8 examples): Model management, embeddings, and structured outputs
            
            Navigate using the sidebar to explore each example individually!
            """)

        with col2:
            st.header("🚀 Quick Start")
            st.markdown("""
            1. Select a page from the sidebar
            2. Use the **🎯 Demo** tab to try it
            3. Check **📄 Source Code** tab to see how it works
            4. Experiment with settings
            
            **Requirements:**
            - Ollama installed and running
            - Models downloaded (gemma3, llama3.2, etc.)
            - Python packages installed
            """)

def show_example_listing():
    with st.expander("📖 All Examples"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("💬 Chat (5)")
            st.markdown("""
            1. **Chat** - Basic interaction
            2. **Chat Stream** - Streaming responses
            3. **Chat History** - Conversation context
            4. **Chat Logprobs** - Token probabilities
            5. **Async Chat** - Async operations
            """)
            
            st.subheader("✨ Generate (8)")
            st.markdown("""
            6. **Generate** - Simple generation
            7. **Generate Stream** - Streaming
            8. **Generate Logprobs** - With probabilities
            9. **Async Generate** - Async generation
            10. **🧠 Thinking** - DeepSeek-R1 reasoning
            11. **🧠 Thinking Generate** - With generation
            12. **🧠 Thinking Levels** - Different levels
            13. **💻 Fill in Middle** - Code completion
            """)

        with col2:
            st.subheader("🖼️ Vision (3)")
            st.markdown("""
            14. **Multimodal Chat** - Image Q&A
            15. **Multimodal Generate** - Image description
            16. **Structured Outputs Image** - JSON from images
            """)
            
            st.subheader("🛠️ Tools (5)")
            st.markdown("""
            17. **Tools** - Function calling basics
            18. **Async Tools** - Async function calling
            19. **Multi Tool** - Multiple tool calls
            20. **GPT-OSS Tools** - Advanced tools
            21. **GPT-OSS Tools Stream** - Streaming tools
            """)

        with col3:
            st.subheader("🌐 Web Search (3)")
            st.markdown("""
            22. **Web Search** - Search and fetch
            23. **Web Search GPT-OSS** - Advanced browser
            24. **Web Search MCP** - MCP integration
            """)
            
            st.subheader("⚙️ Utilities (8)")
            st.markdown("""
            25. **List** - Available models
            26. **PS** - Running processes
            27. **Show** - Model info
            28. **Pull** - Download models
            29. **Create** - Custom models
            30. **Embed** - Generate embeddings
            31. **Structured Outputs** - JSON responses
            32. **Async Structured Outputs** - Async JSON
            """)

def show_tips_and_resources():
    with st.expander("💡 Tips & Best Practices"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🎯 Model Selection")
            st.markdown("""
            - **gemma3**: Fast, general purpose
            - **llama3.1/3.2**: Balanced performance
            - **qwen3**: Good for tool use
            - **deepseek-r1**: Reasoning tasks
            - **codellama**: Code generation
            """)

        with col2:
            st.subheader("⚡ Performance")
            st.markdown("""
            - Use streaming for better UX
            - Smaller models = faster responses
            - Quantized models save memory
            - Adjust context length as needed
            - Cache frequently used models
            """)

        with col3:
            st.subheader("🔧 Configuration")
            st.markdown("""
            - Temperature: 0 = deterministic
            - Top_p: nucleus sampling
            - Max tokens: limit response length
            - System prompts: guide behavior
            - Format: enforce JSON structure
            """)

def show_resources():
    with st.expander("📖 Resources"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Official Documentation:**
            - [Ollama GitHub](https://github.com/ollama/ollama)
            - [Ollama Python SDK](https://github.com/ollama/ollama-python)
            - [Model Library](https://ollama.com/library)
            """)

        with col2:
            st.markdown("""
            **This Application:**
            - Navigate pages via sidebar
            - Source code in `/src` directory
            - Streamlit pages in `/pages` directory
            """)


def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with Streamlit and Ollama SDK | 🦙 Powered by Ollama</p>
        <p><strong>32 Interactive Examples</strong> - Each with Demo & Source Code</p>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 **Get started by selecting an example from the sidebar!**")
show_introduction()

show_example_listing()
show_tips_and_resources()
show_resources()
show_footer()