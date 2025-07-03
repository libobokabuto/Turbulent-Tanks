import random
import config
import pymunk
import math

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
    """
    地图模块，负责生成和管理迷宫地图。
    """
    def __init__(self, debug = False):
        """
        此函数初始化一个 Game_map 对象，可指定大小或随机生成一个横向的矩形迷宫。
        负责人:Thousand
        Args:
            width (int): 迷宫宽度，随机生成 5-8。
            height (int): 迷宫高度，随机生成 4-5。
            extra_walls (int): 拆除的内墙数，默认为prim探索后剩余墙数的10%
        """
        if not debug:
            self.MAX_WIDTH           = config.MAX_MAP_WIDTH
            self.MIN_WIDTH           = config.MIN_MAP_WIDTH
            self.MAX_HEIGHT          = config.MAX_MAP_HEIGHT
            self.MIN_HEIGHT          = config.MIN_MAP_HEIGHT
            self.INNER_WALLS_PERCENT = config.INNER_WALLS_PERCENT
            self.y_offset            = config.Y_OFFSET
            self.wall_elasticity     = config.WALL_ELASTICITY
            self.friction            = config.WALL_FRICTION
        else:
            self.MAX_WIDTH           = 8
            self.MIN_WIDTH           = 5
            self.MAX_HEIGHT          = 5
            self.MIN_HEIGHT          = 5
            self.INNER_WALLS_PERCENT = 0.1
            self.y_offset            = 15
            self.wall_elasticity     = 1.0
            self.wall_friction       = 0.0

        # 初始化格子矩阵
        self.width = random.randint(self.MIN_WIDTH, self.MAX_WIDTH)
        self.height = random.randint(self.MIN_HEIGHT, self.MAX_HEIGHT)
        # 随机生成宽度和高度，范围在MIN和MAX之间
        self.extra_walls = round(self.INNER_WALLS_PERCENT * (self.width - 1) * (self.height - 1))
        # 拆除的墙数为prim探索后剩余墙数的INNER_WALLS_PERCENT%
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
    
    def create_static_walls(self, space, ui):
        static_body = space.static_body
        ts = ui.TILE_SIZE[self.height]
        xo = (ui.SCREEN_WIDTH - self.width * ts) // 2
        yo = self.y_offset

        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                x0 = col_idx * ts + xo
                y0 = row_idx * ts + yo
                for dir_key, (p1, p2) in {
                    'N': ((x0, y0), (x0 + ts, y0)),
                    'S': ((x0, y0 + ts), (x0 + ts, y0 + ts)),
                    'W': ((x0, y0), (x0, y0 + ts)),
                    'E': ((x0 + ts, y0), (x0 + ts, y0 + ts))
                }.items():
                    if cell.walls[dir_key]:
                        seg = pymunk.Segment(static_body, p1, p2, ui.WALL_WIDTH / 2)
                        seg.elasticity = self.wall_elasticity
                        seg.friction = self.wall_friction
                        space.add(seg)

    def get_spawn_points(self, num_players: int, ui) -> list[tuple[float, float]]:
        """
        计算 num_players 个互相距离尽可能远的出生点。（像素坐标）
        Args:
            num_players (int): 玩家 / 坦克数量
            ui (UI): 用来拿 TILE_SIZE 与屏幕偏移量
        Returns:
            List[(x, y)]
        """
        ts = ui.TILE_SIZE[self.height]
        x_off = (ui.SCREEN_WIDTH - self.width * ts) // 2
        y_off = ui.Y_OFFSET

        # ① 把所有格子中心收集成候选点
        candidates = [
            (col * ts + x_off + ts / 2,
             row * ts + y_off + ts / 2)
            for row in range(self.height)
            for col in range(self.width)
        ]

        # ② 选择首个随机点
        spawn_pts = [random.choice(candidates)]
        candidates.remove(spawn_pts[0])

        # ③ 依次挑“离已有点最远”的格子
        while len(spawn_pts) < num_players and candidates:
            # 对每个候选点，算它到已选点的最小距离
            dist_to_nearest = [
                min(math.hypot(cx - sx, cy - sy) for sx, sy in spawn_pts)
                for cx, cy in candidates
            ]
            # 取该最小距离最大的那个点
            idx = dist_to_nearest.index(max(dist_to_nearest))
            spawn_pts.append(candidates.pop(idx))

        return spawn_pts