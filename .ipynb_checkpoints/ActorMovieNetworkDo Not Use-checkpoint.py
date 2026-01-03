{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "0930cb24-2caf-4797-bd58-e7d40e82ae08",
   "metadata": {},
   "outputs": [],
   "source": [
    "from collections import defaultdict\n",
    "import pickle\n",
    "import os\n",
    "\n",
    "class ActorMovieNetwork:\n",
    "    def __init__(self):\n",
    "        \"\"\"Creates a bipartite actor–movie network\"\"\"\n",
    "        self.movie_to_actors = defaultdict(set)  # movie -> actors\n",
    "        self.actor_to_movies = defaultdict(set)  # actor -> movies\n",
    "\n",
    "    # -------------------------\n",
    "    # Counts\n",
    "    # -------------------------\n",
    "\n",
    "    def getNumMovies(self):\n",
    "        return len(self.movie_to_actors)\n",
    "\n",
    "    def getNumActors(self):\n",
    "        return len(self.actor_to_movies)\n",
    "\n",
    "    def getNumEdges(self):\n",
    "        \"\"\"Each edge is one (actor, movie) appearance\"\"\"\n",
    "        return sum(len(actors) for actors in self.movie_to_actors.values())\n",
    "\n",
    "    # -------------------------\n",
    "    # Construction\n",
    "    # -------------------------\n",
    "\n",
    "    def addAppearance(self, movie, actor):\n",
    "        \"\"\"Add an actor–movie edge\"\"\"\n",
    "        self.movie_to_actors[movie].add(actor)\n",
    "        self.actor_to_movies[actor].add(movie)\n",
    "\n",
    "    # -------------------------\n",
    "    # Queries\n",
    "    # -------------------------\n",
    "\n",
    "    def getActors(self, movie):\n",
    "        return self.movie_to_actors.get(movie, set())\n",
    "\n",
    "    def getMovies(self, actor):\n",
    "        return self.actor_to_movies.get(actor, set())\n",
    "\n",
    "    def degreeMovie(self, movie):\n",
    "        return len(self.getActors(movie))\n",
    "\n",
    "    def degreeActor(self, actor):\n",
    "        return len(self.getMovies(actor))\n",
    "\n",
    "    # -------------------------\n",
    "    # Persistence\n",
    "    # -------------------------\n",
    "\n",
    "    def save(self, path):\n",
    "        \"\"\"Serialize the object using pickle\"\"\"\n",
    "        os.makedirs(os.path.dirname(path), exist_ok=True)\n",
    "        with open(path, \"wb\") as f:\n",
    "            pickle.dump(self, f)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "792bf668-525d-48f9-8950-f354642052e0",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Bipartite graph, Undirected, Unweighted"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:anaconda3]",
   "language": "python",
   "name": "conda-env-anaconda3-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
