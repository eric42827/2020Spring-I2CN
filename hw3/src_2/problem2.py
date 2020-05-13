import numpy as np

dtype = np.uint16
DTYPE_MAX = np.iinfo(dtype).max

class dijkstra():
    def __init__(self,topo_matrix):
        self.topo_matrix = topo_matrix
        self.distance = np.empty(vertex_num,dtype = dtype)
        self.check_in_s = np.empty(vertex_num,dtype = bool)
        self.predecessor = np.empty(vertex_num,dtype = dtype)
    def init(self,source):
        self.S = list()
        self.source = source
        self.distance.fill(-1)
        self.distance[source] = 0
        self.check_in_s.fill(False)
        self.predecessor.fill(-1)
    def routing(self,source):
        self.init(source)
        while len(self.S)!=vertex_num:
            u = self.extract_min()
            self.S.append(u)
            self.check_in_s[u] = True
            for i in range(vertex_num):
                if self.topo_matrix[u][i]!=-1 and i!=u:
                    self.relax(u,i)
    def extract_min(self):
        temp = self.distance.copy()
        temp[self.check_in_s] = -1
        return np.argsort(temp)[0]
    def relax(self,u,v):
        if(self.distance[v] > self.distance[u] + self.topo_matrix[u][v]):
            self.distance[v] = self.distance[u] + self.topo_matrix[u][v]
            self.predecessor[v] = u
    def output_filer(self):
        with open(path_prefix+path_name+'_out2.txt', 'a') as f:
            f.write('Routing table of router {}:\n'.format(self.source+1))
            for i in  range(vertex_num):
                if (i+1 in rm_set):
                    continue
                if self.distance[i] == 65535 :
                    f.write('-1 -1\n')
                elif self.distance[i] == 0:
                    f.write('0 {}\n'.format(self.source+1))
                else:
                    f.write('{} {}\n'.format(self.distance[i],self.next_router(i)+1))
            f.close()
    def next_router(self,i):
        p = i
        if self.predecessor[p] == 65535:
            return p
        while self.predecessor[p]!=self.source:
            p = self.predecessor[p].copy()
        return p
try:
    while True:
        command = input('Please enter your test command:\n')
        command = command.split(' ')
        path_prefix = './'
        if command[0]=='lf':
            path_name = command[1].split('.')[0]
            with open(path_prefix+command[1],'r') as f:
                vertex_num = int(f.readline())
                topo_matrix = np.array([line.strip('\n').split(' ') for line in f], dtype = int)
            adj_mat = topo_matrix.copy()
            rm_set = []
            print('load file complete')
        elif command[0]=='of':
            D = dijkstra(adj_mat)
            for i in range(vertex_num):
                if not(i+1 in rm_set):
                    D.routing(i)
                    D.output_filer()
            print('finish process')
            break
        elif command[0]=='rm':
            router_rm = int(command[1].strip('r'))
            rm_set.append(router_rm)
            adj_mat[router_rm-1].fill(-1)
            adj_mat[:][router_rm-1].fill(-1)
            print('remove router{}'.format(router_rm))
        else:
            print("Invalid command!Please enter again!")
except KeyboardInterrupt:
    pass

