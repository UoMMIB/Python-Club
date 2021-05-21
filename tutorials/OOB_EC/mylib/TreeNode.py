from graphviz import Digraph
import weakref

print('TreeNode has loaded')

class TreeNode:
    """
Using a binary tree structure as an example; where a tree is composed of nodes that may have zero, one or two child nodes.
the class represents one node of the tree.
    """ 
    
    nextUID = 1
    
    @classmethod
    def getUID(cls):
        uid = cls.nextUID
        cls.nextUID += 1
        return uid
        
    def __init__(self,name, parent=None):
        self.name = name
        self._left = None
        self._right = None
        #we keep track of the parent node so that we can traverse the tree in reverse
        self._parent = parent 
        self._value = 42 #we've made this protected now, 42 is default
        self._uid = str(TreeNode.getUID())
        
    @property
    def left(self):
        return self._left
    
    @left.setter
    def left(self,child):
        self._left = child
        if child is None:
            return
        child.parent = self
    
    @property
    def right(self):
        return self._right
    
    @right.setter
    def right(self,child):
        self._right = child
        if child is None:
            return
        child.parent = self

    @property
    def parent(self):
        return self._parent
            
    @parent.setter
    def parent(self, parent):
        self._parent = parent
        
    @property
    def value(self): #an example method that doesn't really do much!
        return self._value
    
    @value.setter
    def value(self, newvalue):
        #now we introduce some data validation...
        if isinstance(newvalue, (int, float)) and not isinstance(newvalue, bool):
            self._value = newvalue
        else:
            raise TypeError("'value' must be numeric!")
            
    @staticmethod
    def add_nodes_edges(tree, dot=None):
        # Create Digraph object
        if dot is None:
            dot = Digraph()
            dot.node(name=tree._uid, label=tree.name,style='filled',fillcolor='yellow')

        # Add nodes
        if tree.left:
            dot.node(name=tree.left._uid, label=tree.left.name)
            dot.edge(tree._uid, tree.left._uid)
            dot = tree.add_nodes_edges(tree.left, dot=dot)

        if tree.right:
            dot.node(name=tree.right._uid ,label=tree.right.name)
            dot.edge(tree._uid, tree.right._uid)
            dot = tree.add_nodes_edges(tree.right, dot=dot)

        return dot
    
    def plot(self):
        # Add nodes recursively and create a list of edges
        dot = TreeNode.add_nodes_edges(self)
        return dot
    
    def __str__(self):
        s = self.name
        if self.left and self.right:
            return s+'['+str(self.left)+','+str(self.right)+']'
        if self.left:
            return s+'['+str(self.left)+']'
        if self.right:
            return s+'['+str(self.right)+']'
        return s
