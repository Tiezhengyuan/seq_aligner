

class SuffixTrieNode:
    def __init__(self, val:str=None):
        self.val = val if val else ''
        # parent node
        self.parent = None
        # nodes list
        self.children = []
        # positions of suffix
        self.position = []

    @property
    def is_root(self):
        return True if self.val == '' else False

    @property
    def is_leave(self):
        return True if self.val == '$' else False
    
    def child_path(self, new_val):
        for child in self.children:
            if child.val == new_val:
                return child
        return None

    def append(self, new_val):
        child = self.child_path(new_val)
        if child:
            return child
        # create new node
        new_node = SuffixTrieNode(new_val)
        new_node.parent = self
        self.children.append(new_node)
        return new_node

    def traverse(self):
        '''
        all children nodes
        depth-first search
        '''
        if self.children:
            for child in self.children:
                yield child
                yield from child.traverse()

    def combine(self, child_node):
        '''
        The two nodes must be one-on-one link
        child_node can't be leave node
        '''
        # update this node as parent
        self.val += child_node.val
        self.children = child_node.children
        # update grandson
        for child2 in child_node.children:
            child2.parent = self
        # delete child
        del child_node
        return self

    def search_children(self, surfix:str):
        for child in self.children:
            if surfix.startswith(child.val):
                return child, surfix[len(child.val):]
        return None, surfix