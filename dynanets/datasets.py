import os

import numpy as np
import pandas as pd
from numpy.random import rand

# define a Uniform Distribution
U = lambda MIN, MAX, SAMPLES: rand(*SAMPLES.shape) * (MAX - MIN) + MIN

# define a Truncated Power Law Distribution
P = lambda ALPHA, MIN, MAX, SAMPLES: ((MAX ** (ALPHA+1.) - 1.) * rand(*SAMPLES.shape) + 1.) ** (1./(ALPHA+1.))

# define an Exponential Distribution
E = lambda SCALE, SAMPLES: -SCALE*np.log(rand(*SAMPLES.shape))

class Bunch(object):
    '''
    Iterable object with data attributes, used to iterate over the frames of the dataset.
    '''
    def __init__(self, iter_data, **karg):
        self.iter_data = iter_data
        for k, v in karg.iteritems():
            setattr(self, k, v)
    
    def __iter__(self):
        for i in self.iter_data():
            yield i

def dynamic_gnp(n, p):
    '''
    Implementation of the Dynamic G(n,p) graph as discussed in the following paper:
    
        Andrea E. F. Clementi, Francesco Pasquale, Angelo Monti, and Riccardo Silvestri. 2007. 
        Communication in dynamic radio networks. In Proceedings of the twenty-sixth annual 
        ACM symposium on Principles of distributed computing (PODC '07). ACM, New York, NY, USA, 205-214.
        
    At each time slot t of the execution of the protocol, a (new) graph G(t) is selected
    according to the well-known random graph model G(n,p) where n is the number of nodes and p is the
    edge probability.
    
    Required arguments:
    
      *n*:
        The number of vertices in the graph.
      *p*   
        The probability for drawing an edge between two arbitrary vertices (G(n,p) graph)
    
    '''
    
    def iter_data():
        while True:
            m = np.random.rand(n, n)
            c = np.where(m < p)
            yield np.array([(i,j) for i,j in zip(c[0], c[1]) if i < j])
        
    # Set bunch attributes
    result = Bunch(iter_data=iter_data)
    result.nr_nodes = n
    result.nr_frames = -1
    return result

def dynamic_gnm(n, m):
    '''
    Implementation of the Dynamic G(n,m) graph as discussed in the following paper:
    
        Andrea E. F. Clementi, Francesco Pasquale, Angelo Monti, and Riccardo Silvestri. 2007. 
        Communication in dynamic radio networks. In Proceedings of the twenty-sixth annual 
        ACM symposium on Principles of distributed computing (PODC '07). ACM, New York, NY, USA, 205-214.
    
    At each time slot t of the execution of the protocol, a (new) graph G(t) is selected
    according to the well-known random graph model G(n,m) where n is the number of nodes and m is the
    number of edges.
    
    Required arguments:
    
      *n*:
        The number of vertices in the graph.
      *m*:    
        The number of edges in the graph (for G(n,m) graphs).
    
    '''
    def iter_data():
        while True:
            contacts = []
            while len(contacts) < m:
                i = np.random.randint(n)
                j = np.random.randint(n)
                if i == j or (i, j) in contacts: continue
                contacts.append((i, j))
            yield np.array(contacts)

    # Set bunch attributes
    result = Bunch(iter_data=iter_data)
    result.nr_nodes = n
    result.nr_frames = -1
    return result
        
def edge_markovian(n, p, q, g=0):
    '''
    Implementation of the edge-Markovian dynamic graph as discussed in the following paper:
    
    Andrea E.F. Clementi, Claudio Macci, Angelo Monti, Francesco Pasquale, and Riccardo Silvestri. 2008. 
        Flooding time in edge-Markovian dynamic graphs. In Proceedings of the 
        twenty-seventh ACM symposium on Principles of distributed computing (PODC '08). 
        ACM, New York, NY, USA, 213-222.
    
    Starting from an arbitrary initial edge probability distribu- 
    tion, at every time step, every edge changes its state (exist- 
    ing or not) according to a two-state Markovian process with 
    probabilities p (edge birth-rate) and q (edge death-rate). If 
    an edge exists at time t then, at time t + 1, it dies with prob- 
    ability q. If instead the edge does not exist at time t, then 
    it will come into existence at time t + 1 with probability p. 
    
    Required arguments:
    
      *n*:
        The number of vertices in the graph.
      *p*
        If the edge does not exist at time t then it will come into existence at time
        t + 1 with probability p.
        
      *p*
        If an edge exists at time t then, at time t + 1, it dies with probability q.
    
      *g*:
        an arbitrary initial probability distribution over the set [n] yielding E0.
    
    '''
    
    def iter_data():
        # adjacency matrix
        a = np.zeros((n,n))

        # initial set of edges
        a[np.where(np.random.rand(n, n) < g)] = 1

        while True:
            m = np.random.rand(n, n)
            up = np.where(np.logical_and(a == 0, m < p))
            down = np.where(np.logical_and(a > 0, m < q))
            a[up] = 1.
            a[down] = 0.

            c = np.nonzero(a)
            yield np.array([(i,j) for i,j in zip(c[0], c[1]) if i < j])
    
    # Set bunch attributes
    result = Bunch(iter_data=iter_data)
    result.nr_nodes = n
    result.nr_frames = -1
    return result
        
def continuous_time_edge_markovian(n, lmbd):
    '''
    Implementation of the continuous-time edge-Markovian dynamic graph as discussed in the following paper:
    
    Augustin Chaintreau, Abderrahmen Mtibaa, Laurent Massoulie, and Christophe Diot. 2007. 
        The diameter of opportunistic mobile networks. In Proceedings of the 
        2007 ACM CoNEXT conference (CoNEXT '07). ACM, New York, NY, USA, , Article 12 , 12 pages.
    
    We assume that, for any pairs of nodes (u, v), the times of
    contact are separated by exponential random variables.
    '''
    
    def iter_data():
        a = np.zeros((n,n))
        a = E(lmbd, a)

        while True:
            a -= 1.
            c = np.where(a <= 0.)
            yield np.array([(i,j) for i,j in zip(c[0], c[1]) if i < j])
            a[c] = E(lmbd, c[0])
            
    # Set bunch attributes
    result = Bunch(iter_data=iter_data)
    result.nr_nodes = n
    result.nr_frames = -1
    return result
        
def broad_continuous_time_edge_markovian(n, alpha):
    '''
    This model is similar to the continuous-time edge-Markovian dynamic graph as discussed in the following paper:
    
    Augustin Chaintreau, Abderrahmen Mtibaa, Laurent Massoulie, and Christophe Diot. 2007. 
        The diameter of opportunistic mobile networks. In Proceedings of the 
        2007 ACM CoNEXT conference (CoNEXT '07). ACM, New York, NY, USA, , Article 12 , 12 pages.
        
    The difference is in the generated inter-contact times.    
    We assume that, for any pairs of nodes (u, v), the times of
    contact are separated by random variables from a power-law distribution.
    '''
    
    def iter_data():
        a = P(alpha, 1., 1000., np.random.rand(n,n))

        while True:
            a -= 1.
            c = np.where(a <= 0.)
            yield np.array([(i,j) for i,j in zip(c[0], c[1]) if i < j])
            a[c] = P(alpha, 1., 1000, np.random.rand(*c[0].shape))
            
    # Set bunch attributes
    result = Bunch(iter_data=iter_data)
    result.nr_nodes = n
    result.nr_frames = -1
    return result


def load_spschool():
    '''
    Loads the SocioPatterns School data.
    The data were collected by the SocioPatterns collaboration using wearable proximity sensors that
    sense the face-to-face proximity relations of individuals wearing them.
    '''
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data = pd.read_csv(dir_path + "/data/school.csv.gz", compression="gzip")
    
    def iter_data():
        for t in range(0, data.t.max()+1, 20):
            subdf = data[data.t==t]
            yield subdf[['i', 'j']].values
    
    'Set bunch attributes'
    result = Bunch(iter_data=iter_data, data=data)
    result.nr_nodes = np.max([data.i.max(), data.j.max()]) + 1
    result.nr_frames = np.max(data.t)/20 + 1
    return result
    
def fetch_HT2009(aggregation=None, remove_empty=True):
    
    import urllib2
    import gzip
    from StringIO import StringIO

    response = urllib2.urlopen("http://www.sociopatterns.org/files/datasets/003/ht09_contact_list.dat.gz")
    buf = StringIO(response.read())
    f = gzip.GzipFile(fileobj=buf)
    
    frames_dict = {}
    nodes_dict = {}
    nr_nodes = 0
    
    for line in f:
        (time, source, target) = map(int, line.split('\t'))
        if source == target:
            continue
        if time not in frames_dict:
            frames_dict[time] = []
            
        if source not in nodes_dict:
            nodes_dict[source] = nr_nodes
            nr_nodes += 1
        if target not in nodes_dict:
            nodes_dict[target] = nr_nodes
            nr_nodes += 1
        
        source = nodes_dict[source]
        target = nodes_dict[target]
        frames_dict[time].append((source, target))
    
    frames = []
    for t in range(min(frames_dict.keys()), max(frames_dict.keys()), 20):
        if t not in frames_dict:
            if not remove_empty:
                frames.append([])
        else:
            frames.append(frames_dict[t])
    
    nr_frames = len(frames)
    
    def iter_data():
        for frame in frames:
            yield frame
            
    # Set bunch attributes
    result = Bunch(iter_data=iter_data, data=frames)
    result.nr_nodes = nr_nodes
    result.nr_frames = nr_frames
    return result