import heapq
import pygame as pg

class A_Star:
    def __init__(cls):
        cls.title = "A* Path Finding Algorithm"
        cls.name = "A*"

    def h(cls, p1, p2):
        """
        Uses Manhattan Distance as a heuristic distance
        """
        x1, y1 = p1
        x2, y2 = p2
        return (abs(x1 - x2) + abs(y1 - y2)) * 2

    def construct_path(cls, preceding, start, end, draw):
        curr = end
        while curr in preceding:
            curr = preceding[curr]
            if curr != start and curr != end:
                curr.set_status("PATH")
            draw()

    def run(cls, start, end, grid, draw):
        draw()
        for row in grid:
            for cell in row:
                cell.update_neighbors(grid)

        count = 0
        #          f_score, tie_breaker, cell
        open_q = [ (0, count, start) ]
        in_open = { start }
        preceding = {}
        g_scores = { cell: float('inf') for row in grid for cell in row }
        g_scores[start] = 0
        f_scores = { cell: float('inf') for row in grid for cell in row }
        f_scores[start] = cls.h(start.pos, end.pos)

        while open_q:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            curr = heapq.heappop(open_q)[2]
            in_open.remove(curr)
            if curr == end:
                cls.construct_path(preceding, start, end, draw)
                return True
            
            for neighbor in curr.neighbors:
                tmp_g_score = g_scores[curr] + neighbor.weight
                if tmp_g_score < g_scores[neighbor]:
                    preceding[neighbor] = curr
                    g_scores[neighbor] = tmp_g_score
                    f_scores[neighbor] = tmp_g_score + cls.h(neighbor.pos, end.pos)
                    if neighbor not in in_open:
                        count += 1
                        heapq.heappush( open_q, (f_scores[neighbor], count, neighbor) )
                        in_open.add(neighbor)
                        if neighbor != end:
                            neighbor.set_status("OPEN")                        
            draw()
            if curr != start:
                curr.set_status("CLOSED")

        return False