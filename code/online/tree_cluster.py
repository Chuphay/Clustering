

class t_node(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.n = len(nodes)
        self.parent = None
        self.children = None
        self.num_children = 0
        self.right_alpha = 0
        self.left_alpha = 0

    def print_nodes(self):
        print(self.nodes, self.right_alpha, self.left_alpha)

    def print_tree(self,  leaves = False):
        if(leaves and (self.children == None)):
            self.print_nodes()
        if(self.children != None):
            self.print_nodes()
            for child in self.children:
                child.print_tree(leaves)
            
            
    def union(self, that, right_alpha, left_alpha):
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
        out.right_alpha = right_alpha
        out.left_alpha = left_alpha
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



