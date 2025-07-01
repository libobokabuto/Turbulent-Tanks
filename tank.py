import pygame

class Tank:
    """
    坦克模块：管理坦克状态、运动、方向及射击逻辑。
    负责人: libobokabuto
    """
    def __init__(self, id: int, x: int, y: int, color: tuple,
                 is_ai: bool = False, cell_size: int = 100):
        """
        初始化坦克属性。
        Args:
            id (int): 坦克的唯一编号。
            x (int): 初始 X 坐标（像素）。
            y (int): 初始 Y 坐标（像素）。
            color (tuple): 坦克颜色 (RGB)。
            is_ai (bool): 是否为 AI 控制，默认 False。
            cell_size (int): 地图单元格大小，用于碰撞检测，默认 100。
        """
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.is_ai = is_ai
        self.size = 30
        self.speed = 2
        self.direction = 'UP'
        self.cooldown = 0
        self.cooldown_max = 30
        self.alive = True
        self.cell_size = cell_size
        # 存储每次移动时用于检测的碰撞点
        self.debug_points = []

    def move(self, dx: int, dy: int, game_map, cell_size: int = None):
        """
        尝试移动坦克，并在移动方向遇到墙时停止。
        负责人: libobokabuto
        Args:
            dx (int): 横向移动量，正数向右，负数向左。
            dy (int): 纵向移动量，正数向下，负数向上。
            game_map (Game_map): 地图对象，用于获取格子和墙信息。
            cell_size (int, optional): 单元格像素大小，若不传则使用实例属性。
        """
        # 选用传入尺寸或实例属性
        cs = cell_size if cell_size is not None else self.cell_size
        # 重置调试点
        self.debug_points = []

        # —— 水平移动检测 —— 
        if dx != 0:
            new_x = self.x + dx
            for y_off in (1, self.size - 1):
                edge_x = new_x + (self.size if dx > 0 else 0)
                edge_y = self.y + y_off
                self.debug_points.append((edge_x, edge_y))

                cx = int(edge_x) // cs
                cy = int(edge_y) // cs
                # 出界就停
                if not (0 <= cx < game_map.width and 0 <= cy < game_map.height):
                    break
                cell = game_map.grid[cy][cx]
                # ▶️ 向右检测东墙 E，向左检测西墙 W
                if (dx > 0 and cell.walls['E']) or (dx < 0 and cell.walls['W']):
                    break
            else:
                # 两个检测点都没碰墙，真正更新位置
                self.x = new_x

        # —— 垂直移动检测 —— 
        if dy != 0:
            new_y = self.y + dy
            for x_off in (1, self.size - 1):
                edge_x = self.x + x_off
                edge_y = new_y + (self.size if dy > 0 else 0)
                self.debug_points.append((edge_x, edge_y))

                cx = int(edge_x) // cs
                cy = int(edge_y) // cs
                if not (0 <= cx < game_map.width and 0 <= cy < game_map.height):
                    break
                cell = game_map.grid[cy][cx]
                # ▶️ 向下检测南墙 S，向上检测北墙 N
                if (dy > 0 and cell.walls['S']) or (dy < 0 and cell.walls['N']):
                    break
            else:
                self.y = new_y

    def update(self, game_map, bullet_manager):
        """
        更新坦克状态，比如冷却计时和 AI 行为。
        负责人: libobokabuto
        """
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.is_ai:
            # AI 行为扩展点
            pass

    def rotate(self, direction: str):
        """
        改变坦克朝向方向。
        负责人: libobokabuto
        Args:
            direction (str): 'UP'/'DOWN'/'LEFT'/'RIGHT'。
        """
        if direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            self.direction = direction

    def shoot(self, bullet_manager):
        """
        发射子弹，触发冷却。
        负责人: libobokabuto
        Args:
            bullet_manager (BulletManager): 子弹管理器，用于 spawn。
        """
        if self.cooldown == 0:
            bullet_manager.spawn(
                self.x + self.size // 2,
                self.y + self.size // 2,
                self.direction,
                self.id
            )
            self.cooldown = self.cooldown_max

    def get_rect(self) -> pygame.Rect:
        """
        获取坦克当前位置的矩形对象，用于碰撞检测。
        Returns:
            pygame.Rect
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_center(self) -> tuple:
        """
        获取坦克中心坐标。
        Returns:
            tuple: (x, y)
        """
        return self.get_rect().center

    def reset(self, position: tuple):
        """
        重置坦克位置和状态。
        负责人: libobokabuto
        Args:
            position (tuple): 新位置坐标 (x, y)。
        """
        self.x, self.y = position
        self.direction = 'UP'
        self.cooldown = 0
        self.alive = True
