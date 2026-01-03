from collections import defaultdict
import pickle
import os

class MovieNetwork:
    def __init__(self):
        """Creates a movie similarity network"""
        # adjacency: movie -> {other_movie : weight}
        self.adjacency = defaultdict(dict)
        self.features = {}

    def getNumMovies(self):
        return len(self.adjacency)

    def getNumEdges(self):
        numEdges = 0
        for _, nbrs in self.adjacency.items():
            numEdges += len(nbrs)
        return int(numEdges / 2)

    def addMovie(self, movie, feature_set):
        """Add a movie and its feature set"""
        if movie not in self.adjacency:
            self.adjacency[movie] = {}
        self.features[movie] = set(feature_set)

    def addEdge(self, movie1, movie2, weight):
        """Add an undirected weighted edge"""
        self.adjacency[movie1][movie2] = weight
        self.adjacency[movie2][movie1] = weight


    def jaccard(self, s1, s2):
        if len(s1 | s2) == 0:
            return 0.0
        return len(s1 & s2) / len(s1 | s2)

    def buildEdges(self, threshold=0.0):
        """Compute Jaccard weights for all movie pairs"""
        movies = list(self.features.keys())

        for i in range(len(movies)):
            for j in range(i + 1, len(movies)):
                m1, m2 = movies[i], movies[j]
                w = self.jaccard(self.features[m1], self.features[m2])
                if w > threshold:
                    self.addEdge(m1, m2, w)

   

    def BFS(self, start):
        import queue
        Q = queue.SimpleQueue()
        Q.put(start)

        visited = {m: False for m in self.adjacency}
        parent  = {m: None  for m in self.adjacency}

        visited[start] = True

        while not Q.empty():
            u = Q.get()
            for v in self.adjacency[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    Q.put(v)
        return parent

    def countConnectedComponents(self):
        visited = {m: False for m in self.adjacency}
        components = 0

        for movie in self.adjacency:
            if not visited[movie]:
                components += 1
                stack = [movie]
                visited[movie] = True

                while stack:
                    u = stack.pop()
                    for v in self.adjacency[u]:
                        if not visited[v]:
                            visited[v] = True
                            stack.append(v)
        return components

    # -----------------------------
    # Similarity-specific queries
    # -----------------------------

    def mostSimilar(self, movie, k=5):
        """Return top-k most similar movies"""
        return sorted(
            self.adjacency[movie].items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

    # -----------------------------
    # Persistence
    # -----------------------------

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)


            

#A very high Jaccard weight means the two movies share most of their features and are very similar under 
#the chosen feature set.