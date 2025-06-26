#坦克模块
class Tank:
    def __init__(self, id: int, x: int, y: int, color: tuple, is_ai: bool = False):
        """
        初始化坦克属性，包括位置、颜色、是否为AI等。
        """

    def update(self, game_map, bullet_manager):
        """
        更新坦克状态，如移动、与地图交互、冷却倒计时等。
        """

    def shoot(self, bullet_manager):
        """
        尝试发射一枚子弹（考虑冷却时间）。
        """

    def draw(self, screen):
        """
        将坦克绘制到屏幕上。
        """

    def get_rect(self) -> pygame.Rect:
        """
        返回用于碰撞检测的矩形区域。
        """

    def reset(self, position: tuple):
        """
        重置坦克位置（用于重生等）。
        """
