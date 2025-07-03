import pygame
import config
import pymunk
import math
from map import Game_map

class Tank:
    """
    坦克模块：管理坦克状态、运动、方向及射击逻辑。
    """ 
    def __init__(
            self,id: int, 
            x: float, 
            y: float,
            color: tuple, 
            game_map: Game_map, 
            space: pymunk.Space, 
            is_ai: bool = False, 
            debug=False):
        """
        初始化坦克属性
        负责人: libobokabuto
        Args:
            id (int): 坦克 ID
            x (float): X 坐标
            y (float): Y 坐标
            color (tuple): RGB 颜色值
            game_map (Game_map): 游戏地图对象，用于获取缩放比例
            space (pymunk.Space): Pymunk 空间对象，用于物理模拟
            is_ai (bool): 是否为 AI 控制的坦克，默认为 False
            debug (bool): 是否为调试模式，默认为 False
        """
        # 初始化坦克属性
        self.game_map = game_map
        self.scale = 135 /150 if game_map.height == 5 else 150 / 150# 缩放
        self.id = id
        self.color = color
        self.is_ai = is_ai

        if not debug:
            self.length = config.TANK_LENGTH * self.scale
            self.width = config.TANK_WIDTH * self.scale
            self.max_speed = config.TANK_MAX_SPEED * self.scale
            self.direction = config.TANK_DIRECTION
            self.cooldown = config.TANK_COOLDOWN
            self.max_exist_ammo = config.TANK_MAX_EXIST_AMMO
            self.rotate_step = config.TANK_ROTATE_STEP
            self.weapon_color = config.TANK_WEAPON_COLOR
            self.mass = config.TANK_MASS
            self.angular_damping = config.TANK_ANGULAR_DAMPING
            self.elasticity = config.TANK_ELASTICITY
            self.friction = config.TANK_FRICTION
            self.collision_type = config.TANK_COLLISION_TYPE
        else:
            self.length = 65 * self.scale
            self.width = 45 * self.scale
            self.max_speed = 144 * self.scale
            self.direction = 0
            self.cooldown = 0
            self.max_exist_ammo = 5
            self.rotate_step = 2
            self.weapon_color = (100, 100, 100)
            self.mass = 1
            #self.angular_damping = 0.05
            self.elasticity = 0.3
            self.friction = 0.5
            self.collision_type = 1

        # 创建物理 Body
        moment = pymunk.moment_for_box(self.mass, (self.width, self.length))
        self.body = pymunk.Body(self.mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        #self.body.angular_damping = self.angular_damping

        # 创建车身 Shape
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.length))
        self.shape.elasticity = config.TANK_ELASTICITY
        self.shape.friction = config.TANK_FRICTION
        self.shape.collision_type = config.TANK_COLLISION_TYPE
        space.add(self.body, self.shape)

        # 创建炮塔 Shape
        barrel_len = self.length / 1.5
        barrel_w   = max(2, self.width / 4)
        cx, cy = 0, -barrel_len/2
        w2, l2 = barrel_w/2, barrel_len/2
        barrel_vertices = [
            (cx - w2, cy - l2),  # 左上
            (cx + w2, cy - l2),  # 右上
            (cx + w2, cy + l2),  # 右下
            (cx - w2, cy + l2),  # 左下
        ]
        barrel_shape = pymunk.Poly(self.body, barrel_vertices)
        barrel_shape.elasticity = config.TANK_ELASTICITY
        barrel_shape.friction   = config.TANK_FRICTION
        barrel_shape.collision_type = config.TANK_COLLISION_TYPE
        # 使用坦克自身 ID 分组，防止自身碰撞
        barrel_shape.filter = pymunk.ShapeFilter(group=self.body.id)
        space.add(barrel_shape)
        self.barrel_shape = barrel_shape

    def apply_actions(self,actions):
        # 旋转
        if actions["LEFT"]:
            self.body.angle -= math.radians(self.rotate_step)
        if actions["RIGHT"]:
            self.body.angle += math.radians(self.rotate_step)
        # 推进/制动
        if actions["UP"] or actions["DOWN"]:
            ang = self.body.angle
            force = 500 * (1 if actions["UP"] else -1)
            fx = force * math.sin(ang)
            fy = -force * math.cos(ang)
            self.body.apply_force_at_world_point((fx, fy), self.body.position)
        else:
            self.body.velocity = (0, 0)
    
    def limit_speed(self):
        v = self.body.velocity
        if v.length > config.TANK_MAX_SPEED:
            self.body.velocity = v.normalized() * config.TANK_MAX_SPEED
        self.body.angular_velocity *= 0.8

    def get_rect(self) -> pygame.Rect:
        """
        获取坦克的矩形边界，用于碰撞检测和渲染
        以左上角为原点，宽度和长度为坦克的实际尺寸
        负责人: libobokabuto
        Returns:
            pygame.Rect: 坦克的矩形边界
        """
        cx, cy = self.body.position
        half_w, half_l = self.width/2, self.length/2
        return pygame.Rect(int(cx-half_w),
                           int(cy-half_l),
                           int(self.width),
                           int(self.length))

    def get_center(self) -> tuple:
        """
        获取坦克的中心坐标
        以左上角为原点
        负责人: libobokabuto    
        Returns:
            tuple: 坦克的中心坐标 (x, y)
        """
        x, y = self.body.position
        return int(x), int(y)
    
