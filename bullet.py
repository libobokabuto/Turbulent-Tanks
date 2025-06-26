#子弹模块
class Bullet:
    def __init__(self, x: int, y: int, direction: int, owner_id: int):
        """
        初始化子弹位置、方向、发射者ID。
        """

    def update(self, game_map):
        """
        更新子弹移动和反弹逻辑。
        """

    def check_collision(self, tanks: list) -> bool:
        """
        检查是否击中某个坦克。
        返回值：是否命中。
        """

    def draw(self, screen):
        """
        将子弹绘制到屏幕上。
        """

class BulletManager:
    def __init__(self):
        """
        管理所有子弹的创建与状态更新。
        """

    def spawn(self, x: int, y: int, direction: int, owner_id: int):
        """
        创建新子弹对象加入管理列表。
        """

    def update(self, game_map, tanks: list):
        """
        批量更新所有子弹的状态与碰撞处理。
        """

    def draw(self, screen):
        """
        批量绘制所有子弹。
        """

    def clear(self):
        """
        清空所有子弹（用于游戏重启）。
        """
