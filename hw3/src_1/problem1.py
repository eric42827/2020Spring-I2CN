import numpy as np

class dijkstra():
    def __init__(self,topo_matrix):
        self.topo_matrix = topo_matrix
        #print(self.topo_matrix)
        self.distance = np.empty(vertex_num,dtype = np.uint16)
        self.check_in_s = np.empty(vertex_num,dtype = bool)
        self.predecessor = np.empty(vertex_num,dtype = np.uint16)
    def init(self,source):
        self.S = list()
        self.source = source
        self.distance.fill(-1)
        #print('dist, ',self.distance)
        self.distance[source] = 0
        #rint('dist ',self.distance)
        self.check_in_s.fill(False)
        self.predecessor.fill(-1)
    def routing(self,source):
        #print('routing',source)
        self.init(source)
        #print('source dist:',self.distance[0])
        while len(self.S)!=vertex_num:
            u = self.extract_min()
            #print('u=',u)
            self.S.append(u)
            self.check_in_s[u] = True
            #print('dist, ',self.distance)
            for i in range(vertex_num):
                if self.topo_matrix[u][i]!=-1 and i!=u:
                    #print('relax!u:{} i:{}'.format(u,i))
                    self.relax(u,i)
    def extract_min(self):
        #print('extract_min')
        temp = self.distance.copy()
        #print('temp:',temp)
        temp[self.check_in_s] = -1
        #print('temp after check in s:',temp)
        #print('dist, ',self.distance)
        #print('arg ',np.argsort(temp))
        return np.argsort(temp)[0]
    def relax(self,u,v):
        if(self.distance[v] > self.distance[u] + self.topo_matrix[u][v]):
            #print('dist{}:{} to {}'.format(v,self.distance[v],self.distance[u] + self.topo_matrix[u][v]))
            self.distance[v] = self.distance[u] + self.topo_matrix[u][v]
            self.predecessor[v] = u
            #print('predecessor of {} is:{}'.format(v,self.predecessor[v]))
            #print('dist, ',self.distance)

    def output_file(self):
        with open(path_prefix+command[1], 'a') as f:
            #print('all dist',self.distance)
            f.write('Routing table of router {}:\n'.format(self.source+1))
            #print('Routing table of router {}:'.format(self.source+1))
            #print('predecessor: ',self.predecessor)
            for i in  range(vertex_num):
                if self.distance[i] == 65535 :
                    #print('{} {}'.format(-1,-1))
                    f.write('{} {}\n'.format(-1,-1))
                elif self.distance[i] == 0:
                    f.write('{} {}\n'.format(0,self.source+1))
                else:
                    #print('{} {}'.format(self.distance[i],self.next_router(i)+1))
                    f.write('{} {}\n'.format(self.distance[i],self.next_router(i)+1))
            f.close()
    def next_router(self,i):
        p = i
        if self.predecessor[p] == 65535:
            return p
        while self.predecessor[p]!=self.source:
            p = self.predecessor[p].copy()
        return p

while True:
    command = input('Please enter your test command:\n')
    command = command.split(' ')
    path_prefix = './'
    #print(command)
    if command[0]=='lf':
        with open(path_prefix+command[1],'r') as f:
            vertex_num = int(f.readline())
            #print('vertex',vertex_num)
            #next(f)
            topo_matrix = np.array([line.strip('\n').split(' ') for line in f], dtype = int)
        print('load file complete')
    elif command[0]=='of':
        D = dijkstra(topo_matrix)
        for i in range(vertex_num):
            #print(i)
            D.routing(i)
            D.output_file()
        print('finish process')
        break

