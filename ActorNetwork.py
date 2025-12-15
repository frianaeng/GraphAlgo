import pandas as pd
from collections import defaultdict
import queue
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

    def loadDataSet(self, pthToFile):
        """ Given file name of a dataset """

        df = pd.read_csv("name.basics.tsv", sep = "\t")
        subdf = df[:1000]
        # movieDict <movieTitle> -> <set<actors>>
        movieDict = defaultdict(set)
        for row,col in subDf.iterrows():
            actor = col["primaryName"]
            titles = col["knownForTitles"].split(",")
            for title in titles:
                movieDict[title].add(actor)

    def addMovie(self, movie, actors):
        """ Add a movie (string) and a set<actors> string to the network """
        processed = set()
        yetToProcess = actors
        while yetToProcess: # Is only true when actors is non-empty
            actor = yetToProcess.pop()
            self.costars[actor] = self.costars[actor].union(yetToProcess).union(processed)
            self.movies[actor].add(movie)
            processed.add(actor)

    def BFS(self,actor):
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
                    visited[u]=True
        return parent

    def getShortestPath(self,actor1,actor2):
        startT = time.time()
        p = self.BFS(actor1)
        if(actor2 not in p):
            print(actor2 +" is not in the database")
        if(p[actor2]==None):
            print(actor2 + " is not in the same network")
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
        return actor,movie





if __name__ == "__main__":
    print('hello world')
