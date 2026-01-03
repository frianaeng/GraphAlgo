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

    # -------------------------
    # Persistence
    # -------------------------

    def save(self, path):
        """Serialize the object using pickle"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)

#Bipartite graph, Undirected, Unweighted