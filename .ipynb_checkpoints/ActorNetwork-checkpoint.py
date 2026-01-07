import pandas as pd
from collections import defaultdict
import queue
import copy
import time

class ActorNetwork:

    def __init__(self):
        """ Creates an actor network object """
        self.costars = defaultdict(set) # actor(string) to acted with (set<string>)
        self.movies  = defaultdict(set) # actor(string) to movies starred in (set<string>)
        
    def getNumActors(self): return len(self.costars)
    
    def getNumConnections(self):
        """ Find the number of edges in a given actor network """
        numEdges = 0
        for _,v in self.costars.items(): numEdges += len(v)
        return int(numEdges/2)
                


    def loadDataSet(self, pthToActorFile, pthToMovieFile):

        import pandas as pd
        from collections import defaultdict, deque
    
        # =========================
        # LOAD DATA
        # =========================
        moviedf = pd.read_csv(pthToMovieFile, sep="\t", low_memory=False,engine="python",error_bad_lines=False,warn_bad_lines=True)
        actordf = pd.read_csv(pthToActorFile, sep="\t", low_memory=False,engine="python",error_bad_lines=False,warn_bad_lines=True)
        print(len(actordf))
        # =========================
        # BUILD MOVIE → ACTORS LOOKUP
        # =========================
        movie_to_actors = defaultdict(deque)
    
        for _, row in actordf.iterrows():
            if pd.isna(row["knownForTitles"]):
                continue
            for movie in row["knownForTitles"].split(","):
                movie_to_actors[movie].append(row["primaryName"])
    
        # =========================
        # BUILD NETWORK (SUBSET)
        # =========================
        MAX_MOVIES = 2000    # adjust if needed
        counter = 0
    
        for movie, actors in movie_to_actors.items():
            if len(actors) > 1:   # skip single-actor movies
                self.addMovie(movie, deque(actors))
                counter += 1
    
                if counter % 200 == 0:
                    print(f"{counter} movies processed")
    
                if counter >= MAX_MOVIES:
                    break

        
        
    def addMovie(self, movie, actors):
        """ Add a movie (string) and a set<actors> string to the network """
        processed = set()
        yetToProcess = actors
        #print(yetToProcess)
       # import pdb;pdb.set_trace()
        while yetToProcess: # Is only true when actors is non-empty
            actor = yetToProcess.popleft()
            
            s = set()
            q= copy.deepcopy(yetToProcess)
            while len(q)!=0:
                s.add(q.popleft())
                
            self.costars[actor] = self.costars[actor].union(s).union(processed)
            self.movies[actor].add(movie)
            processed.add(actor)
    
    def _BFS(self,actor):
       # stack=[]
       # stack.append(actor)
        Q = queue.SimpleQueue()
        Q.put(actor)
        parent={}
        visited = {}
        for act in self.costars:
            visited[act]=False
            parent[act]=None
        visited[actor] = True
    
        while(not Q.empty()):
            u = Q.get()
        
            for v in self.costars[u]:
                if(visited[v]==False):
                    parent[v] = u
                    Q.put(v)
                    visited[v]=True
        return parent

            

    def _biBFS(self, actor1, actor2):

        if actor1 not in self.costars or actor2 not in self.costars:
            return False, None, None, None
    
        Q1 = queue.SimpleQueue()
        Q2 = queue.SimpleQueue()
        Q1.put(actor1)
        Q2.put(actor2)
    
        parent1 = {a: None for a in self.costars}
        parent2 = {a: None for a in self.costars}
    
        visited1 = {a: False for a in self.costars}
        visited2 = {a: False for a in self.costars}
    
        visited1[actor1] = True
        visited2[actor2] = True
    
        while not Q1.empty() or not Q2.empty():
    
            # expand from actor1 side
            if not Q1.empty():
                u = Q1.get()
                for v in self.costars[u]:
                    if not visited1[v]:
                        visited1[v] = True
                        parent1[v] = u
                        Q1.put(v)
    
                        if visited2[v]:
                            return True, parent1, parent2, v
    
            # expand from actor2 side
            if not Q2.empty():
                u = Q2.get()
                for v in self.costars[u]:
                    if not visited2[v]:
                        visited2[v] = True
                        parent2[v] = u
                        Q2.put(v)
    
                        if visited1[v]:
                            return True, parent1, parent2, v
    
        return False, parent1, parent2, None
    




    
    def getShortestPath(self,actor1,actor2):
        startT = time.time()
        p = self._BFS(actor1)
       
        if(actor2 not in p):
            print(actor2 +" is not in the database")
            return
        if(p[actor2]==None):
            print(actor2 + " is not connected to "+actor1)
            return
        curract = actor2
        movie = []
        actor = [actor2]
        while(curract!=actor1):
            s= p[curract]
            actor.append(s)
            l = list(self.movies[s].intersection(self.movies[curract]))
            movie.append(l[0])
            curract = s
        endT = time.time()
        print(endT-startT)
        return actor[::-1],movie[::-1]

    def biBFSGetShortestPath(self,actor1,actor2):
        startT = time.time()
        
        if(not actor1 in self.costars):
            print(actor1+ " is not in the database")
        if(not actor2 in self.costars):
            print(actor2 +" is not in the database")
        isPath,p1,p2,x = self._biBFS(actor1,actor2)

        if not isPath:
            return "There is no path from " + actor1 +" to "+actor2
        
        l1=[]
        l2=[]
        m1=[]
        m2=[]
        curract = x
        
        while(curract!=actor1):
            l1.append(curract)
            nextAct= p1[curract]
            l=list(self.movies[nextAct].intersection(self.movies[curract]))
            m1.append(l[0])
            
            curract =p1[curract]
            
        l1 = l1[1:]
        curract=x
        while(curract!=actor2):
            l2.append(curract)
            nextAct= p2[curract]
            l=list(self.movies[nextAct].intersection(self.movies[curract]))
            m2.append(l[0])
            curract=p2[curract]
        actor = [actor1]+l1[::-1] + l2[::-1]+[actor2]
        movie = m1[::-1]+m2[::-1]
        
        endT = time.time()
        print(x)
        print(endT-startT)
        return actor,movie
        
    def visualize_network(self):
        """ Visualize the actor network using NetworkX and Matplotlib """
        G = nx.Graph()
        
        # Add nodes (actors)
        for actor in self.costars:
            G.add_node(actor)
        
        # Add edges (costar relationships)
        for actor, costars in self.costars.items():
            for costar in costars:
                G.add_edge(actor, costar)
        
        # Create a circular layout for visualization
        pos = nx.circular_layout(G)
        
        # Draw the graph
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_size=8, font_weight='bold', 
                edge_color='gray')
        
        # Add title and display
        plt.title("Actor Network Visualization")
        plt.show()




    def DFS(self,actor):
       # Q = queue.SimpleQueue()
       # Q.put(actor)
        start=time.time()
        stack = []                
        stack.append(actor)

        parent={}
        visited = {}
        for act in self.costars:
            visited[act]=False
            parent[act]=None
        visited[actor] = True
    
        while(not len(stack)==0):
           # u = Q.get()
            u=stack.pop()
            for v in self.costars[u]:
                if(visited[v]==False):
                    parent[v] = u
                    stack.append(v)
                   # Q.put(v)
                    visited[v]=True
        e=time.time()
        tot=e-start
        print(tot)
        return parent

    def DFS_recursive(self, actor):
        start=time.time()
        parent = {}
        visited = {}
    
        for act in self.costars:
            visited[act] = False
            parent[act] = None
    
        def dfs(u):
            visited[u] = True
            for v in self.costars[u]:
                if not visited[v]:
                    parent[v] = u
                    dfs(v)
    
        dfs(actor)
        e=time.time()
        tot=e-start
        print(tot)
        return parent

    
    def countConnectedComponents(self):
        visited = {actor: False for actor in self.costars}
        components = 0
    
        for actor in self.costars:
            if not visited[actor]:
                components += 1
    
                # run DFS from this actor
                stack = [actor]
                visited[actor] = True
    
                while stack:
                    u = stack.pop()
                    for v in self.costars[u]:
                        if not visited[v]:
                            visited[v] = True
                            stack.append(v)
    
        return components


    