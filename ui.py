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


    def handle_input(self, player_tank, game_map):
        """
        处理玩家按键输入，控制坦克的移动与旋转。
        负责人: libobokabuto
        Args:
            player_tank (Tank): 玩家控制的坦克对象。
            game_map (Game_map): 地图对象。
        Returns:
            None
        """
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_tank.rotate('UP')
        player_tank.move(0, -player_tank.speed, game_map)
        moved = True
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_tank.rotate('DOWN')
        player_tank.move(0, player_tank.speed, game_map)
        moved = True
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_tank.rotate('LEFT')
        player_tank.move(-player_tank.speed, 0, game_map)
        moved = True
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_tank.rotate('RIGHT')
        player_tank.move(player_tank.speed, 0, game_map)
        moved = True

    if keys[pygame.K_SPACE]:
        player_tank.shoot(None)  # 记得替换为真实 bullet_manager


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

    def draw_tank(self, screen, tank):
        '''
        此函数在屏幕上绘制一个坦克对象和其朝向。
        负责人: libobokabuto
            Args:
                screen (pygame.Surface): 绘图目标。
                tank (Tank): 要绘制的坦克对象。
            Returns:
                 None
        '''
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
