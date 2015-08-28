import sys
import os
from random import shuffle

file_name = os.readlink('/proc/self/fd/0')
#print(file_name)

data = {}        
for line in sys.stdin:
    x = line.split()
    node = int(x[0])
    out = []
    for i in range(len(x)-1):
        out.append(int(x[i+1]))
    data[node] = {"links": out, 
                  "cluster": None}

clusters = {}
def make_cluster(node, num_clusters):
    data[node]["cluster"] = num_clusters
    try:
        #check_initialized = clusters[num_clusters]["area"]
        clusters[num_clusters]["nodes"].append(node)
        shuffle(data[node]["links"]) #add some much needed randomness
        for i in data[node]["links"]:
            try: 
                if(data[i]["cluster"] == num_clusters):
                    clusters[num_clusters]["area"] += 1
                else:
                    clusters[num_clusters]["perimeter"].append(i)
            except KeyError:
                clusters[num_clusters]["perimeter"].append(i)
        while True:
            try:
                clusters[num_clusters]["perimeter"].remove(node)
            except ValueError:
                break

    except KeyError:
        #print("initializing a new cluster")
        clusters[num_clusters] = {"area": 0, "nodes": [node],
                                  "perimeter": [i for i in data[node]['links']]}

    for link in data[node]['links']:
        try:
            if(data[link]["cluster"] != None):
                continue
        
            old_area = clusters[num_clusters]["area"]
            old_perimeter = len(clusters[num_clusters]["perimeter"])

            num_point_to_this_link = sum([True for i in clusters[num_clusters]["perimeter"] if i == link])

            num_links_in_new_link =  len(data[link]['links'])
            new_perimeter = old_perimeter + num_links_in_new_link - 2*num_point_to_this_link
            new_area = old_area + num_point_to_this_link
            if(new_area/(new_perimeter + 0.0001) > old_area/(old_perimeter + 0.0001)):
                make_cluster(link, num_clusters)
            
        except KeyError:
            #print("keyError on :", link)
            pass
        
    



num_clusters = 0
for node in data:
    if(data[node]["cluster"] != None):
        continue

    num_clusters += 1
    if(num_clusters<10):
        make_cluster(node, num_clusters)
    else:
        print("Too many clusters")
        sys.exit(1)

#print(file_name, "num_clusters", num_clusters)
#print(data) 
for c in clusters:
    print(file_name,"area", clusters[c]['area'],"nodes",clusters[c]["nodes"], "perimeter", clusters[c]["perimeter"])



