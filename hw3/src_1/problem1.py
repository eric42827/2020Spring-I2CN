import numpy as np
while True:
    command = input()
    command = command.split(' ')
    path_prefix = './'
    if command[0]=='lf':
        with open(path_prefix+command[1],'r') as f:
            next(f)
            topo_matrix = np.array([line.strip('\n').split(' ') for line in f], dtype = int)
        print(topo_matrix)
    elif command[0]=='of':
        with open(path_prefix+command[1], 'w') as f:
            for i in  topo_matrix:
                f.write('{}\n'.format(topo_matrix[i]))

class dijkstra():
    def __init__(self,topo_matrix):
        self.topo_matrix = topo_matrix
        self.vertices = np.empty(len(topo_matrix[0]),dtype = np.uint16)
        self.check_in_q = np.empty(len(topo_matrix[0]),dtype = bool)
        self.S = list()
    def init(source):
        self.vertices = self.vertices.fill(-1) 
        self.vertices[source] = 0
        self.check_in_q.fill(False)
    def routing(source):
        init(source)
        while len(vertices)!=len(S):
            u = extract_min()
            
    def extract_min():
        temp = vertices
        temp[check_in_q == True] = -1
        return np.argsort(temp)[0]
                

