import os, sys

data = {'elapsed':[], 'user':[], 'system':[]}

for i in range(10):
    os.system('(time ./look_up) 2> time.txt')
    text = open('time.txt').read().split()

    
    #for the 336 machines:
    data[text[0][4:]].append(text[0][:4])
    data[text[1][4:]].append(text[1][:4])
    data[text[2][7:]].append(text[2][3:7])
    """
    #for the trig machines:
    data['elapsed'].append(text[1])
    data['user'].append(text[3])
    data['system'].append(text[5])
    """
    print( text)


try:
    text = open(sys.argv[1],'w')
    for i in data:
        text.write(i)
        text.write('\n')
        for j in data[i]:
            text.write(j)
            text.write(', ')
        text.write('\n')
    text.close()
except IndexError:
    print( 'supply a name for a file to save the data to.')
    pass


