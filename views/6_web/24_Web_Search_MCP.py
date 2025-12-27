import streamlit as st

st.set_page_config(page_title="Web Search MCP", page_icon="🌐", layout="wide")

st.title("🌐 Web Search with MCP")
st.markdown("Model Context Protocol server for Ollama web search")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ This is an MCP (Model Context Protocol) server implementation")
    
    st.markdown("""
    ### About MCP Server
    
    This script creates an MCP stdio server that exposes Ollama's `web_search` and `web_fetch` as tools.
    
    **Features:**
    - Exposes web_search and web_fetch as MCP tools
    - Supports both FastMCP and low-level stdio server APIs
    - Can be used with MCP-compatible clients
    
    **Environment:**
    - Requires `OLLAMA_API_KEY` environment variable
    
    **Usage:**
    ```bash
    python src/web-search-mcp.py
    ```
    
    This server runs as a stdio server and communicates via stdin/stdout with MCP clients.
    """)
    
    st.warning("⚠️ This is not an interactive demo. This script runs as an MCP server.")
    
    st.markdown("""
    ### Testing the MCP Server
    
    To test this MCP server:
    
    1. Run the server:
       ```bash
       python src/web-search-mcp.py
       ```
    
    2. Connect an MCP client to use the tools
    
    3. Available tools:
       - `web_search(query, max_results=3)` - Perform web search
       - `web_fetch(url)` - Fetch content from URL
    """)

with tab2:
    st.header("Source Code")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/web-search-mcp.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
    
    st.markdown("""
    ### Key Components
    
    - **FastMCP**: High-level API for creating MCP servers (preferred)
    - **stdio_server**: Low-level API fallback if FastMCP not available
    - **Tools**: web_search and web_fetch exposed as MCP tools
    - **Environment**: Uses OLLAMA_API_KEY for authentication
    """)
