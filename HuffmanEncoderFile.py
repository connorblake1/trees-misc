from PriorityQueueFile import PriorityQueue
from TreeNodesFile import *
from typing import Dict, List

class HuffmanEncoder():
    def __init__(self, stringToEncode=""):
        self.encode_string = stringToEncode
        self.encode_dictionary:Dict[str,List[int]] = {}

    def do_setup(self):
        self.build_frequency_dictionary()
        self.build_priority_queue()
        self.build_tree()
        self.build_encode_dictionary_with_tree(self.encoding_tree)

    def build_frequency_dictionary(self):
        """
        construct a dictionary, self.freq_dict, where the various single-character strings found in the encode_string are the
        keys, and the number of times they appear are the values.
        For instance, "red beret" would lead to a dictionary {"r":2, "e":3, "d":1, " ":1, "b":1, "t":1}
        """
        self.freq_dict:Dict[str,int] = {}
        for character in self.encode_string:
            if character in self.freq_dict:
                self.freq_dict[character] += 1
            else:
                self.freq_dict[character] = 1

            ## ----------------------------------------

    def build_priority_queue(self):
        """
        create a min-heap priority queue of TreeNodes (called self.frequencyQueue) out of the data in self.freqDict.
        Your priorityQueue will have priority of the count of the letters, and the values will be brand-new LeafNodes,
        with the character as the value in the node.
        (That is, you'll need to make a new LeafNode[str] for each item in self.freq_dict and add it to the PQ.)

        """
        print(self.encode_string)
        self.frequency_queue:PriorityQueue[TreeNode[str]] = PriorityQueue[TreeNode[T]] (isMinHeap=True)
        # ----------------------
        for letter in self.freq_dict.keys():
            n:LeafNode[str] = LeafNode[str](letter)
            self.frequency_queue.add_value(n, self.freq_dict[letter])
        print(self.frequency_queue)

        # ----------------------

    def build_tree(self):
        """
        Use the priority queue (self.frequencyQueue) to generate a Huffman Encoding tree for this string.
        (We are using the queue to make the most efficient tree for this string, so that frequently used characters
        appear higher in the tree.) This will radically change the PQ in the process. Here is the algorithm for doing this:
            • Pop *two* PQ nodes (priority, TreeNode[str]) off the priority queue. These are the two lowest-frequency nodes on the tree.
            • Create a new JointNode with these two tree nodes. (1st -> left; 2nd -> right)
            • Add the new JointNode back into the priority queue, with a new priority that is the sum of the previous two.
            • Repeat until you cannot pop two nodes - that is, until there are no more pairs to combine!
            • The one PQ node left in the queue will hold your new tree, which you should store in the variable self.encodingTree.
        Note: I've written the last step for you... so don't reinvent it.
        """
        # ----------------------

        # suggestion: each time through your loop, print out the
        # priority queue to help you debug.
        while len(self.frequency_queue) >= 2:
            l1:TreeNode[T] = self.frequency_queue.pop()
            l2:TreeNode[T] = self.frequency_queue.pop()
            j1:JointNode[T] = JointNode[T](l1[1],l2[1])
            self.frequency_queue.add_value(j1,l1[0]+l2[0])

        # ----------------------

        last_PQ_Node = self.frequency_queue.pop()
        self.encoding_tree:TreeNode[str] = last_PQ_Node[1]

    def build_encode_dictionary_with_tree(self, root:TreeNode[str]=None, pathSoFar:List[int]=[]):
        """
        Generates a lookup table based on the given tree, producing a dictionary of characters --> 0/1 code sequences.
        (A recursive method)
        :param root: the root of the tree or subtree to add to dictionary.
        :param pathSoFar: the path (a list of 0s and 1s) that got us to this root.
        :return: None
        Note: this is building self.encode_dictionary, a dictionary {str -> list of 0s and 1s} that was initialized
        in __init__().
        """
        # I've written this one for you.
        if root is None:
            root = self.encoding_tree  # ok to do, because we would only go left or right recursively if there is a left
                                        # and right, so this must be the real root node.

        if isinstance(root,JointNode): #is this node a joint node?
            left_list = pathSoFar[:]  # makes a copy
            left_list.append(0)
            self.build_encode_dictionary_with_tree(root.left, left_list)
            right_list = pathSoFar[:]  # makes a copy
            right_list.append(1)
            self.build_encode_dictionary_with_tree(root.right, right_list)

        else:  #then this must be a leaf node.... Note that this is the only time we actually add anything to the dictionary.
            self.encode_dictionary[root.value] = pathSoFar
            print(" ")
            print(root.value)
            print(pathSoFar)

    def encode_message(self, messageToEncode:str) -> List[int]:
        """
        Use the self.encodingDictionary to convert each letter into a sequence of 1's and 0's (bits),
        and generate a (very) long array of bits, which you should return.
        :param messageToEncode: a string, all of whose characters should be contained in the encoding tree.
        :return: a (very long) list of ones and zeros.
        """
        encoded_result:List[int] = []
        # ----------------------
        i=0
        for char in messageToEncode:
            # print(char)
            # print(type(encoded_result))
            # print(type(self.encode_dictionary[char]))
            encoded_result.extend(self.encode_dictionary[char])
            # print(encoded_result)
            i+=1
            # if there is a problem, you should throw the following.
            #raise new KeyError(f"The letter \'{char}\' was not contained in the key string.")
        return encoded_result

    def decode_message(self, messageToDecode:List[int])-> str:
        """
        :param messageToDecode:
        :return:
        """
        decoded_result = ""
        p = self.encoding_tree
        p.print_tree()
        index = 0
        while index < len(messageToDecode):
            while isinstance(p, JointNode):
                if messageToDecode[index] == 0:
                    p = p.left
                else:
                    p = p.right
                index+=1
            decoded_result+=p.value
            p = self.encoding_tree

        # ----------------------

        return decoded_result
