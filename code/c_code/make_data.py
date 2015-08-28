import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial.kdtree import KDTree 
from subprocess import Popen, PIPE


#not sure about the following line
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')


def write(s):
    s = s.split()
    out = Popen(s,stdout = PIPE).communicate()[0]
    return out.decode("utf-8")


def plot_clusters(data):

    clusters = list(map(int, open("clusters.data").read().split()))
    num_clusters = max(clusters)
    colors = cm.rainbow(np.linspace(0, 1, num_clusters))

    for i in range(num_clusters):
        for j in range(len(clusters)):
            if(clusters[j] == i + 1): #plus 1 because my clusters start at 1
                ax.scatter(data[j][0],data[j][1],data[j][2], c = colors[i])

    plt.show();


def make_gauss(n, mean=0, sd=1):
    x = np.random.normal(mean, sd, n)
    y = np.random.normal(mean, sd, n)
    z = np.random.normal(mean, sd, n)
    return np.array([x,y,z]).T


def make_ring(n, radius = 10, noise = 1):
    theta = 2*np.pi*np.random.rand(n)
    x = radius*np.cos(theta)+noise*np.random.randn(n)
    y = radius*np.sin(theta)+noise*np.random.randn(n)
    z = np.random.randn(n)*noise/10  #felt better
    return np.array([x,y,z]).T 

def plot_data(data, c = 'k', mark = '.'):
    ax.scatter(data[:,0],data[:,1],data[:,2], color = c, marker = mark)
    plt.show()

def make_saturn(n, sd = 1.1, r= 7, noise = 1):
    flag = n%2
    d_1 = make_gauss(n//2+flag, sd = sd)
    d_2 = make_ring(n//2, r, noise)

    return np.vstack((d_1,d_2))

def make_two(n):
    flag = n%2
    d_1 = make_gauss(n//2, mean=0)
    d_2 = make_gauss(n//2+flag, mean =7)
    return np.vstack((d_1,d_2))




 
def make_adjacency_matrix(data, k):
    kt = KDTree(data) 
    out = zeros((len(data),len(data)))
    for i, points in enumerate(data):
        distance, neighbors = kt.query_ball_point(points, k)
        for j in neighbors[1:]:
            out[i][j] = 1;
            out[j][i] = 1; #to ensure symmetry, one can imagine the the nearest neighbors is not necessarily associative
    return out 

def make_edge_graph(data, k, ball = True):
    kt = KDTree(data)
    out = [set() for i in data]
    k_max = 0
    k_min = np.infty
    for i, points in enumerate(data):
        if(ball):
            neighbors = kt.query_ball_point(points, k)
        else:
            distance, neighbors = kt.query(points,int(k+1))
            neighbors = neighbors[1:]
        for j in neighbors:
            if(j != i):
                out[i].add(j)
                if(len(out[i])>k_max):
                    k_max = len(out[i])
                out[j].add(i)
                if(len(out[j])>k_max):
                    
                    k_max = len(out[j])
        if(len(out[i])<k_min):
            k_min = len(out[i])

    return (k_min, k_max, out)

def write_data(edge_graph, k, file_name):
    N = len(edge_graph)
    f = open(file_name, 'w')
    f.write("{0} {1}\n".format(N,k))
    for i, d in enumerate(edge_graph):
        f.write("{0}".format(str(i)))
        for j in d:
            f.write(" {0}".format(str(j)))
        f.write("\n")
    f.close()

def plot_perimeter():
    perimeter = list(map(int, open("perimeter.data").read().split()))
    plt.plot([i for i in range(len(perimeter))],perimeter)
    plt.show()

def get_num_clusters(alpha):
    my_string = "./look_up {0}".format(alpha)
    x = write(my_string)
    #print(x)
    z = x.split("\n")[2]
    if(z[:15] == 'num_of_clusters'):
        return int(z[15:])
    else:
        return np.infty
    
  
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_zlim(-10, 10)
    num = 1000
    k = 30
    np.random.seed(123)
    g = make_saturn(num)
    #g = make_two(num)
    k_min,k_max, x = make_edge_graph(g, k, False)
    k_tot = 0
    for d in x:
        k_tot = k_tot + len(d)

    print("min:",k_min,"max:",k_max, "avg:",(k_tot/num))    
    if(k_min == 0):
        print("k_min is zero, not writing data")
    else:
        write_data(x, k_max, "test.data")
        #plot_data(g)

    x = write("./look_up")
    print(x)
    plot_clusters(g)
    plot_perimeter()
