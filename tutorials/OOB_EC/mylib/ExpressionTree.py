from .TreeNode2 import TreeNode
from abc import ABCMeta, abstractmethod
import numpy as np

class ExpressionTree(TreeNode,metaclass=ABCMeta):
    # ExpressionTree is a subclass of TreeNode
      
    arity = 2 
    #how many child nodes; Const, Var = 0, Unary function =1, binary function = 2; 
    # now a class variable
    
    @classmethod
    def treegrow(cls,tree,maxd=5,varList=['x1','x2','x3']):
        d = tree.getDepth 
        if d < maxd and tree.arity > 0:
            if (d==maxd-1):
                if not tree.left:
                    k = np.random.choice([k for k in cls.__subclasses__() if k.arity==0])
                    tree.left = k(varList=varList)
            else:
                if not tree.left:
                    k = np.random.choice([k for k in cls.__subclasses__()])
                    tree.left = k()
                cls.treegrow(tree.left,maxd)
        if d < maxd and tree.arity > 1:
            if (d==maxd-1):
                if not tree.right:
                    k = np.random.choice([k for k in cls.__subclasses__() if k.arity==0])
                    tree.right = k(varList=varList)
            else:
                if not tree.right:
                    k = np.random.choice([k for k in cls.__subclasses__()])
                    tree.right = k()
                cls.treegrow(tree.right,maxd)
    
    # Override __init__
    def __init__(self,value,parent=None):
        super().__init__(value,parent)
        
    def __deepcopy__(self,memo):
        new = object.__new__(type(self))
        memo[id(self)] = new
        new.__dict__.update(deepcopy(self.__dict__, memo))
        #manually deal with left and right parents:
        if new.right:
            new.right.parent = new
        if new.left:
            new.left.parent = new
        return new
        
    @property
    def value(self): #an example method that doesn't really do much!
        return self._value
        
    @value.setter
    def value(self, newvalue):
        #now we introduce some data validation...
        if np.all(np.isreal(newvalue)):
            self._value = newvalue
        else:
            raise TypeError("'value' must be numeric!")
          
    @property
    def findRoot(self):
        if self.parent is None:
            return self
        else:
            return self.parent.findRoot
    
    @property
    def getDepth(self):
        if self.parent is None:
            return 1
        else:
            return self.parent.getDepth+1
        
    @property
    def getMaxd(self):
        if self.left and self.right:
            d = max(self.left.getMaxd,self.left.getMaxd)
            return d + 1
        if self.left:
            d = self.left.getMaxd
            return d + 1
        if self.right:
            d = self.right.getMaxd
            return d + 1
        return 1
    
    @property
    def getMaxdFromRoot(self):
        return self.findRoot.getMaxd
        
    @abstractmethod
    def evaluate(self,data=None):
        pass
    
    def grow(self,maxd=5):
        d = self.getDepth 
        if d < maxd and self.arity > 0:
            self.left = ExpressionTree('L'+ str(d+1),self)
            self.left.grow(maxd)
        if d < maxd and self.arity > 1:
            self.right = ExpressionTree('R'+ str(d+1),self)
            self.right.grow(maxd)
    
    def clone(self):
        return copy.deepcopy(self)
    
    @abstractmethod
    def mutate(self):
        pass
