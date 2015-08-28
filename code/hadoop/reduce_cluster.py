import sys
import re
from random import shuffle
data = {}
data_nodes = {}
current_file = None
current_cluster = None
num_clusters_start = 0
for line in sys.stdin:
    #print(line.strip())
    x = re.search("file.\.txt", line).group()
    words = line.split()
    num_clusters_start += 1
    nodes = [int(i) for i in re.search("nodes \[(.*)\] per", line).group(1).split(",")]
    for i in nodes:
        data_nodes[i] = num_clusters_start
    perimeter = [int(i) for i in re.search("perimeter \[(.*)\]$",line).group(1).split(",") if i != ""]
    data[num_clusters_start] = {'nodes':nodes, 'area': int(words[2]), 'perimeter':perimeter}

#print(data)
#print(data_nodes)
data_nodes_out = {}
for i in data_nodes:
    data_nodes_out[i] = None
data_out = {}

def add_to_cluster(c, x, area):
    data_out[c]["area"] = area
    for i in data[x]["nodes"]:
        data_out[c]["nodes"].append(i)
        data_nodes_out[i] = c
    for i in data[x]["perimeter"]:
        data_out[c]["perimeter"].append(i)
    #data_nodes[x] = c
    #print(data_out[c]["perimeter"])
    temp = []
    for i in data_out[c]["perimeter"]:
        #print("inside",i, data_out[c]["perimeter"])
        if(i in data_out[c]["nodes"]):
            pass
        else:
            temp.append(i)
    data_out[c]["perimeter"] = temp
    


num_clusters = 0
for c in data:
    already_mapped = False
    for i in data[c]["nodes"]:
        if(data_nodes_out[i] != None):
            already_mapped = True
            
    print("Already_mapped: ", already_mapped, c)
    if(already_mapped):
        continue
    num_clusters += 1
    for i in data[c]["nodes"]:
        data_nodes_out[i] = num_clusters
            
    data_out[num_clusters] = {'nodes':data[c]['nodes'][:], 'area':data[c]['area'], 'perimeter':data[c]['perimeter'][:]}
    
    print("TOP",c, data[c])
    print(data_nodes)
    #try:
    old_perimeter = len(data[c]['perimeter'])
    old_area = data[c]["area"]
    shuffle(data[c]['perimeter']) #add some much needed randomness
    for node in data[c]['perimeter']:
        if(data_nodes_out[node] != None):
            continue
        try:
            
            new_cluster = data_nodes[node]
            if(new_cluster == c): 
                print("Already in the cluster!")
                continue
            print(node, data_nodes[node], data[new_cluster])
            print(data[new_cluster]["perimeter"])
            links = 0           
            for new_new_node in data[new_cluster]["perimeter"]:
                try:
                    print(new_new_node, data_nodes[new_new_node])
                    if(data_nodes[new_new_node] == c):
                        links += 1

                except KeyError:
                    print("KeyError on new_new_node", new_new_node)
            print("links: " ,links)
            print("old_per: ",old_perimeter, "old_area: ", old_area)
            new_area = old_area + links + data[new_cluster]["area"]
            new_perimeter = old_perimeter + len(data[new_cluster]["perimeter"]) -2*links
            print("new_per: ", new_perimeter, "new_area: ", new_area)
            passed = new_area/(new_perimeter +0.0001) > old_area/(old_perimeter+0.0001)
            print("Pass? ", passed)
            if(passed): add_to_cluster(num_clusters, new_cluster, new_area)
            
        except KeyError:
            print("KeyError on", node)
    

print(data_out)
print(data_nodes_out)
