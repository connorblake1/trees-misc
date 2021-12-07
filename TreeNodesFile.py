from typing import Generic, TypeVar

T = TypeVar("T")


class TreeNode(Generic[T]):
    def __init__(self, value: T = None, left: "TreeNode[T]" = None, right: "TreeNode[T]" = None):
        self.value = value
        self.left = left
        self.right = right

    def has_left(self) -> bool:
        return self.left is not None

    def has_right(self) -> bool:
        return self.right is not None

    def print_tree(self, indentation_level:int =0):
        """
            used to visualize this tree - not implemented in TreeNode
        """
        pass


# ---------------------------------------------------------------------------
class LeafNode(TreeNode[T]):
    def __init__(self, value:T=None):
        super().__init__(value=value, left=None, right=None)

    def has_left(self) -> bool:
        return False

    def has_right(self) -> bool:
        return False

    def __str__(self):
        """ this is like toString() in java, when the user wants to print this node."""
        if self.value == '\n':
            return f"[\\n]"
        return f"[{self.value}]"

    def __repr__(self):
        """ this is like toString() in java, when the user is printing a bunch of these
        objects inside another data structure. We'll need both versions."""
        if self.value == '\n':
            return f"[\\n]"
        return f"[{self.value}]"

    def print_tree(self, indentation_level=0):
        """
            used to visualize this tree - not implemented in TreeNode
        """
        print(f"{' ' * (4 * indentation_level)}{self}")


# ---------------------------------------------------------------------------
class JointNode(TreeNode[T]):
    def __init__(self, left:"TreeNode[T]", right:"TreeNode[T]"):
        super().__init__(None, left, right)
        if left is None or right is None:
            raise RuntimeError(
                f"Tried to create a JointNode that didn't have both children. {left =}, {right = }")

    def __str__(self):
        result = ""
        if self.has_left():
            result += self.left.__str__()
        if self.has_right():
            result += self.right.__str__()
        return result

    def __repr__(self):
        result = ""
        if self.has_left():
            result += self.getLeft().__repr__()
        if self.has_right():
            result += self.getRight().__repr__()
        return result;

    def print_tree(self, indentation_level:int=0):
        """
            used to visualize this tree - not implemented in TreeNode
        """
        if self.has_left():
            self.left.print_tree(indentation_level + 1)
        print(f"{' ' * (4 * indentation_level)}",end="<\n")
        if self.has_right():
            self.right.print_tree(indentation_level + 1)
