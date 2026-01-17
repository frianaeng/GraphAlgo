from collections import defaultdict
import pickle
import os

class ActorMovieNetwork:
    def __init__(self):
        """Creates a bipartite actor–movie network"""
        self.movie_to_actors = defaultdict(set)  # movie -> actors
        self.actor_to_movies = defaultdict(set)  # actor -> movies

    # -------------------------
    # Counts
    # -------------------------

    def getNumMovies(self):
        return len(self.movie_to_actors)

    def getNumActors(self):
        return len(self.actor_to_movies)

    def getNumEdges(self):
        """Each edge is one (actor, movie) appearance"""
        return sum(len(actors) for actors in self.movie_to_actors.values())

    # -------------------------
    # Construction
    # -------------------------

    def addAppearance(self, movie, actor):
        """Add an actor–movie edge"""
        self.movie_to_actors[movie].add(actor)
        self.actor_to_movies[actor].add(movie)

    # -------------------------
    # Queries
    # -------------------------

    def getActors(self, movie):
        return self.movie_to_actors.get(movie, set())

    def getMovies(self, actor):
        return self.actor_to_movies.get(actor, set())

    def degreeMovie(self, movie):
        return len(self.getActors(movie))

    def degreeActor(self, actor):
        return len(self.getMovies(actor))

    def getConnectedComponentSizes(self):
        visited_actors = set()
        visited_movies = set()
        sizes = []
    
        for actor in self.actor_to_movies:
            if actor in visited_actors:
                continue
    
            stack = [("actor", actor)]
            visited_actors.add(actor)
            size = 0
    
            while stack:
                kind, node = stack.pop()
                size += 1
    
                if kind == "actor":
                    for movie in self.actor_to_movies[node]:
                        if movie not in visited_movies:
                            visited_movies.add(movie)
                            stack.append(("movie", movie))
                else:
                    for a in self.movie_to_actors[node]:
                        if a not in visited_actors:
                            visited_actors.add(a)
                            stack.append(("actor", a))
    
            sizes.append(size)
    
        return sizes


    # -------------------------
    # Persistence
    # -------------------------

    def save(self, path):
        """Serialize the object using pickle"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)

#Bipartite graph, Undirected, Unweighted