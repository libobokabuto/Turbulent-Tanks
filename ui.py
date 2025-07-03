import pygame
import pymunk
import config
import math
from map import Game_map

class UI:
    """
    渲染模块：图形渲染与音效音乐。
    """
    def __init__(self,debug=False):
        """
        初始化 UI，读取文件设置绘制参数
        负责人: Thousand
        Args:
            debug (bool): 是否为调试模式，默认为 False。
        """
        if not debug:
            self.SCREEN_WIDTH          = config.SCREEN_WIDTH
            self.SCREEN_HEIGHT         = config.SCREEN_HEIGHT
            self.TILE_SIZE             = config.TILE_SIZE
            self.FPS                   = config.FPS
            self.BG_COLOR              = config.BG_COLOR
            self.WALL_COLOR            = config.WALL_COLOR
            self.WALL_WIDTH            = config.WALL_WIDTH
            self.TILE_COLOR_1          = config.TILE_COLOR_1
            self.TILE_COLOR_2          = config.TILE_COLOR_2
            self.Y_OFFSET              = config.Y_OFFSET
            self.outline_color         = config.OUTLINE_COLOR
            self.debug_collision_color = config.DEBUG_COLLISION_COLOR
        else:
            self.SCREEN_WIDTH          = 1230
            self.SCREEN_HEIGHT         = 915
            self.TILE_SIZE             = {4:150, 5:135}
            self.FPS                   = 60
            self.BG_COLOR              = (255, 255, 255)
            self.WALL_COLOR            = (102, 102, 102)
            self.WALL_WIDTH            = 8 
            self.TILE_COLOR_1          = (214, 214, 214)
            self.TILE_COLOR_2          = (230, 230, 230)
            self.Y_OFFSET              = 15
            self.outline_color         = (0,0,0)
            self.debug_collision_color = (255, 0, 0)

    def init_pygame(self):
        """
        初始化 Pygame，设置屏幕大小和标题。
        负责人: Thousand
        Returns:
            screen (pygame.Surface): Pygame 画布。
            clock (pygame.time.Clock): Pygame 时钟对象，用于控制帧率。
        """
        pygame.init()
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("坦克动荡")
        clock = pygame.time.Clock()
        return screen, clock

    def draw_map(self, screen, game_map: Game_map):
        """
        渲染地图，遍历 game_map.grid，根据 cell.walls 绘制交替色格子与墙体
        以screen的左上角为原点，x轴向右，y轴向下。
        负责人: Thousand
        Args:
            screen (pygame.Surface): Pygame 画布
            game_map (Game_map): 地图对象
        """
        tile_size = self.TILE_SIZE[game_map.height]# 根据地图高度获取对应的格子大小
        x_offset = (self.SCREEN_WIDTH - game_map.width * tile_size) // 2
        y_offset = self.Y_OFFSET# 获取XY偏移量

        # 先行后列遍历全部格子
        for row_idx, row in enumerate(game_map.grid):
            for col_idx, cell in enumerate(row):

                # 计算格子左上角的像素位置
                x_px = col_idx * tile_size + x_offset
                y_px = row_idx * tile_size + y_offset

                # 绘制交替色背景
                color = self.TILE_COLOR_1 if (row_idx + col_idx) % 2 == 0 else self.TILE_COLOR_2
                pygame.draw.rect(screen, color, (x_px, y_px, tile_size, tile_size))
                
                # 绘制墙体
                if cell.walls['N']:
                    pygame.draw.line(screen, self.WALL_COLOR,
                                     (x_px, y_px), (x_px + tile_size, y_px), self.WALL_WIDTH)
                if cell.walls['S']:
                    pygame.draw.line(screen, self.WALL_COLOR,
                                     (x_px, y_px + tile_size), (x_px + tile_size, y_px + tile_size), self.WALL_WIDTH)
                if cell.walls['W']:
                    pygame.draw.line(screen, self.WALL_COLOR,
                                     (x_px, y_px), (x_px, y_px + tile_size), self.WALL_WIDTH)
                if cell.walls['E']:
                    pygame.draw.line(screen, self.WALL_COLOR,
                                     (x_px + tile_size, y_px), (x_px + tile_size, y_px + tile_size), self.WALL_WIDTH)

    def draw_tank(self, screen, tank):
        """
        绘制坦克对象
        以screen的左上角为原点，x轴向右，y轴向下，角度顺时针增大
        负责人: libobokabuto
        Args:
            screen (pygame.Surface): Pygame 画布。
            tank (Tank): 坦克对象。
        """

        # 计算坦克中心点，坐标
        cx, cy = tank.get_center()

        # 计算坦克的各个部分尺寸
        length     = int(tank.length)     # 车身高度
        width      = int(tank.width)     # 车身宽度
        barrel_len = int(length / 1.5)      # 炮管长度
        barrel_w   = max(2, int(width / 4))  # 炮管宽度
        turret_r   = max(2, int(width / 2.5)) # 炮塔半径

        # 创建surface
        surf_w = width
        surf_h = barrel_len + length
        surf  = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)

        # 计算surface中心点
        cx_surf = surf_w // 2
        cy_surf = surf_h // 2

        # 对齐车身矩形的中心点对齐到 surf 的中心
        body_rect = pygame.Rect(
            0,
            cy_surf - length // 2,
            width,
            length
        )
        pygame.draw.rect(surf, tank.color, body_rect)
        pygame.draw.rect(surf, self.outline_color, body_rect, 2)

        # 将炮管从车身中心往上延伸 barrel_len
        barrel_rect = pygame.Rect(
            cx_surf - barrel_w // 2,
            cy_surf - barrel_len,
            barrel_w,
            barrel_len
        )
        pygame.draw.rect(surf, tank.weapon_color, barrel_rect)
        pygame.draw.rect(surf, self.outline_color, barrel_rect, 2)

        # 以车身中心为圆心绘制炮塔
        pygame.draw.circle(surf, tank.weapon_color, (cx_surf, cy_surf), turret_r)
        pygame.draw.circle(surf, self.outline_color,(cx_surf, cy_surf), turret_r, 2)

        # 旋转并贴到屏幕上
        angle = math.degrees(tank.body.angle) % 360
        rotated = pygame.transform.rotate(surf, -angle)
        rot_rect = rotated.get_rect(center=(cx, cy))
        screen.blit(rotated, rot_rect)

    def draw_bullets(self,screen:pygame.Surface, bullets: list):
        """
        批量渲染子弹列表。
        负责人: Thousand
        """
        for b in bullets:
            if not b.alive:
                continue
            x, y= b.get_position()
            r = b.radius
            color = b.color
            pygame.draw.circle(screen, color, (x, y), r)

    def draw_tank_collision_shapes(self, screen, tank):
        """
        绘制坦克的碰撞箱，主要用于调试。
        负责人: thousand
        Args:
            screen (pygame.Surface): Pygame 画布。
            tank (Tank): 坦克对象。
        """
        for shape in [tank.shape, tank.barrel_shape]:
            if isinstance(shape, pymunk.Poly):
                vs = [tank.body.local_to_world(v) for v in shape.get_vertices()]
                pts = [(int(v[0]), int(v[1])) for v in vs]
                pygame.draw.polygon(screen, self.debug_collision_color, pts, 2)
