import random
import pygame

class Cell:
    """
    迷宫中的一个格子类，包含四条边墙和访问状态。
    """
    def __init__(self):
        """
        此函数初始化一个格子对象，四条边墙初始都存在，格子未被访问。
        负责人:Thousand
        """
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False

class Game_map:
    def __init__(self, width = None, height = None, extra_walls = None):
        """
        此函数初始化一个 Game_map 对象，可指定大小或随机生成一个横向的矩形迷宫。
        负责人:Thousand
        Args:
            width (int): 迷宫宽度，默认为 None 时随机生成 4-9。
            height (int): 迷宫高度，默认为 None 时为 width- 0~2 (最小为4)。
            extra_walls (int): 拆除的内墙数，默认为 None 时为prim探索后剩余墙数的30%
        """
        # 初始化格子矩阵
        self.width = random.randint(4,9)if width is None else width
        self.height = self.width - random.randint(0,2)if height is None else height
        # 不指定参数时，随机生成宽度为4-9，高度为宽度-0~2的矩形迷宫，保证地图为横向
        if self.height < 4:
            self.height = 4# 保证高度至少为4
        self.extra_walls = round(0.3 * (self.width - 1) * (self.height - 1)) if extra_walls is None else extra_walls
        # 拆除的墙数为prim探索后剩余墙数的30%
        self.grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        # 按行生成，也就是先左右再上下，这里很重要，后续访问格子也是按照第几行第几列的顺序访问

    def random_break_walls(self, count):
        """
        此函数从当前还存在的内墙中随机拆除 count 堵，避免单一路线。
        负责人:Thousand
        Args:
            count (int): 要拆除的墙数，若大于剩余墙数，则拆除所有剩余墙。
        """
        # 收集所有仍留存的可拆内墙（去掉边界外的墙）
        candidates = []
        for y in range(self.height):
            for x in range(self.width):
                for dir, (dx, dy) in {
                    'N': (0, -1), 'S': (0, 1),
                    'W': (-1, 0), 'E': (1, 0)
                }.items():
                    # 先从左到右，再由上而下，每个格子的四个方向构成的三重循环
                    if self.grid[y][x].walls[dir]:
                        # 如果这个格子在某个方向有墙，则执行一次对邻居的判断，若邻居在边界范围内，则将这堵墙加入待拆列表
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            candidates.append((x, y, dir, nx, ny))

        # 从待拆列表中不重复的抽取count堵墙或者全部墙
        to_remove = random.sample(candidates, min(count, len(candidates)))

        for x, y, dir, nx, ny in to_remove:
            # 拆除双向墙
            self.grid[y][x].walls[dir] = False
            opp = {'N':'S','S':'N','E':'W','W':'E'}[dir]# 方向反转
            self.grid[ny][nx].walls[opp] = False

    def generate_map(self):
        """
        此函数用随机普利姆算法打通格子之间的墙，生成一个完美迷宫。
        随后随机拆除几堵内墙，为地图增加多种路线。
        负责人:Thousand
        Returns:
            grid (list[list[Cell]]): 生成的迷宫格子数据，格式为二维列表。
        """
        def neighbors(x, y):
            for direction, (dx, dy) in {# 映射四个方向到(dx,dy),步长为1
                'N': (0, -1), 'S': (0, 1),
                'W': (-1, 0), 'E': (1, 0)
            }.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:# 若邻居格子处于边界内，则yield一组(direction, nx, ny)
                    yield direction, nx, ny

        # 从 左上角(0,0) 开始
        sx, sy = 0, 0
        self.grid[sy][sx].visited = True

        # 初始化 frontier，即为当前格子候选拆除的边界
        frontier = []
        for dir, nx, ny in neighbors(sx, sy):# 遍历当前格子四个方向合法的邻居格子
            frontier.append((sx, sy, dir, nx, ny))

        # 随机 Prim
        while frontier:
            cx, cy, dir, nx, ny = frontier.pop(random.randrange(len(frontier)))# 随机选择一个边界墙
            if not self.grid[ny][nx].visited:# 如果邻居格子未被访问
                self.grid[cy][cx].walls[dir] = False # 打通当前格子的 dir 方向边界墙
                opposite = {'N':'S','S':'N','E':'W','W':'E'}[dir]
                self.grid[ny][nx].walls[opposite] = False # 反过来拆除邻居格子的对应边界墙

                self.grid[ny][nx].visited = True # 标记为已访问，并将新格子的所有边加入 frontier
                for ndir, nnx, nny in neighbors(nx, ny):
                    if not self.grid[nny][nnx].visited:
                        frontier.append((nx, ny, ndir, nnx, nny))
        
        if self.extra_walls > 0:
            self.random_break_walls(self.extra_walls)

        return self.grid