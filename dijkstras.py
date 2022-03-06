import heapq

class Dijkstras:
    def __init__(cls):
        cls.title = "Dijkstra's Path Finding Algorithm"
        cls.name = "Dijkstra's"
        
    def construct_path(cls, preceding, start, end, draw):
        curr = end
        while curr.pos in preceding:
            curr = preceding[curr.pos]
            if curr != start and curr != end:
                curr.set_status("PATH")
            draw()

    def run(cls, start, end, grid, draw):
        draw()
        for row in grid:
            for cell in row:
                cell.update_neighbors(grid)

        count = 0
        qq = [ (0, count, start) ]
        visited = set()
        dists = { 
            (i, j): float('inf') for i in range(len(grid)) 
                                    for j in range(len(grid[i])) 
        }
        dists[start.pos] = 0
        preceding = {}

        while qq:
            d, _, cell = heapq.heappop(qq)
            if cell.pos in visited:
                if cell != start and cell != end:
                    cell.set_status("VISITED")
                continue

            if cell == end:
                cls.construct_path(preceding, start, end, draw)
                return True

            visited.add(cell.pos)
            if cell != start:
                cell.set_status("LOOK")
            for neighbor in cell.neighbors:
                count += 1
                pos = neighbor.pos
                if neighbor.weight + d < dists[pos]:
                    dists[pos] = neighbor.weight + d
                    preceding[pos] = cell
                heapq.heappush( qq, (dists[pos], count, neighbor) )
                if neighbor != start and neighbor != end:
                    neighbor.set_status("OPEN")
            draw()
            if cell != start and cell != end:
                cell.set_status("VISITED")
