#地图模块
class GameMap:
    def __init__(self):
        """
        初始化地图对象，加载地图数据。
        """
    
    def load_map(self) -> list:
        """
        加载地图二维数组（可以是静态/随机）。
        返回值：地图二维列表。
        """
    
    def is_wall(self, x: int, y: int) -> bool:
        """
        判断给定像素坐标是否为墙体，用于碰撞检测。
        """
    
    def draw(self, screen):
        """
        将地图绘制到屏幕上。
        """
    
    def get_spawn_points(self) -> list:
        """
        获取所有坦克出生点坐标，用于重生或初始化。
        """
