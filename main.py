import streamlit as st
import os
from visualizations.tree import visualize_tree

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="Data Structure Visualizer",
    page_icon="📊",
    layout="centered",
)

# Apply VS Code-inspired CSS
with open(os.path.join(os.path.dirname(__file__), "static", "style.css")) as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

# Force the background color
st.markdown(
    """
    <style>
    .main {
        background-color: #111414 !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #111414 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom sidebar styling
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        background-color: #2a3331;
        border-right: 1px solid #454545;
    }
    section[data-testid="stSidebar"] .css-1vq4p4l {
        padding-top: 5rem;
    }
</style>
""", unsafe_allow_html=True)

option = st.sidebar.selectbox(
    "Pick a data structure:",
    ("Tree"),
    index=0
)

# Add a "Problems" panel at the bottom to mimic VS Code UI
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    <div style="color: #d4d4d4; font-family: 'Segoe UI', sans-serif; font-size: 13px;">
        <strong style="color: #569cd6;">OUTLINE</strong><br/>
        &nbsp;&nbsp;📁 Data Structures<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;└─ 🌳 Tree<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─ BST<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ AVL<br/>
    </div>
    """, unsafe_allow_html=True)

if option == "Tree":
    visualize_tree()
    
# Add a footer with VS Code-like status bar
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #007acc; color: white; font-size: 12px; padding: 2px 10px; display: flex; justify-content: space-between;">
    <div>🐍 Python 3.12</div>
    <div>©️ abbycrockett</div>
</div>
""", unsafe_allow_html=True)

# Hides Streamlit's header
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# This hides the collapse "<<" button on the sidebar:
st.markdown(
    """
    <style>
    [data-testid="stIconMaterial"] {
        display: none;
    }
    [data-testid="stBaseButton-headerNoPadding"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)