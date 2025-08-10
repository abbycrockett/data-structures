import streamlit as st
from visualizations.tree import visualize_tree

st.title("Data Structure Visualizer")

option = st.sidebar.selectbox(
    "Choose a data structure:",
    ("Tree"),
    index=0
)

if option == "Tree":
    visualize_tree()
