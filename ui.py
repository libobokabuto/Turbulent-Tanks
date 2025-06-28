#用户交互模块
import pygame
import map
class UI:
    def __init__(self, cell_size=100, wall_color=(200, 200, 200), wall_width=2, bg_color=(255, 255, 255)):
        """
        初始化 UI，设置绘制参数，方便后续调用。
        Args:
            cell_size (int): 每个格子的像素大小。
            wall_color (tuple): 墙壁颜色。
            wall_width (int): 墙壁宽度。
            bg_color (tuple): 背景色。
        """
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.wall_width = wall_width
        self.bg_color = bg_color


    def handle_input(self, player_tank):
        """
        处理玩家按键输入，控制坦克移动与射击。
        """

    def draw_HUD(self, screen, tanks: list):
        """
        绘制得分、状态条等HUD元素。
        """ 

    def draw_map(self, screen, grid):
        """
        此函数绘制迷宫地图。
        负责人:Thousand
        Args:
            screen (pygame.Surface): 要绘制到的屏幕。
            grid (list[list[Cell]]): 迷宫格子数据。
        """
        screen.fill(self.bg_color)
        # 绘制墙体
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                x_px = x * self.cell_size
                y_px = y * self.cell_size
                if cell.walls['N']:
                    pygame.draw.line(screen, self.wall_color,
                                     (x_px, y_px),
                                     (x_px + self.cell_size, y_px),
                                     self.wall_width)
                if cell.walls['S']:
                    pygame.draw.line(screen, self.wall_color,
                                     (x_px, y_px + self.cell_size),
                                     (x_px + self.cell_size, y_px + self.cell_size),
                                     self.wall_width)
                if cell.walls['W']:
                    pygame.draw.line(screen, self.wall_color,
                                     (x_px, y_px),
                                     (x_px, y_px + self.cell_size),
                                     self.wall_width)
                if cell.walls['E']:
                    pygame.draw.line(screen, self.wall_color,
                                     (x_px + self.cell_size, y_px),
                                     (x_px + self.cell_size, y_px + self.cell_size),
                                     self.wall_width)
        pygame.display.flip()


    def show_main_menu(self, screen):
        """
        显示主菜单界面。
        """

    def show_game_over(self, screen):
        """
        显示游戏结束界面。
        """

    def show_pause_menu(self, screen):
        """
        显示暂停菜单。
        """
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
        # 仅渲染迷宫地图
        ui.draw_map(screen, grid)
        clock.tick(30)
    pygame.quit()
