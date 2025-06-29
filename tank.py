#坦克模块
# tank.py
import pygame

class Tank:
    def __init__(self, id: int, x: int, y: int, color: tuple, is_ai: bool = False):
        """
        初始化函数
        负责人: libobokabuto
        Args:
            id (int): 坦克的唯一编号。
            x (int): 初始X坐标位置。
            y (int): 初始Y坐标位置。
            color (tuple): 坦克显示的颜色（RGB元组）。
            is_ai (bool): 是否为AI控制，默认为False。
        Returns:
            None
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

    def update(self, game_map, bullet_manager):
        """
        更新坦克状态，如冷却计数和AI逻辑。
        负责人: libobokabuto
        Args:
            game_map (Game_map): 地图对象。
            bullet_manager (BulletManager): 子弹管理器。
        Returns:
            None
        """
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.is_ai:
            pass  # AI行为可在此拓展

    def move(self, dx, dy, game_map, cell_size=100):
        """
        尝试移动坦克并检测是否撞墙。
        负责人: libobokabuto
        Args:
            dx (int): x方向移动量。
            dy (int): y方向移动量。
            game_map (Game_map): 地图对象。
            cell_size (int): 每格像素尺寸。
        Returns:
            None
        """
        new_x = self.x + dx
        new_y = self.y + dy

        cx, cy = self.x // cell_size, self.y // cell_size
        grid = game_map.grid
        if 0 <= cx < game_map.width and 0 <= cy < game_map.height:
            cell = grid[cy][cx]
            if dy < 0 and cell.walls['N']: return
            if dy > 0 and cell.walls['S']: return
            if dx < 0 and cell.walls['W']: return
            if dx > 0 and cell.walls['E']: return

        self.x = new_x
        self.y = new_y

    def rotate(self, direction):
        """
        改变坦克方向。
        负责人: libobokabuto
        Args:
            direction (str): 'UP'/'DOWN'/'LEFT'/'RIGHT'之一。
        Returns:
            None
        """
        if direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            self.direction = direction

    def shoot(self, bullet_manager):
        """
        发射子弹。
        负责人: libobokabuto
        Args:
            bullet_manager (BulletManager): 子弹管理器。
        Returns:
            None
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
        返回坦克当前的矩形区域。
        负责人: libobokabuto
        Returns:
            pygame.Rect: 用于碰撞检测。
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_center(self):
        """
        获取坦克中心坐标。
        负责人: libobokabuto
        Returns:
            tuple: 中心坐标(x, y)。
        """
        return self.get_rect().center

    def reset(self, position: tuple):
        """
        重设坦克位置与状态。
        负责人: libobokabuto
        Args:
            position (tuple): 重生坐标(x, y)。
        Returns:
            None
        """
        self.x, self.y = position
        self.direction = 'UP'
        self.cooldown = 0