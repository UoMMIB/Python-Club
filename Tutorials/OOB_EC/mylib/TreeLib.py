import numpy as np
import pandas as pd

from .ExpressionTree import ExpressionTree

class ConstLeafNode(ExpressionTree):
    
    arity = 0 # leaf nodes have no children :-(
    
    def __init__(self,parent=None,**kwargs):
        v = kwargs.get('value',1.0)
        super().__init__(f'{v:0.2f}',parent)
        self._value = v
    
    def evaluate(self,data=None):
        if data is None:
            return self._value
        n = len(data)
        return np.repeat(self._value,n)
    
    def mutate(self):
        self._value = np.random.uniform(-1.0,1.0)
        self.name = f'{self._value:0.2f}'
        

class VarLeafNode(ExpressionTree):
    
    arity = 0 # leaf nodes have no children :-(
    
    def __init__(self,parent=None,**kwargs):
        self.varList = kwargs.get('varList',['x1'])
        v = np.random.choice(self.varList)
        super().__init__(v,parent)
        self.value = np.NaN
    
    def evaluate(self,data=None):
        if data is None:
            self.value = np.NaN
            return np.NaN
        else:
            self.value = data[self.name]
            return data[self.name]
    
    def mutate(self):
        v = np.random.choice(self.varList)
        self.name = v
        

class BinaryFuncPlus(ExpressionTree):
    
    arity = 2 # v = left + right
    
    def __init__(self,parent=None,**kwargs):
        super().__init__('+',parent)
        self.value = np.NaN
    
    def evaluate(self,data=None):
        if data is None:
            self.value = np.NaN
            return np.NaN
        else:
            self.value = self.left.evaluate(data)+self.right.evaluate(data)
            return self.value
    
    def mutate(self):
        pass
    
class BinaryFuncMinus(ExpressionTree):
    
    arity = 2 # v = left - right
    
    def __init__(self,parent=None,**kwargs):
        super().__init__('-',parent)
        self.value = np.NaN
    
    def evaluate(self,data=None):
        if data is None:
            self.value = np.NaN
            return np.NaN
        else:
            self.value = self.left.evaluate(data)-self.right.evaluate(data)
            return self.value
    
    def mutate(self):
        pass
    

class BinaryFuncMult(ExpressionTree):
    
    arity = 2 # v = left * right
    
    def __init__(self,parent=None,**kwargs):
        super().__init__('*',parent)
        self.value = np.NaN
    
    def evaluate(self,data=None):
        if data is None:
            self.value = np.NaN
            return np.NaN
        else:
            self.value = self.left.evaluate(data)*self.right.evaluate(data)
            return self.value
    
    def mutate(self):
        pass
    
    
class BinaryFuncDiv(ExpressionTree):
    
    arity = 2 # v = left / right
    
    def __init__(self,parent=None,**kwargs):
        super().__init__('/',parent)
        self.value = np.NaN
    
    def evaluate(self,data=None,**kwargs):
        if data is None:
            self.value = np.NaN
            return np.NaN
        else:
            self.value = self.left.evaluate(data) / self.right.evaluate(data)
            return self.value
    
    def mutate(self):
        pass
    
