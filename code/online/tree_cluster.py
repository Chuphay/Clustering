

class t_node(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.n = len(nodes)
        self.parent = None
        self.children = None
        self.num_children = 0

    def print_nodes(self):
        print(self.nodes)

    def print_tree(self):
        self.print_nodes()
        if(self.children != None):
            for child in self.children:
                child.print_tree()
            
            
    def union(self, that):
        #print("union", self.nodes, that.nodes)
        cur = self.get_parent()
        that = that.get_parent()

        for node in cur.nodes: #could be 
            if(node in that.nodes): #time consuming
                print("Error: union") 
        #print("new union", cur.nodes, that.nodes)
        new_nodes = cur.nodes + that.nodes
        out = t_node(new_nodes)
        out.num_children = 2
        out.children = [cur, that]
        cur.parent = out
        that.parent = out
        return out

    def get_parent(self):
        cur = self
        while(cur.parent != None):
            cur = cur.parent
        return cur

if __name__ == "__main__":
    print("on")
    start = [t_node([i]) for i in range(10)]
    b = t_node([1])
    start[1].union(b)
    start[4].union(b)
    start[5].union(start[1])
    c = start[1].get_parent()
    c.print_nodes()
    start[7].union(start[9])
    start[9].union(start[1])
    start[1].get_parent().print_nodes()



