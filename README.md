# maze
Laboratory 12.3

## Description
Implementation of the maze ADT using C-based arrays and stacks (linked-based).

## Example
```python
>>> maze = Maze(5, 5)
>>> maze = buildMaze("mazefile.txt")
>>> print(maze)
* * * * * 
* _ * _ * 
* _ _ _ * 
* _ * _ _ 
_ _ * * * 
>>> maze.findPath()
True
>>> print(maze)
* * * * * 
* o * o * 
* x x x * 
* x * x x 
_ x * * * 
>>> maze.reset()
>>> print(maze)
* * * * * 
* _ * _ * 
* _ _ _ * 
* _ * _ _ 
_ _ * * * 
```
