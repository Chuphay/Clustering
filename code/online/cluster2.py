import numpy as np
from tree_cluster import t_node

class Cluster(object):
    def __init__(self, my_id, nodes, weights, degrees, perimeter = None, area = None):
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
        self.my_id = my_id
            
    def get_closest(self):
        #print("getting closest", self.my_id)
        if(sum(self.nodes) == len(self.nodes)):
            raise IndexError
        if(sum(self.weights) == 0):
            raise IndexError
        if (self.parent == None):
            temp_perimeter = self.perimeter - 2*self.weights + self.degrees
            temp_area = self.area + self.weights 
            #ratios = temp_area / (temp_perimeter + 0.000001)
            ratios = self.weights/(self.degrees - self.weights + 0.00001)
            next_vertex = np.argmax(ratios * np.logical_not(self.nodes))
            this_alpha = (self.area*temp_perimeter[next_vertex])/(self.perimeter*temp_area[next_vertex])
            return (next_vertex,  this_alpha)
        else:
            return self.parent.get_closest()
        
    def get_alpha(self, other_nodes):
        #print("getting_alpha")
        if(sum(self.nodes) == len(self.nodes)):
            raise IndexError
        if(sum(self.weights) == 0):
            raise IndexError
        if(len(other_nodes) != len(self.nodes)):
            raise SyntaxError
        if (self.parent == None):
            temp_perimeter = self.perimeter - 2*self.weights + self.degrees
            temp_area = self.area + self.weights 
            #ratios = temp_area / (temp_perimeter + 0.000001)
            ratios = self.weights/(self.degrees - self.weights + 0.00001)
            next_vertex = np.argmax(ratios * other_nodes)
            this_alpha = (self.area*temp_perimeter[next_vertex])/(self.perimeter*temp_area[next_vertex])
            return (this_alpha, next_vertex)
        else:
            return self.parent.get_alpha(other_nodes)
        
        
    def add_nodes(self, node_vector, weight):
        node_vector = node_vector.astype(float)
        if(sum(np.logical_and(self.nodes,node_vector)) != 0):
            raise IndexError

        self.weights = self.weights + weight.astype(float)
        self.nodes = self.nodes + node_vector
        self.area = sum(self.weights*self.nodes)/2.0
        self.perimeter = sum(self.weights) - 2*self.area

    def get_change(self, other_nodes):
        cur = self.__get_parent()
        temp_area = sum(cur.weights*other_nodes)
        temp_perimeter = - 2*sum(cur.weights*other_nodes) + sum(cur.degrees*other_nodes)
        return (temp_area, -temp_perimeter)

        
    def readable_nodes(self):
        out = []
        for i in range(len(self.nodes)):
            if(self.nodes[i] == 1):
                out.append(i)
        return out
    def get_parent(self):
        cur = self
        while(cur.parent):
            cur = cur.parent
        return cur.my_id
    def __get_parent(self):
        cur = self
        while(cur.parent):
            cur = cur.parent
        return cur

    def get_nodes(self):
        cur = self.__get_parent()
        return cur.nodes




def make_clusters(adjacency,  seed = 0):
    graph = np.array(adjacency)
    degrees = np.sum(graph, axis = 1) 
    n = len(graph)
    all_nodes = np.eye(n)
    clusters = [Cluster(i, all_nodes[i],graph[i].astype(float),degrees) for i in range(n)]
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


        next_node, alpha = clusters[here].get_closest()
        #print("here", here, "next_node", next_node, "alpha", alpha)
        #print(clusters[next_node].get_nodes())
        #print(clusters[here].get_change(clusters[next_node].get_nodes()))


        while(clusters[next_node].parent):
            next_node = clusters[next_node].parentId

        next_node_best, next_node_alpha = clusters[next_node].get_closest()
        #print("alphas", alpha, next_node_alpha)
        if(clusters[here].nodes[next_node_best] == 1):
            #print("match!", next_node)
            #print(clusters[next_node].get_change(clusters[here].get_nodes()))
            where_we_are = [here]
            where_we_are_alpha = []
            clusters[here].add_nodes(clusters[next_node].nodes,clusters[next_node].weights)
            clusters[next_node].parent = clusters[here]
            clusters[next_node].parentId = here
            binary_cluster[here].union(binary_cluster[next_node], alpha, next_node_alpha)


        elif(alpha < next_node_alpha):
            print("Takeover!!!", alpha, next_node_alpha, here, next_node)
            #print(clusters[next_node].get_change(clusters[here].get_nodes()))
            where_we_are = [here]
            where_we_are_alpha = []
            clusters[here].add_nodes(clusters[next_node].nodes,clusters[next_node].weights)
            clusters[next_node].parent = clusters[here]
            clusters[next_node].parentId = here
            binary_cluster[here].union(binary_cluster[next_node], alpha, next_node_alpha)

        elif(next_node in where_we_are):

            
            where_we_are_alpha.append(alpha) #sort of messy, but we got to do it
            print("found a loop:", where_we_are, next_node, where_we_are_alpha,"here", here)
            
            backwards_alpha = []
            max_alpha =[] #actually we are doing the average
            for i in range(len(where_we_are)):
                first = where_we_are[i]
                second = where_we_are[(i+1)%len(where_we_are)]
                t_t_alpha, next_ve =  clusters[second].get_alpha(clusters[first].nodes)
                backwards_alpha.append(t_t_alpha)
                if(backwards_alpha[i] > where_we_are_alpha[i]):
                    max_alpha.append(t_t_alpha+where_we_are_alpha[i]) #average
                else:
                    max_alpha.append(where_we_are_alpha[i]+t_t_alpha) #average
            
            minimum_arg = np.argmin(np.array(max_alpha))
            #print(where_we_are[minimum_arg], where_we_are[(minimum_arg+1)%len(where_we_are)])
            here = where_we_are[minimum_arg]
            spot = where_we_are[(minimum_arg +1)%len(where_we_are)]
            if(clusters[here].parent or clusters[spot].parent):
                raise SyntaxError
            """
            size_of_cluster = []
            for x in where_we_are:
                size_of_cluster.append(sum(clusters[x].nodes))
            minimum_arg = np.argmin(np.array(size_of_cluster))
            here = where_we_are[minimum_arg]
            spot = where_we_are[(minimum_arg +1)%len(where_we_are)]
            """
        
            clusters[here].add_nodes(clusters[spot].nodes,clusters[spot].weights)
            clusters[spot].parent = clusters[here]
            clusters[spot].parentId = here
            binary_cluster[here].union(binary_cluster[spot],\
                                       where_we_are_alpha[minimum_arg],\
                                       backwards_alpha[minimum_arg]) 
            where_we_are = [here]
            where_we_are_alpha = []
        else:
            #print("moving on")
            #print(clusters[next_node].get_change(clusters[here].get_nodes()))
            where_we_are.append(next_node)
            where_we_are_alpha.append(alpha)

    return binary_cluster[0].get_parent()


def make_one_cluster(clust_tree, graph):
    #print(clust_tree.nodes)
    n = len(graph)
    graph = np.array(graph)
    degrees = np.sum(graph, axis = 1) 
    weights = np.zeros(n)
    nodes = np.zeros(n)
    for x in clust_tree.nodes:
        nodes[x] = 1 
        weights += graph[x]
    area = 0
    for x in clust_tree.nodes:
        area += weights[x]/2.0
    perimeter = sum(weights) - 2*area
    return Cluster(clust_tree.nodes[0], nodes, weights, degrees, perimeter, area)

if __name__ == "__main__":

    graph = np.array([[0,1,0.1,0,0,0],
                      [1,0,0,0.1,0,0],
                      [0.1,0,0,1,0.1,0],
                      [0,0.1,1,0,0,0.1],
                      [0,0,0.1,0,0,1],
                      [0,0,0,0.1,1,0]])
    graph = np.array([[0,1,1,0,0,0],[1,0,1,0,0,0],[1,1,0,1,0,0],[0,0,1,0,1,1],[0,0,0,1,0,1],[0,0,0,1,1,0]])
    np.random.seed(13)
    n = 8
    thing1 = np.random.randn(n*n).reshape(n,n)
    thing1 = abs(thing1.T + thing1)
    for i in range(n):
        thing1[i][i] = 0
    graph = thing1
    clusters = make_clusters(graph)
    #clusters.print_nodes()
    #clusters.print_tree()

    myCluster = make_one_cluster(clusters.children[1], graph)
    print(myCluster.get_closest())

