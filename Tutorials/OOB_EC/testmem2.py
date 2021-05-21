import weakref
   
class DLL2:
    
    # Double linked list
    
    def __init__(self,parent=None):
        self._parent = weakref.ref(parent) if parent else parent
        self.link = None
        self.data = ' ' * 128 * 1024 * 1024
    
    @property
    def parent(self):
        # if parent is None, return None
        if not self._parent:
            return self._parent
        # get the actual parent from the weakref
        _parent = self._parent()
        if _parent:
            return _parent
        else:
            # if _parent is None, something went wrong?!
            raise LookupError("Parent was destroyed")
        
    def grow(self,d):
        if d==0:
            return
        self.link = DLL2(parent=self)
        self.link.grow(d-1)
        return
    
    def __del__(self):
        print("delete")

    
def test2():
    for _ in range(10):
        dll = DLL2()
        dll.grow(2)
        del(dll)
    print('End')
    
