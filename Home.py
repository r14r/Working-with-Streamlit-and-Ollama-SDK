import streamlit as st

from pathlib import Path

st.set_page_config(
    page_title="Ollama SDK Examples",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

def build_navigation():
    """
    Build navigation structure by scanning views subfolders.
    Groups pages by topic derived from subfolder names.
    Icons are shown only in navigation group items, not in filenames.
    
    Returns:
        List of st.Page objects organized by topic sections
    """
    views_dir = Path(__file__).parent / "views"
    
    # Topic configuration with display names and emojis for group navigation
    # Maps folder names (with numeric prefix) to display info
    topics = {
        "0_home": {"name": "🏠 Home", "icon": "🏠", "order": 0},
        "1_chat": {"name": "💬 Chat", "icon": "💬", "order": 1},
        "2_generate": {"name": "✨ Generate", "icon": "✨", "order": 2},
        "3_tools": {"name": "🛠️ Tools", "icon": "🛠️", "order": 3},
        "4_utilities": {"name": "⚙️ Utilities", "icon": "⚙️", "order": 4},
        "5_vision": {"name": "🖼️ Vision", "icon": "🖼️", "order": 5},
        "6_web": {"name": "🌐 Web Search", "icon": "🌐", "order": 6},
        "9_helper": {"name": "🔧 Helper", "icon": "🔧", "order": 9}
    }
    
    # Map specific pages to their individual icons
    page_icons = {
        "Thinking": "🧠",
        "Thinking_Generate": "🧠",
        "Thinking_Levels": "🧠",
        "Fill_in_Middle": "💻"
    }
    
    # Build navigation structure
    navigation_pages = {}
    
    # Scan each topic subfolder
    for topic_folder, topic_info in sorted(topics.items(), key=lambda x: x[1]["order"]):
        topic_path = views_dir / topic_folder
        
        if not topic_path.exists():
            continue
            
        # Get all Python files in this topic folder
        py_files = sorted(topic_path.glob("*.py"))
        
        if py_files:
            pages = []
            for py_file in py_files:
                # Extract title from filename (remove number prefix)
                title = py_file.stem.split("_", 1)[1] if "_" in py_file.stem else py_file.stem
                title = title.replace("_", " ")
                
                # Get icon for specific pages, otherwise use topic icon
                icon = page_icons.get(py_file.stem.split("_", 1)[1] if "_" in py_file.stem else "", 
                                     topic_info["icon"])
                icon = None
                
                # Create st.Page for each script
                page = st.Page(
                    str(py_file),
                    title=title,
                    icon=icon
                )
                pages.append(page)
            
            # Add this topic's pages to navigation
            if pages:
                navigation_pages[topic_info["name"]] = pages
    
    return navigation_pages


# -----

# --- Navigation ---

pages = build_navigation()

pg = st.navigation(pages)
pg.run()
