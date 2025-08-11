import streamlit as st
import matplotlib.pyplot as plt
from data_structures.tree import TreeNode
from data_structures.avl_tree import AVLTree  # Import AVLTree class

# Helper functions

def tree_height(node):
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))

def draw_node(node, x, y, dx, highlight_list, ax, level=0, max_width=0, edge_positions=None):
    if node:
        color = '#FFD700' if node.value in highlight_list else "#7EC28D"
        size = 14 if node.value in highlight_list else 12
        ax.text(x, y, str(node.value), bbox=dict(facecolor=color, edgecolor='black'), ha='center', va='center', fontsize=size, fontweight='bold', zorder=4)

        # Track edge positions for dynamic axis limits
        if edge_positions is not None:
            edge_positions.append((x, y))

        next_dx = dx / (2 ** level) if max_width > 0 else dx / 2

        if node.left:
            ax.plot([x, x-next_dx], [y, y-1], 'k-', lw=3, alpha=0.7, zorder=1)
            if edge_positions is not None:
                edge_positions.append((x-next_dx, y-1))
            draw_node(node.left, x-next_dx, y-1, dx, highlight_list, ax, level + 1, max_width, edge_positions)
        if node.right:
            ax.plot([x, x+next_dx], [y, y-1], 'k-', lw=3, alpha=0.7, zorder=1)
            if edge_positions is not None:
                edge_positions.append((x+next_dx, y-1))
            draw_node(node.right, x+next_dx, y-1, dx, highlight_list, ax, level + 1, max_width, edge_positions)

# Tree insertion functions

def insert_bst(root, value):
    if not root:
        return TreeNode(value)
    if str(value) < str(root.value):
        root.left = insert_bst(root.left, value)
    else:
        root.right = insert_bst(root.right, value)
    return root

def insert_avl(root, value, avl_tree):
    return avl_tree.insert(root, value)  # Use AVLTree's insert method

# Traversal functions

def traverse_tree(node, traversal, parent=None):
    frames = []
    explanations = []
    import copy

    if traversal == "Pre-order":
        def pre_order(n, parent):
            if n:
                highlight = [n.value]
                if parent:
                    explanations.append(f"Pre-order: Visit {n.value} (child of {parent.value})")
                else:
                    explanations.append(f"Pre-order: Visit root {n.value}")
                frames.append((copy.deepcopy(node), explanations[-1], highlight))
                pre_order(n.left, n)
                pre_order(n.right, n)
        pre_order(node, parent)

    elif traversal == "In-order":
        def in_order(n, parent):
            if n:
                in_order(n.left, n)
                highlight = [n.value]
                if parent:
                    explanations.append(f"In-order: Visit {n.value} (child of {parent.value})")
                else:
                    explanations.append(f"In-order: Visit root {n.value}")
                frames.append((copy.deepcopy(node), explanations[-1], highlight))
                in_order(n.right, n)
        in_order(node, parent)

    elif traversal == "Post-order":
        def post_order(n, parent):
            if n:
                post_order(n.left, n)
                post_order(n.right, n)
                highlight = [n.value]
                if parent:
                    explanations.append(f"Post-order: Visit {n.value} (child of {parent.value})")
                else:
                    explanations.append(f"Post-order: Visit root {n.value}")
                frames.append((copy.deepcopy(node), explanations[-1], highlight))
        post_order(node, parent)

    return frames, explanations

def find_insertion(prev, curr):
    # Returns (inserted_value, parent_value, direction) or (None, None, None)
    if not prev:
        return (curr.value, None, None)
    stack = [(prev, curr, None)]
    while stack:
        prev_node, curr_node, parent = stack.pop()
        if not prev_node and curr_node:
            # New node inserted
            return (curr_node.value, parent.value if parent else None, 'left' if parent and parent.left == curr_node else 'right')
        if prev_node and curr_node:
            stack.append((prev_node.left, curr_node.left, curr_node))
            stack.append((prev_node.right, curr_node.right, curr_node))
    return (None, None, None)

# Streamlit UI

def visualize_tree():
    st.header("Trees 🌳")
    st.markdown("""
    If you can picture a family tree, you'll recognize the hierarchical structure of a tree.

    A ***node*** (🟢) represents an individual element in the tree, connected by edges (➖).
    First you'll notice the topmost node called the ***root***, which acts as the ***parent***, while the nodes directly below it are its ***children***.
    Each node can have up to two children; if a node has no children, it is called a ***leaf***.
    Trees are commonly used for organizing data, as well as for searching and sorting.
                
    #### Binary Search Tree (BST)
    - The first value becomes the root.
    - For each new value, start at the root and compare it to the nodes:
        - Go left if the value is less than the current node (parent).
        - Go right if the value is greater than or equal to the current node (parent).
    - This process repeats until the value finds its correct spot.

    #### AVL Tree
    AVL Trees are a type of self-balancing BST. After each insertion, rotations are performed to ensure the tree remains balanced, meaning the height difference between the left and right subtrees of any node is at most one.

    #### Experimentation
    Branch out and try both types! :)
    """)

    # User input section
    tree_type = st.selectbox("Choose tree type:", ["Binary Search Tree (BST)", "AVL Tree"], index=0)

    # Ensure both text boxes are always synchronized
    if "tree_node_values" not in st.session_state:
        st.session_state.tree_node_values = "5,3,7,2,4,6,8"

    # Main input for building tree
    user_input = st.text_input("Enter tree node values (numeric comma-separated):", value=st.session_state.tree_node_values, key="tree_node_input")
    st.session_state.tree_node_values = user_input

    # Use st.session_state.tree_node_values everywhere for values
    values = [int(v.strip()) for v in st.session_state.tree_node_values.split(",") if v.strip()]

    # Initialize tree and AVLTree instance
    tree_root = None
    avl_tree = AVLTree()

    # Build tree from user input
    frames = []
    explanations = []
    prev_tree = None
    for i, v in enumerate(values):
        if tree_type == "Binary Search Tree (BST)":
            tree_root = insert_bst(prev_tree, v)
        else:
            tree_root = insert_avl(prev_tree, v, avl_tree)
        import copy
        frames.append((copy.deepcopy(tree_root), None, [v]))
        prev_tree = copy.deepcopy(tree_root)

    # Generate explanations by analyzing frames
    for i, (frame, _, highlight) in enumerate(frames):
        if i == 0:
            explanations.append(f"🌱 Insert root node {highlight[0]}.")
        else:
            prev_frame = frames[i-1][0]
            inserted, parent, direction = find_insertion(prev_frame, frame)
            if parent is None:
                explanations.append(f"🌱 Insert node {inserted}: direct child of root.")
            else:
                comparison = '<' if direction == 'left' else '>='
                explanations.append(f"🌱 Insert node {inserted}: Go {direction} from {parent} since {inserted} {comparison} {parent}.")
        frames[i] = (frame, explanations[-1], highlight)

    # Only allow one animation (grow or traverse) at a time
    if "active_animation" not in st.session_state:
        st.session_state.active_animation = None

    st.markdown("### 'Grow' your Tree:")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        play_tree_animation = st.button("🎬 Grow", disabled=st.session_state.active_animation == "traverse")

    if play_tree_animation and st.session_state.active_animation is None:
        st.session_state.active_animation = "grow"
        st.session_state.show_keyframes = False  # Reset to animation mode
        st.session_state.tree_animation_frames = frames
        st.session_state.tree_current_frame = 0
        placeholder = st.empty()
        for i, (frame, description, highlighted) in enumerate(frames):
            with placeholder.container():
                st.write(f"**Tree Height:** {tree_height(frame) - 1}")
                st.write(f"**Step {i+1}/{len(frames)}:** {description}")
                fig, ax = plt.subplots(figsize=(8, 6))
                max_height = tree_height(frame)
                max_width = 2 ** max_height
                ax.set_xlim(-max_width * 1.2, max_width * 1.2)
                ax.set_ylim(-max_height-1, 1)
                ax.axis('off')
                ax.set_facecolor('#F0F8FF')
                edge_positions = []
                draw_node(frame, 0, 0, max_width, highlighted, ax, max_width=max_width, edge_positions=edge_positions)
                if edge_positions:
                    x_positions, y_positions = zip(*edge_positions)
                    ax.set_xlim(min(x_positions) - 1, max(x_positions) + 1)
                    ax.set_ylim(min(y_positions) - 1, max(y_positions) + 1)
                fig.patch.set_facecolor('white')
                fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
                st.pyplot(fig)
                plt.close(fig)
            import time, gc
            time.sleep(1.2)
            gc.collect()  # Explicitly free memory
        placeholder.empty()
        st.session_state.show_keyframes = True
        st.session_state.active_animation = None

    if st.session_state.get("show_keyframes", False) and st.session_state.active_animation is None:
        if "tree_animation_frames" not in st.session_state:
            st.session_state.tree_animation_frames = frames
        if "tree_current_frame" not in st.session_state:
            st.session_state.tree_current_frame = 0
        st.markdown("---")
        total_steps = len(st.session_state.tree_animation_frames)
        col1, col2, _ = st.columns([1, 1, 6])
        with col1:
            if st.button("Prev", key="tree_prev_button"):
                st.session_state.tree_current_frame = max(0, st.session_state.tree_current_frame - 1)
        with col2:
            if st.button("Next", key="tree_next_button"):
                st.session_state.tree_current_frame = min(total_steps - 1, st.session_state.tree_current_frame + 1)
        selected_step = st.slider(
            label="",
            min_value=1,
            max_value=total_steps,
            value=st.session_state.tree_current_frame + 1,
            step=1,
            format="Step %d"
        )
        st.session_state.tree_current_frame = selected_step - 1
        frame, description, highlighted = st.session_state.tree_animation_frames[st.session_state.tree_current_frame]
        st.write(f"**Step {st.session_state.tree_current_frame+1}/{total_steps}:** {description}")
        fig, ax = plt.subplots(figsize=(8, 6))
        max_height = tree_height(frame)
        max_width = 2 ** max_height
        ax.set_xlim(-max_width * 1.2, max_width * 1.2)
        ax.set_ylim(-max_height-1, 1)
        ax.axis('off')
        ax.set_facecolor('#F0F8FF')
        edge_positions = []
        draw_node(frame, 0, 0, max_width, highlighted, ax, max_width=max_width, edge_positions=edge_positions)
        if edge_positions:
            x_positions, y_positions = zip(*edge_positions)
            ax.set_xlim(min(x_positions) - 1, max(x_positions) + 1)
            ax.set_ylim(min(y_positions) - 1, max(y_positions) + 1)
        fig.patch.set_facecolor('white')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        st.pyplot(fig)
        plt.close(fig)

    # Add description for tree traversals
    st.markdown(
        """
        ### Tree Traversals
        Traversals are methods to visit all nodes in a tree systematically. They are crucial for various operations like searching, sorting, and modifying trees.

        **In-Order Traversal**: 
        - Visit the left subtree, then the node, and finally the right subtree.
        - ***Example***: For an AVL Tree [2,1,3,4], the traversal order is **1, 2, 3, 4**.
            - Produces nodes in sorted order for Binary Search Trees.

        **Pre-Order Traversal**: 
        - Visit the node first, then the left subtree, and finally the right subtree.
        - ***Example***: For an AVL Tree [2,1,3,4], the traversal order is **2, 1, 3, 4**.
            - Useful for creating a copy of the tree.

        **Post-Order Traversal**: 
        - Visit the left subtree, then the right subtree, and finally the node.
        - ***Example***: For an AVL Tree [2,1,3,4], the traversal order is **1, 4, 3, 2**.
            - Useful for deleting or freeing nodes in a tree.
        """
    )

    # Only allow one animation (grow or traverse) at a time
    if "show_traversal_keyframes" not in st.session_state:
        st.session_state.show_traversal_keyframes = False

    traversal_type = st.selectbox("Choose tree traversal:", ["Pre-order", "In-order", "Post-order"], index=0)
    st.session_state.traversal_type = traversal_type
    traversal_user_input = st.text_input("Update tree node values if needed (numeric comma-separated):", value=st.session_state.tree_node_values, key="traversal_tree_node_input")
    st.session_state.tree_node_values = traversal_user_input
    values = [int(v.strip()) for v in st.session_state.tree_node_values.split(",") if v.strip()]
    st.markdown(f"### Traverse your {tree_type}:")
    play_traversal_animation = st.button("🔄 Traverse", disabled=st.session_state.active_animation == "grow")

    if play_traversal_animation and st.session_state.active_animation is None:
        st.session_state.active_animation = "traverse"
        st.session_state.show_traversal_keyframes = False
        traversal_frames, traversal_explanations = traverse_tree(tree_root, traversal_type)
        st.session_state.traversal_animation_frames = traversal_frames
        st.session_state.traversal_current_frame = 0
        placeholder = st.empty()
        for i, (frame, description, highlighted) in enumerate(traversal_frames):
            with placeholder.container():
                fig, ax = plt.subplots(figsize=(8, 6))
                max_height = tree_height(frame)
                max_width = 2 ** max_height
                ax.set_xlim(-max_width * 1.2, max_width * 1.2)
                ax.set_ylim(-max_height-1, 1)
                ax.axis('off')
                ax.set_facecolor('#F0F8FF')
                edge_positions = []
                draw_node(frame, 0, 0, max_width, highlighted, ax, max_width=max_width, edge_positions=edge_positions)
                if edge_positions:
                    x_positions, y_positions = zip(*edge_positions)
                    ax.set_xlim(min(x_positions) - 1, max(x_positions) + 1)
                    ax.set_ylim(min(y_positions) - 1, max(y_positions) + 1)
                fig.patch.set_facecolor('white')
                fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
                st.pyplot(fig)
                plt.close(fig)
            import time, gc
            time.sleep(1.2)
            gc.collect()
        placeholder.empty()
        st.session_state.show_traversal_keyframes = True
        st.session_state.active_animation = None

    if st.session_state.get("show_traversal_keyframes", False) and st.session_state.active_animation is None:
        st.markdown("---")
        traversal_order = [str(frame[2][0]) for frame in st.session_state.traversal_animation_frames]
        total_steps = len(st.session_state.traversal_animation_frames)
        col1, col2, _ = st.columns([1, 1, 6])
        with col1:
            if st.button("Prev", key="traversal_prev_button"):
                st.session_state.traversal_current_frame = max(0, st.session_state.traversal_current_frame - 1)
        with col2:
            if st.button("Next", key="traversal_next_button"):
                st.session_state.traversal_current_frame = min(total_steps - 1, st.session_state.traversal_current_frame + 1)
        selected_step = st.slider(
            label="",
            min_value=1,
            max_value=total_steps,
            value=st.session_state.traversal_current_frame + 1,
            step=1,
            format="Step %d",
            key="traversal_slider"
        )
        st.session_state.traversal_current_frame = selected_step - 1
        frame, description, highlighted = st.session_state.traversal_animation_frames[st.session_state.traversal_current_frame]
        st.write(f"**Step {st.session_state.traversal_current_frame+1}/{total_steps}:** {description}")
        fig, ax = plt.subplots(figsize=(8, 6))
        max_height = tree_height(frame)
        max_width = 2 ** max_height
        ax.set_xlim(-max_width * 1.2, max_width * 1.2)
        ax.set_ylim(-max_height-1, 1)
        ax.axis('off')
        ax.set_facecolor('#F0F8FF')
        edge_positions = []
        draw_node(frame, 0, 0, max_width, highlighted, ax, max_width=max_width, edge_positions=edge_positions)
        if edge_positions:
            x_positions, y_positions = zip(*edge_positions)
            ax.set_xlim(min(x_positions) - 1, max(x_positions) + 1)
            ax.set_ylim(min(y_positions) - 1, max(y_positions) + 1)
        fig.patch.set_facecolor('white')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        st.pyplot(fig)
        plt.close(fig)