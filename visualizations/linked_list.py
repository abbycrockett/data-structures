import streamlit as st
import matplotlib.pyplot as plt
from data_structures.linked_list import LinkedList

def visualize_linked_list():
    st.markdown("# Linked List 🔗")
    st.markdown('''
    <div style="margin-top: 1.5em; margin-bottom: 1.5em;">
    A linked list is a chain of nodes, each one pointing to the next. 
    In the diagram below, <strong>node A</strong> points to the memory address of <strong>node B</strong>, which is <strong>3450</strong>. 
    The final node in the list always points to <strong>NULL</strong>.
    </div>
    ''', unsafe_allow_html=True)


    st.image("visualizations/linked-list.png")

    st.markdown('''
        <div style="margin-top: 1.5em; margin-bottom: 1.5em; line-height: 1.6;">
        Now that you understand how nodes are connected, here are some common operations you can perform on a linked list:
        <ul style="padding-left: 1.5em;">
        <li><strong>Search</strong>: Locate the value at a specific position (index).</li>
        <li><strong>Insert</strong>: Add a value at any position, not just at the end.</li>
        <li><strong>Delete</strong>: Remove a value from any position, not just the front.</li>
        </ul>
        Experiment with searching, inserting, or deleting values at any position below!
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("#### Search, Insert, or Delete at Nth Position")

    values_list = ['A', 'B', 'C']
    ll = LinkedList(values_list)
    canvas_placeholder = st.empty()
    st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)
    # Override Streamlit pink border for input widgets except when focused
    st.markdown("""
    <style>
    .st-da, .st-db, .st-dc, .st-d9 {
        border-color: var(--vscode-border) !important;
    }
    .st-da:focus, .st-db:focus, .st-dc:focus, .st-d9:focus {
        border-color: var(--vscode-pink) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Controls for search, insert, delete at nth position
    col_search, col_insert, col_delete = st.columns(3)
    ll_length = len(st.session_state.ll_state) if 'll_state' in st.session_state else len(ll.to_list())
    with col_search:
        search_value = st.text_input('Search value', '', key="ll_search_value")
        search_clicked = st.button('Search', key="ll_search_btn")
    with col_insert:
        insert_index = st.number_input('Insert at index', min_value=0, max_value=ll_length, step=1, value=0, key="ll_insert_index")
        insert_at_value = st.text_input('Value to insert', '', key="ll_insert_at_value")
        insert_at_clicked = st.button('Insert', key="ll_insert_at_btn")
    with col_delete:
        delete_index = st.number_input('Delete at index', min_value=0, max_value=max(ll_length-1,0), step=1, value=0, key="ll_delete_index")
        delete_at_clicked = st.button('Delete', key="ll_delete_at_btn")

    if 'll_state' not in st.session_state:
        st.session_state.ll_state = ll.to_list()

    highlight_index = None
    search_result = None
    # Search by value with animation
    if search_clicked and search_value:
        found_index = None
        for i, v in enumerate(st.session_state.ll_state):
            fig = draw_linked_list(LinkedList(st.session_state.ll_state), highlight_index=i, return_fig=True)
            canvas_placeholder.pyplot(fig, use_container_width=False, clear_figure=True)
            import time
            time.sleep(0.35)
            import matplotlib.pyplot as plt
            plt.close('all')
            if str(v) == str(search_value):
                found_index = i
                break
        if found_index is not None:
            st.success(f'Value "{search_value}" found at index {found_index}')
            highlight_index = found_index
        else:
            st.warning(f'Value "{search_value}" not found in the list.')
            highlight_index = None
    # Insert at nth position
    elif insert_at_clicked and insert_at_value:
        if insert_index < 0 or insert_index > len(st.session_state.ll_state):
            st.warning('Index out of range!')
        else:
            st.session_state.ll_state.insert(insert_index, insert_at_value)
            st.success(f'Inserted {insert_at_value} at index {insert_index}')
            highlight_index = insert_index
    # Delete at nth position
    elif delete_at_clicked:
        if delete_index < 0 or delete_index >= len(st.session_state.ll_state):
            st.warning('Index out of range!')
        else:
            removed = st.session_state.ll_state.pop(delete_index)
            st.success(f'Deleted {removed} at index {delete_index}')
            highlight_index = delete_index

    ll = LinkedList(st.session_state.ll_state)
    fig = draw_linked_list(ll, highlight_index=highlight_index, return_fig=True)
    canvas_placeholder.pyplot(fig, use_container_width=False, clear_figure=True)
    import matplotlib.pyplot as plt
    plt.close('all')

def draw_linked_list(ll, highlight_index=None, return_fig=False):
    items = ll.to_list()
    min_width = 3.5
    fig_width = max(len(items) * 0.95 + 0.7, min_width)
    fig, ax = plt.subplots(figsize=(fig_width, 1.6))
    fig.patch.set_facecolor("#1E1E1E")
    ax.set_xlim(-0.5, max(2.5, len(items) - 0.1))
    ax.set_ylim(0, 1.6)
    ax.axis('off')

    base_radius = 0.23
    base_font = 11
    base_lw = 1.1
    min_radius = 0.13
    min_font = 7
    min_lw = 0.5
    n = max(len(items), 1)
    radius_scale = min(1, 3.0 / (n + 2))
    other_scale = min(1, 2.0 / n)
    radius = max(base_radius * radius_scale, min_radius)
    font_size = max(int(base_font * other_scale), min_font)
    lw = max(base_lw * other_scale, min_lw)

    y = 0.8
    for i, value in enumerate(items):
        x = i * 0.95 + 0.35
        # Highlight selected index
        if highlight_index is not None and i == highlight_index:
            color = '#FFC107'  # Yellow highlight
            edgecolor = '#1E1E1E'
            lw_highlight = lw + 1.2
        else:
            color = "#569CD6"  # Color for linked list nodes
            edgecolor = 'black'
            lw_highlight = lw
        circle = plt.Circle((x, y), radius, color=color, ec=edgecolor, lw=lw_highlight, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(value), ha='center', va='center', fontsize=font_size, fontweight='bold', color='#1E1E1E', zorder=3)
        # Draw arrow line to next node
        if i < len(items) - 1:
            start_x = x + radius
            end_x = (i + 1) * 0.95 + 0.35 - radius
            ax.annotate('', xy=(end_x, y), xytext=(start_x, y),
                        arrowprops=dict(arrowstyle="->", color="#D4D4D4", lw=lw, shrinkA=0, shrinkB=0), zorder=1)
        # Head and Tail labels
        if i == 0:
            ax.text(x, y + radius + 0.18, 'Head', ha='center', va='center', fontsize=max(int(font_size*0.9), 7), color='#1E1E1E', fontweight='bold', bbox=dict(facecolor='#B7E1F7', edgecolor='none', boxstyle='round,pad=0.18'))
        if i == len(items) - 1:
            ax.text(x, y - radius - 0.18, 'Tail', ha='center', va='center', fontsize=max(int(font_size*0.9), 7), color='#1E1E1E', fontweight='bold', bbox=dict(facecolor='#B7E1F7', edgecolor='none', boxstyle='round,pad=0.18'))

    if return_fig:
        return fig
    st.pyplot(fig, use_container_width=False)