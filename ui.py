import pygame
from map import Game_map

class UI:
    """
    用户界面模块：负责处理输入及图形渲染。
    """
    def __init__(self, cell_size=100, wall_color=(200, 200, 200), wall_width=2, bg_color=(255, 255, 255)):
        """
        初始化 UI，设置绘制参数。
        负责人: Thousand
        Args:
            cell_size (int): 每个格子的像素大小。
            wall_color (tuple): 墙壁颜色（RGB）。
            wall_width (int): 墙壁宽度。
            bg_color (tuple): 背景色。
        Returns:
            None
        """
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.wall_width = wall_width
        self.bg_color = bg_color
        # 调试时存储碰撞检测点
        self.debug_points = []

    def handle_input(self, player_tank, game_map):
        """
        处理玩家按键输入，控制坦克的移动与旋转。
        负责人: libobokabuto
        Args:
            player_tank (Tank): 玩家控制的坦克对象。
            game_map (Game_map): 地图对象。
        Returns:
            dict: 当前帧的操作状态字典。
        """
        keys = pygame.key.get_pressed()
        actions = {
            "UP": keys[pygame.K_w] or keys[pygame.K_UP],
            "DOWN": keys[pygame.K_s] or keys[pygame.K_DOWN],
            "LEFT": keys[pygame.K_a] or keys[pygame.K_LEFT],
            "RIGHT": keys[pygame.K_d] or keys[pygame.K_RIGHT],
            "SHOOT": keys[pygame.K_SPACE],
            "SWITCH_MENU": False
        }
        # 只负责返回操作状态，真正移动和射击由主循环处理
        return actions

    def draw_map(self, screen, grid):
        """
        绘制迷宫地图并可视化墙体的碰撞盒。
        负责人: Thousand
        Args:
            screen (pygame.Surface): 绘制目标画布。
            grid (list[list[Cell]]): 迷宫格子数据。
        Returns:
            None
        """
        screen.fill(self.bg_color)
        half = self.wall_width // 2
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                x0 = x * self.cell_size
                y0 = y * self.cell_size

                # 北墙
                if cell.walls['N']:
                    pygame.draw.line(screen, self.wall_color,
                                     (x0, y0), (x0 + self.cell_size, y0),
                                     self.wall_width)
                    rect = pygame.Rect(x0, y0 - half,
                                       self.cell_size, self.wall_width)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
                # 南墙
                if cell.walls['S']:
                    py = y0 + self.cell_size
                    pygame.draw.line(screen, self.wall_color,
                                     (x0, py), (x0 + self.cell_size, py),
                                     self.wall_width)
                    rect = pygame.Rect(x0, py - half,
                                       self.cell_size, self.wall_width)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
                # 西墙
                if cell.walls['W']:
                    pygame.draw.line(screen, self.wall_color,
                                     (x0, y0), (x0, y0 + self.cell_size),
                                     self.wall_width)
                    rect = pygame.Rect(x0 - half, y0,
                                       self.wall_width, self.cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
                # 东墙
                if cell.walls['E']:
                    px = x0 + self.cell_size
                    pygame.draw.line(screen, self.wall_color,
                                     (px, y0), (px, y0 + self.cell_size),
                                     self.wall_width)
                    rect = pygame.Rect(px - half, y0,
                                       self.wall_width, self.cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)

        # 可视化碰撞检测点
        for px, py in getattr(self, 'debug_points', []):
            pygame.draw.circle(screen, (0, 255, 0), (px, py), 4)

    def draw_tank(self, screen, tank):
        """
        绘制单个坦克及其朝向箭头。
        负责人: libobokabuto
        Args:
            screen (pygame.Surface): 绘图目标画布。
            tank (Tank): 坦克对象。
        Returns:
            None
        """
        pygame.draw.rect(screen, tank.color, tank.get_rect())
        center = tank.get_center()
        arrow_len = 20
        dir_vec = {
            'UP': (0, -arrow_len),
            'DOWN': (0, arrow_len),
            'LEFT': (-arrow_len, 0),
            'RIGHT': (arrow_len, 0)
        }[tank.direction]
        end_pos = (center[0] + dir_vec[0], center[1] + dir_vec[1])
        pygame.draw.line(screen, (0, 0, 0), center, end_pos, 3)

    def draw_bullets(self, screen, bullets):
        """
        绘制所有子弹对象。
        负责人: wobudao1a
        Args:
            screen (pygame.Surface): 绘图目标画布。
            bullets (list): 子弹对象列表。
        Returns:
            None
        """
        for bullet in bullets:
            bullet.draw(screen)

if __name__ == "__main__":
    pygame.init()
    ui = UI()
    game_map = map.Game_map()
    grid = game_map.generate_map()
    screen = pygame.display.set_mode((game_map.width * ui.cell_size, game_map.height * ui.cell_size))
    pygame.display.set_caption("Maze UI Test")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # 示例：把 debug_points 从 Tank 自动传递给 UI
        ui.debug_points = getattr(ui, 'debug_points', [])
        ui.draw_map(screen, grid)
        pygame.display.flip()
        clock.tick(30)
