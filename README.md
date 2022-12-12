# Solving a Weighted 8-puzzle Problem with Search

Implementation of 8 puzzle board solvers using either BFS or A* with the various heiuristic functions to discover the best solution.
The 8-puzzle consists of eight tiles on a 3x3 grid, with one open blank spot. The goal state consists of the open square in the upper left, with the other tiles arranged in numeric order from left to right. Valid moves are Up, Down, Left, and Right, which shift a tile into the open square. Depending on the position of the open square, not all of those moves may be available. The solver must take a start state as input, perform a search over the state space, and return a solution path to the goal states when possible.
