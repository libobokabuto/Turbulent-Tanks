#子弹模块
import pygame

class Bullet:
    def __init__(self, x: int, y: int, direction: str, owner_id: int, cell_size: int = 100):
        """
        初始化子弹属性
        负责人: wobudao1a​
        Args:
            x (int): 初始x坐标
            y (int): 初始y坐标
            direction (str): 移动方向（'UP'/'DOWN'/'LEFT'/'RIGHT'）
            owner_id (int): 发射者ID
            cell_size (int): 每个格子像素大小（用于撞墙检测），默认为 100
        """
        self.x = x
        self.y = y
        
        self.speed = 5
        self.radius = 3
        self.color = (255, 0, 0)
        self.alive = True
        self.owner = owner_id
        self.cell_size = cell_size
        # 方向向量
        dirs = {
            'UP':    (0, -1),
            'DOWN':  (0,  1),
            'LEFT':  (-1, 0),
            'RIGHT': (1,  0)
        }
        self.dx, self.dy = dirs[direction]
        self.speed = 5

    def update(self, game_map):
        """
        更新子弹移动和墙壁碰撞
        负责人: wobudao1a​
        Args:
            game_map (Game_map): 地图对象
        """
        # 先算出下一个位置
        next_x = self.x + self.dx * self.speed
        next_y = self.y + self.dy * self.speed

        # 计算下一个点所在格子
        cx = int(next_x) // self.cell_size
        cy = int(next_y) // self.cell_size

        # 如果越出地图边界，子弹消亡
        if not (0 <= cx < game_map.width and 0 <= cy < game_map.height):
            self.alive = False
            return

        cell = game_map.grid[cy][cx]
        # 水平分量：右撞东墙 or 左撞西墙 → 反转 dx
        if self.dx > 0 and cell.walls['E'] and next_x + self.radius >= (cx + 1)*self.cell_size:
            self.dx = -self.dx
        elif self.dx < 0 and cell.walls['W'] and next_x - self.radius <= cx*self.cell_size:
            self.dx = -self.dx

        # 垂直分量：下撞南墙 or 上撞北墙 → 反转 dy
        if self.dy > 0 and cell.walls['S'] and next_y + self.radius >= (cy + 1)*self.cell_size:
            self.dy = -self.dy
        elif self.dy < 0 and cell.walls['N'] and next_y - self.radius <= cy*self.cell_size:
            self.dy = -self.dy

        # 应用移动
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def check_collision(self, tanks: list) -> bool:
        """
        检测与坦克的碰撞
        负责人: wobudao1a​
        Args:
            tanks (list): 所有坦克对象列表
        Returns:
            bool: 是否命中
        """
        for tank in tanks:
            if tank.id != self.owner and tank.get_rect().collidepoint(self.x, self.y):
                self.alive = False
                tank.alive = False
                return True
        return False

    def draw(self, screen):
        """
        绘制圆形子弹
        负责人: wobudao1a​
        Args:
            screen (pygame.Surface): 绘制目标表面
        """
        

        if self.alive:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)