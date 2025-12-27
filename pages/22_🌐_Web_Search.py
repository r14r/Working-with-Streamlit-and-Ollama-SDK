import streamlit as st
from typing import Union
from ollama import WebFetchResponse, WebSearchResponse, chat, web_fetch, web_search

st.set_page_config(page_title="Web Search", page_icon="🌐", layout="wide")

st.title("🌐 Web Search")
st.markdown("Use web search and web fetch tools to answer questions")

# Create tabs
tab1, tab2 = st.tabs(["🎯 Demo", "📄 Source Code"])

def format_tool_results(results: Union[WebSearchResponse, WebFetchResponse], user_search: str):
    """Format tool results for display"""
    output = []
    if isinstance(results, WebSearchResponse):
        output.append(f'**Search results for "{user_search}":**\n')
        for result in results.results:
            output.append(f"📄 **{result.title if result.title else 'Result'}**")
            output.append(f"   🔗 {result.url}")
            output.append(f"   {result.content[:200]}...")
            output.append('')
        return '\n\n'.join(output)
    
    elif isinstance(results, WebFetchResponse):
        output.append(f'**Fetch results for "{user_search}":**\n')
        output.extend([
            f'**Title:** {results.title}',
            f'**URL:** {user_search}' if user_search else '',
            f'**Content:** {results.content[:300]}...',
        ])
        if results.links:
            output.append(f'**Links:** {", ".join(results.links[:5])}...')
        return '\n\n'.join(output)

with tab1:
    st.header("Interactive Demo")
    
    st.info("⚠️ Note: Web search requires API access")
    
    # Sidebar settings
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Select Model", ["qwen3", "llama3.1"], index=0)
    
    # User input
    query = st.text_input("Enter your query:", value="what is ollama's new engine", key="query")
    
    if st.button("Search", key="search_btn"):
        with st.spinner("Searching..."):
            available_tools = {'web_search': web_search, 'web_fetch': web_fetch}
            
            messages = [{'role': 'user', 'content': query}]
            
            st.write(f"**Query:** {query}")
            st.divider()
            
            iteration = 0
            max_iterations = 3
            
            while iteration < max_iterations:
                iteration += 1
                
                response = chat(
                    model=model,
                    messages=messages,
                    tools=[web_search, web_fetch],
                    think=True
                )
                
                if response.message.thinking:
                    with st.expander(f"🤔 Thinking (iteration {iteration})"):
                        st.text(response.message.thinking)
                
                if response.message.content:
                    st.write(f"**Content (iteration {iteration}):**")
                    st.write(response.message.content)
                
                messages.append(response.message)
                
                if response.message.tool_calls:
                    st.write(f"**🔧 Tool Calls (iteration {iteration}):**")
                    for tool_call in response.message.tool_calls:
                        function_to_call = available_tools.get(tool_call.function.name)
                        if function_to_call:
                            args = tool_call.function.arguments
                            st.write(f"- Calling `{tool_call.function.name}` with: `{args}`")
                            
                            try:
                                result: Union[WebSearchResponse, WebFetchResponse] = function_to_call(**args)
                                
                                user_search = args.get('query', '') or args.get('url', '')
                                formatted_results = format_tool_results(result, user_search=user_search)
                                
                                with st.expander("📊 Results Preview"):
                                    st.markdown(formatted_results[:500])
                                
                                # Cap result at ~2000 tokens
                                messages.append({
                                    'role': 'tool',
                                    'content': formatted_results[:2000 * 4],
                                    'tool_name': tool_call.function.name
                                })
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                                messages.append({
                                    'role': 'tool',
                                    'content': f'Error: {str(e)}',
                                    'tool_name': tool_call.function.name
                                })
                        else:
                            st.error(f"Tool {tool_call.function.name} not found")
                    st.divider()
                else:
                    st.success("✅ Search completed")
                    break

with tab2:
    st.header("Source Code")
    with open('/Users/Shared/CLOUD/Programmier-Workshops/Kurse/Ollama/Fortgeschrittene/Working-with-Ollama-SDK/src/web-search.py', 'r') as f:
        source_code = f.read()
    st.code(source_code, language='python')
