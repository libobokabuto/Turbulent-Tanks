#子弹模块
class Bullet:
    def __init__(self, x: int, y: int, direction: str, owner_id: int):
        """
        初始化子弹属性
        负责人: wobudao1a​
        Args:
            x (int): 初始x坐标
            y (int): 初始y坐标
            direction (str): 移动方向（'UP'/'DOWN'/'LEFT'/'RIGHT'）
            owner_id (int): 发射者ID
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 5
        self.radius = 3
        self.color = (255, 0, 0)
        self.alive = True
        self.owner = owner_id

    def update(self, game_map):
        """
        更新子弹移动和墙壁碰撞
        负责人: wobudao1a​
        Args:
            game_map (Game_map): 地图对象
        """
        dirs = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        dx, dy = dirs[self.direction]
        self.x += dx * self.speed
        self.y += dy * self.speed

        # 边界检测
        if not (0 <= self.x < game_map.width*100 and 0 <= self.y < game_map.height*100):
            self.alive = False

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
                return True
        return False

    def draw(self, screen):
        """
        绘制圆形子弹
        负责人: wobudao1a​
        Args:
            screen (pygame.Surface): 绘制目标表面
        """
        for bullet in self.bullets:
            bullet.draw(screen)

        if self.alive:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)