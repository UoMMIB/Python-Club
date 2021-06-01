class DLL:
    # Double linked list
    
    def __init__(self,parent=None):
        self.parent = parent
        self.link = None
        # make each instance use up a reasonably large amount of memory ~128 MB.
        self.data = ' ' * 128 * 1024 * 1024
        
    def grow(self,d):
        if d==0:
            return
        self.link = DLL(parent=self)
        self.link.grow(d-1)
        return
    
    def __del__(self):
        print("delete")
       
def test():
    for _ in range(10):
        dll = DLL() #any previous 'dll' should be free to be deleted
        dll.grow(2)
        del(dll)
    print('End')
