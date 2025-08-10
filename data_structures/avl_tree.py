class AVLTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 # Height is needed to calculate the balance factor

class AVLTree:
    def insert(self, root, value):
        # 1. Base case: If the tree is empty, return a new node
        if not root:
            return AVLTreeNode(value)

        # 2. Recursive case: Insert the value into the appropriate subtree
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        # 3. Update the height of the ancestor node
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # 4. Get the balance factor
        balance = self.get_balance(root)

        # 5. Rebalancing
        # * If the balance factor is outside the range [-1, 1], then the tree is unbalanced.
        #   - A balance factor of 0 means the left and right subtrees are of equal height.
        #   - A balance factor of 1 means the left subtree is taller by 1 level.
        #   - A balance factor of -1 means the right subtree is taller by 1 level.
        #   - So, if left and right subtree both have the height of 3 then 3-3=0. This means they are balanced.

        # Left Left Case
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        # Return the new root
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        # Return the new root
        return y

    # Returns the height of a node. If the node is None, the height is 0.
    def get_height(self, node): 
        if not node:
            return 0
        return node.height

    # Returns the balance factor of a node. If the node is None, the balance factor is 0.
    # Balance factor = height of left subtree - height of right subtree.
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
