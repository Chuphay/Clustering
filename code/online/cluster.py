import numpy as np
from tree_cluster import t_node

class Cluster(object):
    def __init__(self, nodes, weights, degrees, perimeter = None, area = None):
        self.nodes = nodes.astype(float)
        self.weights = weights.astype(float)
        self.degrees = degrees #this never changes       
        if(perimeter == None):
            if(sum(self.nodes) != 1):
                raise IndexError
            self.perimeter = sum(self.weights)
        else:
            self.perimeter = perimeter
        if(area == None):
            self.area = 0
        else:
            self.area = area
        self.parent = None
        self.parentId = None
            
    def get_closest(self):
        if(sum(self.nodes) == len(self.nodes)):
            raise IndexError
        if(sum(self.weights) == 0):
            raise IndexError
        if (self.parent == None):
            temp_perimeter = self.perimeter - 2*self.weights + self.degrees
            temp_area = self.area + self.weights 
            ratios = temp_area / (temp_perimeter + 0.000001)
            next_vertex = np.argmax(ratios * np.logical_not(self.nodes))
            this_alpha = (self.area*temp_perimeter[next_vertex])/(self.perimeter*temp_area[next_vertex]) 
            return (next_vertex, temp_area[next_vertex], temp_perimeter[next_vertex], this_alpha)
        else:
            return self.parent.get_closest()
        
    def get_alpha(self, other_node):
        if(sum(self.nodes) == len(self.nodes)):
            raise IndexError
        if(sum(self.weights) == 0):
            raise IndexError
        if (self.parent == None):
            temp_perimeter = self.perimeter - 2*self.weights[other_node] + self.degrees[other_node]
            temp_area = self.area + self.weights[other_node] 
            this_alpha = (self.area*temp_perimeter)/(self.perimeter*temp_area) 
            return this_alpha
        else:
            return self.parent.get_alpha(other_node)
        
        
    def add_nodes(self, node_vector, weight):
        node_vector = node_vector.astype(float)
        if(sum(np.logical_and(self.nodes,node_vector)) != 0):
            raise IndexError

        self.weights = self.weights + weight.astype(float)
        self.nodes = self.nodes + node_vector
        self.area = sum(self.weights*self.nodes)/2.0
        self.perimeter = sum(self.weights) - 2*self.area
        
    def readable_nodes(self):
        out = []
        for i in range(len(self.nodes)):
            if(self.nodes[i] == 1):
                out.append(i)
        return out



def make_clusters(adjacency, alpha_breaks = [0,1,2], seed = 0):
    graph = np.array(adjacency)
    degrees = np.sum(graph, axis = 1) 
    n = len(graph)
    all_nodes = np.eye(n)
    clusters = [Cluster(all_nodes[i],graph[i].astype(float),degrees) for i in range(n)]
    binary_cluster = [t_node([i]) for i in range(n)]

    where_we_are = [seed]
    where_we_are_alpha = []
    for i in range(3*n+2):
        here = where_we_are[-1]
        #print("here",here,clusters[here].readable_nodes())
        if(clusters[here].parent):
            print("this is probably a bug")

        if(sum(clusters[here].nodes)==n):
            print("Finished after", i, "iterations")
            break
        if(i == 3*n):
            print("bad break....")
            break


        next_node, not_using, not_using2, alpha = clusters[here].get_closest()
        #print("here", here, "next_node", next_node, "alpha", alpha)


        while(clusters[next_node].parent):
            next_node = clusters[next_node].parentId

        next_node_best, not_using, not_using2, not_using3 = clusters[next_node].get_closest()

        if(clusters[here].nodes[next_node_best] == 1):
            #print("match!", next_node)
            where_we_are = [here]
            where_we_are_alpha = []
            clusters[here].add_nodes(clusters[next_node].nodes,clusters[next_node].weights)
            clusters[next_node].parent = clusters[here]
            clusters[next_node].parentId = here
            binary_cluster[here].union(binary_cluster[next_node])

        elif(next_node in where_we_are):
            #print("found a loop:", where_we_are, next_node, where_we_are_alpha,"here", here)
            
            where_we_are_alpha.append(alpha) #sort of messy, but we got to do it
            minimum_arg = np.argmin(np.array(where_we_are_alpha))

            #print(where_we_are[minimum_arg], where_we_are[(minimum_arg+1)%len(where_we_are)])
            here = where_we_are[minimum_arg]
            spot = where_we_are[(minimum_arg +1)%len(where_we_are)]
            if(clusters[here].parent or clusters[spot].parent):
                raise SyntaxError

                    
            clusters[here].add_nodes(clusters[spot].nodes,clusters[spot].weights)
            clusters[spot].parent = clusters[here]
            clusters[spot].parentId = here
            binary_cluster[here].union(binary_cluster[spot])
            where_we_are = [here]
            where_we_are_alpha = []
        else:
            #print("moving on")
            where_we_are.append(next_node)
            where_we_are_alpha.append(alpha)

    return binary_cluster[0].get_parent()

if __name__ == "__main__":
    graph = np.array([[0,1,1,0,0,0],[1,0,1,0,0,0],[1,1,0,1,0,0],[0,0,1,0,1,1],[0,0,0,1,0,1],[0,0,0,1,1,0]])
    clusters = make_clusters(graph)
    clusters.print_nodes()
    clusters.print_tree()
    print("u")
