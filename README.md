# Graph Algos

Graph algos when looking at the imdb network

## Functionality

Actors are represented as nodes, and an undirected edge exists between two actors if they have appeared in the same movie. The network is stored using two dictionaries: one for costars one for movies.

The function addMovie adds a movie and updates all pairwise co-starring relationships where each actor is connected to every other actor in the same movie.
This updates both self.costars and self.movies.

getNumActors() – Returns the total number of actors (nodes).
getNumConnections() – Returns the total number of unique co-starring relationships (edges). Internally divides by 2 to account for undirected duplication.

BFS(actor) – Performs a breadth-first search starting from a given actor.

getShortestPath(actor1, actor2) for BFS finds the shortest co-starring path between two actors.

Run BFS starting from actor1

Check reachability of actor2

Backtrack using the parent map

For each actor transition, determine a connecting movie

biBFS(actor1, actor2) attempts to find a shortest path using bidirectional BFS.
Maintains two queues, two visited maps, and two parent maps. Expands from both ends until an intersection is found.

visualize_network() uses NetworkX and Matplotlib to visualize the actor graph.
Actors are nodes. Co-starring relationships are edges.

getShortestPathBidirectionalBFS(actor1, actor2)
This method computes a shortest co-starring path between two actors using bidirectional breadth-first search (bi-BFS). Unlike standard BFS which expands outward from a single source, bidirectional BFS performs two simultaneous searches: one starting from actor1, one starting from actor2.

Two queues are maintained, one for each search direction. Two visited maps track explored actors from each side. Two parent maps store predecessor relationships. At each step, the algorithm expands one level from each frontier. When a node is discovered by both searches, a meeting point is found.
