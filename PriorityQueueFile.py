import math
from typing import List, TypeVar, Generic, Tuple

T = TypeVar("T")

show_debug_messages = False


class PriorityQueue (Generic[T]):
    Node = Tuple[int,T]
    def __init__(self, tree:List[Node]=[], isMinHeap:bool=True):
        self.my_tree:List["Node"] = []
        for n in tree:
            self.my_tree.append(n)
        self.is_min_heap = isMinHeap


    def node_at_index(self, index:int) -> Node:
        """
        gives the value stored in node at index
        :param index: location in the tree
        :return: value stored at that location
        postcondition: the tree is unchanged
        raises an indexError if we are out of bounds
        """
        if self.in_bounds(index):
            return self.my_tree[index]
        raise IndexError("Index {0} is out of bounds for tree of size {1}".format(index, len(self)))

    def set_node_at_index(self, in_node:Node, index:int):
        """
        changes the node at index to in_node and returns the old node.
        :param in_node: the new node to be stored in this location.
        :param index: location in the tree
        :return: node previously stored at that location
        postcondition: the shape of the tree is unchanged, though content may be changed.
        raises an indexError if we are out of bounds
        """
        if self.in_bounds(index):
            old_node = self.my_tree[index]
            self.my_tree[index] = in_node
            return old_node
        raise IndexError("Index {0} is out of bounds for tree of size {1}".format(index, len(self)))

    def left_child_of_index(self, index:int) -> int:
        """
        gives the index of the tree that is directly below and to the left of the given index.
        Note: the index may be out of bounds.
        :param index:
        :return index of left child of node at index
        """
        return 2 * index + 1

    def right_child_of_index(self, index:int )->int:
        """
        gives the index of the tree that is directly below and to the right of the given index.
        Note: the index may be out of bounds.
        :param index:
        :return index of right child of node at index
        """
        return 2 * index + 2

    def parent_of_index(self, index:int)->int:
        """
        gives the index of the tree that is the parent of the given index
        :param index:
        :return index above the given node index:
        """
        return int((index - 1) / 2)  # yay, integer math!

    def __len__(self):
        return len(self.my_tree)

    def in_bounds(self, index:int)->bool:
        """
        indicates whether index is within the size of this tree
        :param index:
        :return:
        """
        return index >= 0 and index < len(self)

    def has_left_child(self, index:int) -> bool:
        """
        indicates whether the node at this index has a child to the left
        :param index:
        :return boolean:
        """
        return self.in_bounds(self.left_child_of_index(index))

    def has_right_child(self, index:int) -> bool:
        """
        indicates whether the node at this index has a child to the right
        :param index:
        :return boolean:
        """
        return self.in_bounds(self.right_child_of_index(index))

    def a_has_priority_over_b(self, a:Node, b:Node)->bool:
        """
        Determines whether the node "a" has priority over node "b." This is determined by the priorities of "a" and "b" and
        by self.is_min_heap - i.e, should the higher node prevail, or the lower node?
        If the values are equal, then we _do not_ say that the "a" node has priority.
        """
        if self.is_min_heap:
            return a[0] < b[0]
        return a[0] > b[0]

    def is_empty(self)->bool:
        return len(self) == 0

    def __str__(self):
        """
        Draws a string representation of this tree, without changing it.
        ( you are welcome to examine this code, but you are not responsible for it.)
        :return:
        """
        spaces_per_item = 2 ** ((int)(
            math.log(len(self)) / math.log(2)) + 2)  # sneaky code to make the tree only as wide as needed.
        result = "-" * (spaces_per_item * 2)
        result += "\n"
        items_per_row = 1
        items_in_current_row = 0
        for item in self.my_tree:
            block = "{0}:{1}".format(item[0], item[1])
            result += "{0}{1}{0}".format(" " * int(spaces_per_item - (len(block)) / 2), block)
            items_in_current_row += 1
            if items_in_current_row == items_per_row:
                items_in_current_row = 0
                items_per_row *= 2
                spaces_per_item /= 2
                result += "\n"
        return result

    def __repr__(self):
        return self.__str__()

    def to_color_string(self, indices_to_color:List[int]=[]):
        """
        Draws a string representation of this tree, without changing it. For all items in the indices list,
        they will show up in a different color.
        This is essentially the same as __str__, but fancy!
        ( you are welcome to examine this code, but you are not responsible for it.)
        :return:
        """
        starters = ["\u001b[31m","\u001b[32m","\u001b[33m","\u001b[34m","\u001b[35m","\u001b[36m"]
        reset = "\u001b[0m"



        spaces_per_item = 2 ** ((int)(
            math.log(len(self)) / math.log(2)) + 2)  # sneaky code to make the tree only as wide as needed.
        result = "-" * (spaces_per_item * 2)
        result += "\n"
        items_per_row = 1
        items_in_current_row = 0
        counter = 0
        for item in self.my_tree:
            block = f"{item[0]}:{item[1]}"
            num_spaces = int(spaces_per_item - (len(block)) / 2)
            if counter in indices_to_color:
                col_num = indices_to_color.index(counter)%len(starters)
                result += starters[col_num]
                result += f"{' ' * num_spaces}{block}{' ' * num_spaces}"
                result += reset
            else:
                result += f"{' ' * num_spaces}{block}{' ' * num_spaces}"

            items_in_current_row += 1
            if items_in_current_row == items_per_row:
                items_in_current_row = 0
                items_per_row *= 2
                spaces_per_item /= 2
                result += "\n"
            counter+=1
        return result

    def clear(self):
        """
        removes all items from this priority queue.
        :return None:
        """
        self.my_tree = []

    def is_a_heap(self)->bool:
        """
        checks whether the self.my_tree variable holds a representation that is a heap. Any tree is considered a heap
        until you find a child that has greater priority than its parent.
        :return whether _all_ nodes are in a heap-like relationship with parents and children:
        """
        index = 0
        while self.in_bounds(index):
            if self.has_left_child(index):
                if self.a_has_priority_over_b(self.my_tree[self.left_child_of_index(index)],self.my_tree[index]):
                    return False
            if self.has_right_child(index):
                if self.a_has_priority_over_b(self.my_tree[self.right_child_of_index(index)],self.my_tree[index]):
                    return False
            index += 1
        if (show_debug_messages):
            print("This is a heap.")
        return True

    def add_value(self, value:T, priority:int=1):
        """
        adds a node to this data structure and makes sure that the my_tree data structure is
        still a heap.
        :param value: the value to store
        :param priority: its relative weight
        :return None:
        """
        if (show_debug_messages):
            print("-" * 128)
            print(f"Adding: [{priority = }, {value = }]")
        self.my_tree.append([priority, value])  # makes a new, 2-element list and adds it to the main array.
        self.heapify_up(len(self) - 1)
        if (show_debug_messages):
            print(self)

    def heapify_up(self, index:int):
        """
        given the index, potentially swaps itself with its parent, and onward up the tree
        as needed to make this a heap.
        precondition: The node at index is the only one in my_tree that is un-heaplike
        :param index:
        :return None:
        """
        while self.a_has_priority_over_b(self.my_tree[index],self.my_tree[self.parent_of_index(index)]):
            p = self.my_tree[self.parent_of_index(index)]
            self.my_tree[self.parent_of_index(index)] = self.my_tree[index]
            self.my_tree[index]=p
            index = self.parent_of_index(index)
        # ----------------------
        # ----------------------

    def peek(self) -> Node:
        """
        Gives the node at the start of this Priority Queue without removing it.
        """
        if self.isEmpty():
            raise IndexError("Attempted to peek at an empty Queue.")
        return self.my_tree[0]

    def pop(self) -> Node:
        """
        Removes the node at the start of this Priority Queue and resets the Queue so that it is in order; then
        returns the removed node.
        """
        if self.is_empty():
            raise IndexError("Attempted to pop from an empty Queue.")
        result:"Node" = self.my_tree[0]
        self.my_tree[0] = self.my_tree[-1]
        del (self.my_tree[-1])
        if (show_debug_messages):
            print("*" * 128)
            print("Just popped {result}")
        self.heapify_down()
        if (show_debug_messages):
            print(self)
        return result

    def heapify_down(self, index:int=0):
        """
        The node at index is possibly too high in the tree; we compare it to its children and potentially swap
        it with one of them to put it in better order, and repeat with the node in its new location.
        precondition: the tree is a heap, except possibly for the node at "index."
        postcondition: the tree is once again a heap
        """
        if not self.in_bounds(index):
            return
        current_index = index
        left_index:int = self.left_child_of_index(index)
        right_index:int = self.right_child_of_index(index)
        breaker:bool = False
        if self.in_bounds(left_index):
            wrongB = False
            wrongA = self.a_has_priority_over_b(self.my_tree[left_index], self.my_tree[current_index])
            if self.in_bounds(right_index):
                wrongB = self.a_has_priority_over_b(self.my_tree[right_index], self.my_tree[current_index])
            if wrongB and wrongA:
                if self.a_has_priority_over_b(self.my_tree[right_index],self.my_tree[left_index]):
                    new_index = right_index
                else:
                    new_index = left_index
            elif wrongA:
                new_index = left_index
            elif wrongB:
                new_index = right_index
            else:
                return
            n = self.my_tree[current_index]
            self.set_node_at_index(self.my_tree[new_index], current_index)
            self.set_node_at_index(n, new_index)
            self.heapify_down(new_index)
        else:
            return

