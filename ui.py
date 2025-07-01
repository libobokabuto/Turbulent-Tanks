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
    for i, tank in enumerate(tanks):  # 遍历每个坦克对象
        # 绘制得分文本
        score_text = self.font.render(f"Score: {tank['score']}", True, (0, 0, 0))
        # 将得分文本绘制到屏幕上，位置为(20, 20 + i * 40)，函数score为得分函数
        screen.blit(score_text, (20, 20 + i * 40))

        # 绘制健康状态文本
        health_text = self.font.render(f"Health: {tank['health']}", True, (0, 0, 0))
        # 将健康状态文本绘制到屏幕上，位置为(200, 20 + i * 40)函数health为状态函数
        screen.blit(health_text, (200, 20 + i * 40))

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

# 显示主菜单界面
def show_main_menu(self, screen):
    # 填充屏幕背景色为白色
    screen.fill((255, 255, 255))
    # 渲染主菜单标题文本，字体为黑色
    title = self.font.render("Main Menu", True, (0, 0, 0))
    # 将主菜单标题绘制到屏幕上
    screen.blit(title, (350, 200))

    # 遍历主菜单选项并绘制到屏幕上
    for i, item in enumerate(self.main_menu_items):
        # 根据当前选中项设置文本颜色，选中为灰色，未选中为黑色
        color = (128, 128, 128) if i == self.selected_item else (0, 0, 0)
        # 渲染菜单选项文本
        text = self.font.render(item, True, color)
        # 将菜单选项文本绘制到屏幕上
        screen.blit(text, (350, 300 + i * 50))

# 显示游戏结束界面
def show_game_over(self, screen):
    # 填充屏幕背景色为白色
    screen.fill((255, 255, 255))
    # 渲染游戏结束标题文本，字体为黑色
    title = self.font.render("Game Over", True, (0, 0, 0))
    # 将游戏结束标题绘制到屏幕上
    screen.blit(title, (350, 200))

    # 遍历游戏结束菜单选项并绘制到屏幕上
    for i, item in enumerate(self.game_over_items):
        # 根据当前选中项设置文本颜色，选中为灰色，未选中为黑色
        color = (128, 128, 128) if i == self.selected_item else (0, 0, 0)
        # 渲染菜单选项文本
        text = self.font.render(item, True, color)
        # 将菜单选项文本绘制到屏幕上
        screen.blit(text, (350, 300 + i * 50))

# 显示暂停菜单
def show_pause_menu(self, screen):
    # 填充屏幕背景色为白色
    screen.fill((255, 255, 255))
    # 渲染暂停菜单标题文本，字体为黑色
    title = self.font.render("Paused", True, (0, 0, 0))
    # 将暂停菜单标题绘制到屏幕上
    screen.blit(title, (350, 200))

    # 遍历暂停菜单选项并绘制到屏幕上
    for i, item in enumerate(self.pause_menu_items):
        # 根据当前选中项设置文本颜色，选中为灰色，未选中为黑色
        color = (128, 128, 128) if i == self.selected_item else (0, 0, 0)
        # 渲染菜单选项文本
        text = self.font.render(item, True, color)
        # 将菜单选项文本绘制到屏幕上
        screen.blit(text, (350, 300 + i * 50))
    def draw_bullets(self, screen, bullets):
        '''
        绘制所有子弹对象
        负责人: wobudao1a
        Args:
            screen (pygame.Surface): 绘制目标表面
            bullets (list): 子弹对象列表
        '''
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
        # 仅渲染迷宫地图
        ui.draw_map(screen, grid)
        clock.tick(30)
    pygame.quit()