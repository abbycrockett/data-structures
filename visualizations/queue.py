import streamlit as st
import matplotlib.pyplot as plt
from data_structures.queue import Queue

def visualize_queue():
    st.markdown("# Queue 👥")
    st.markdown('''
        <div style="margin-top: 1.5em; margin-bottom: 1.5em;">
        A queue works like a line of people waiting: you can only join (<strong>enqueue</strong>) the line at the back and leave (<strong>dequeue</strong>) the line from the front.
        This is the principle of <strong>FIFO</strong>: First In, First Out.
        <br><br>
        For example, if you add items in the order <strong>A, B, C</strong>, see which comes off first!
        </div>
        ''', unsafe_allow_html=True)

    values_list = ['A', 'B', 'C']
    queue = Queue(values_list)
    canvas_placeholder = st.empty()
    st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)

    col_dequeue, col_enqueue, col_input = st.columns([0.2, 0.2, 1])
    with col_enqueue:
        enqueue_clicked = st.button('Enqueue ⬅️', key="queue_enqueue")
    with col_dequeue:
        dequeue_clicked = st.button('Dequeue ❌', key="queue_dequeue")
    with col_input:
        insert_value = st.text_input('Value to enqueue (single character pls):', '', key="queue_insert_value")

    if 'queue_state' not in st.session_state:
        st.session_state.queue_state = queue.to_list()

    if enqueue_clicked and insert_value:
        st.session_state.queue_state.append(insert_value)
        st.success(f'Enqueued: {insert_value}')
        st.rerun()
    elif dequeue_clicked:
        if not st.session_state.queue_state:
            st.warning('Queue is empty!')
        else:
            dequeued = st.session_state.queue_state.pop(0)
            st.success(f'Dequeued: {dequeued}')

    queue = Queue(st.session_state.queue_state)
    fig = draw_queue(queue, return_fig=True)
    canvas_placeholder.pyplot(fig, use_container_width=False, clear_figure=True)

def draw_queue(queue, highlight_index=None, return_fig=False):
    items = queue.to_list()
    min_width = 5 # Set a minimum width for the figure
    fig_width = max(len(items) * 1.5, min_width)  # Ensure the width never goes below the minimum
    fig, ax = plt.subplots(figsize=(fig_width, 2.5))  # Adjust width based on queue length
    fig.patch.set_facecolor("#151C15")
    ax.set_xlim(-0.5, max(3, len(items))) 
    ax.set_ylim(0, 3) 
    ax.axis('off')

    base_width = 0.6
    base_font = 18
    base_rect_height = 1.7
    base_rect_y = 0.2  
    base_top_font = 14
    base_lw = 1.5
    min_width = 0.18
    min_font = 8
    min_rect_height = 0.45
    min_rect_y = 0.1 
    min_top_font = 7
    min_lw = 0.5
    n = max(len(items), 1)
    width_scale = min(1, 6.0 / (n + 3))
    other_scale = min(1, 3.0 / n)
    rect_width = max(base_width * width_scale, min_width)
    font_size = max(int(base_font * other_scale), min_font)
    rect_height = max(base_rect_height * other_scale, min_rect_height)
    rect_y = max(base_rect_y * other_scale, min_rect_y)
    top_font_size = max(int(base_top_font * other_scale), min_top_font)
    lw = max(base_lw * other_scale, min_lw)

    for i, value in enumerate(items):
        x = i
        color = '#569CD6'
        rect = plt.Rectangle((x, rect_y), rect_width, rect_height, color=color, ec='black', lw=lw)
        ax.add_patch(rect)
        ax.text(x + rect_width/2, rect_y + rect_height/2 - rect_height*0.07, str(value), ha='center', va='center', fontsize=font_size, fontweight='bold', color='#1E1E1E')
        if i == 0:
            label = 'Head' if len(items) == 1 else 'Head'
            ax.text(x + rect_width/2, rect_y + rect_height + 0.6, label, ha='center', va='center', fontsize=top_font_size, color='#1E1E1E', fontweight='bold', bbox=dict(facecolor='#B7E1F7', edgecolor='none', boxstyle='round,pad=0.24'))
        if i == len(items) - 1 and len(items) > 1:
            ax.text(x + rect_width/2, rect_y + rect_height + 0.6, 'Tail', ha='center', va='center', fontsize=top_font_size, color='#1E1E1E', fontweight='bold', bbox=dict(facecolor='#B7E1F7', edgecolor='none', boxstyle='round,pad=0.24'))

    if return_fig:
        return fig
    st.pyplot(fig, use_container_width=False)