import streamlit as st
import matplotlib.pyplot as plt
from data_structures.stack import Stack

def visualize_stack():
    st.markdown("# Stack 📚")
    st.markdown('''
        <div style="margin-top: 1.5em; margin-bottom: 1.5em;">
        A stack works like a stack of trays in a cafeteria: you can only add (<strong>push</strong>) or remove (<strong>pop</strong>) items from the top. 
        This is the principle of <strong>LIFO</strong>: Last In, First Out.
        <br><br>
        If you don’t want to remove the top item, you can <strong>peek</strong> to see what’s there without taking it off.
        <br><br>
        <span style="color: #46ab61;">/*This is not the same as “Full Stack”! That’s a web development job title. 
        A full-stack developer works on both the front end (what you see in the browser) and the back end (where the app's data and logic live) in a web application.*/</span>
        <br><br>
        For example, if you add items in the order <strong>A, B, C</strong>, see which comes off first!
        </div>
        ''', unsafe_allow_html=True)

    values_list = ['A', 'B', 'C']
    stack = Stack(values_list)
    canvas_placeholder = st.empty()
    st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)
    
    # Use a container with CSS to make controls closer together
    st.markdown("""
    <style>
    .control-container {
        display: flex;
        align-items: center;
        gap: 1px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col_peek, col_pop, col_push, col_input = st.columns([0.2, 0.2, 0.2, 1])
    with col_peek:
        st.markdown("<div style='display: flex; align-items: center; height: 100%; justify-content: flex-start;'>", unsafe_allow_html=True)
        peek_clicked = st.button('Peek', key="stack_peek")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_pop:
        st.markdown("<div style='display: flex; align-items: center; height: 100%; justify-content: flex-start;'>", unsafe_allow_html=True)
        pop_clicked = st.button(' Pop ', key="stack_pop")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_push:
        st.markdown("<div style='display: flex; align-items: center; height: 100%; justify-content: flex-start;'>", unsafe_allow_html=True)
        insert_clicked = st.button('Push➥', key="stack_insert")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_input:
        st.markdown("""
        <style>
        div[data-testid="stTextInput"] > label {
            display: none !important;
        }
        div[data-testid="stTextInput"] > div > div > input {
            margin-top: -1.2em !important;
            padding-top: 1.6em !important;
        }
        </style>
        """, unsafe_allow_html=True)
        insert_value = st.text_input('', '', key="stack_insert_value")
    if 'stack_state' not in st.session_state:
        st.session_state.stack_state = stack.to_list()
    if insert_clicked and insert_value:
        st.session_state.stack_state.append(insert_value)
        st.success(f'Inserted: {insert_value}')
        st.rerun()
    elif peek_clicked:
        if not st.session_state.stack_state:
            st.warning('You took a peek, but the stack is empty!')
        else:
            top_item = st.session_state.stack_state[-1]
            st.info(f'You took a peek, the top item is: {top_item}')
    elif pop_clicked:
        if not st.session_state.stack_state:
            st.warning('Stack is empty!')
        else:
            popped = st.session_state.stack_state.pop()
            st.success(f'Popped: {popped}')
    stack = Stack(st.session_state.stack_state)
    canvas_placeholder.pyplot(draw_stack(stack, return_fig=True), use_container_width=False)

def draw_stack(stack, highlight_index=None, return_fig=False):
    items = stack.to_list()
    fig, ax = plt.subplots(figsize=(6, 2.5))  # Reduced height for canvas
    fig.patch.set_facecolor("#151C15")  # Light blue/gray background similar to tree
    ax.set_xlim(0, 2.5)
    ax.set_ylim(-0.5, max(3, len(items)))  # Show at least 3 slots, expand if needed
    ax.axis('off')

    # Dynamically adjust element size based on stack length
    base_height = 0.6
    base_font = 18
    base_rect_width = 1.7
    base_rect_x = .95  # Moved further right
    base_top_font = 14
    base_lw = 1.5
    min_height = 0.18
    min_font = 8
    base_rect_width = .5  
    min_rect_width = 0.45 
    min_rect_x = 0.9   # Moved further right
    min_top_font = 7
    min_lw = 0.5
    n = max(len(items), 1)
    # Shrink height more slowly as stack grows
    height_scale = min(1, 6.0 / (n + 3))
    other_scale = min(1, 3.0 / n)
    rect_height = max(base_height * height_scale, min_height)
    font_size = max(int(base_font * other_scale), min_font)
    rect_width = max(base_rect_width * other_scale, min_rect_width)
    rect_x = max(base_rect_x * other_scale, min_rect_x)
    top_font_size = max(int(base_top_font * other_scale), min_top_font)
    lw = max(base_lw * other_scale, min_lw)

    for i, value in enumerate(items):
        y = i
        color = '#569CD6'
        rect = plt.Rectangle((rect_x, y), rect_width, rect_height, color=color, ec='black', lw=lw)
        ax.add_patch(rect)
        ax.text(rect_x + rect_width/2, y + rect_height/2 - rect_height*0.07, str(value), ha='center', va='center', fontsize=font_size, fontweight='bold', color='#1E1E1E')
        if i == len(items) - 1:
            ax.text(rect_x + rect_width + 0.2, y + rect_height/2, 'Top', va='center', fontsize=top_font_size, color='#1E1E1E', fontweight='bold', bbox=dict(facecolor='#B7E1F7', edgecolor='none', boxstyle='round,pad=0.24'))

    # If return_fig is True, return the figure instead of displaying it
    if return_fig:
        return fig
    st.pyplot(fig, use_container_width=False)
