import pymunk
import config
import math
import time

class Bullet:
    """
    子弹类：管理物理、生命周期与渲染。
    负责人: Thousand
    """
    def __init__(
        self,
        space: pymunk.Space,
        x: float,
        y: float,
        angle: float,
        owner_id: int,
        scale:float,
        debug: bool = False
    ):
        """
        初始化子弹属性并将其加入物理空间。

        Args:
            space (pymunk.Space): 物理空间，用于添加 Body/Shape。
            x (float): 发射起点 X 坐标。
            y (float): 发射起点 Y 坐标。
            angle (float): 发射角度，弧度制。
            owner_id (int): 发射者 ID，用于碰撞过滤。
            debug (bool): 调试模式开关，True 时使用更易观察的慢速大弹丸。
        """
        if not debug:
            self.radius         = config.BULLET_RADIUS * scale
            self.mass           = config.BULLET_MASS
            self.speed          = config.BULLET_SPEED * scale
            self.lifetime       = config.BULLET_LIFETIME
            self.color          = config.BULLET_COLOR
            self.elasticity     = config.BULLET_ELASTICITY
            self.friction       = config.BULLET_FRICTION
            self.collision_type = config.BULLET_COLLISION_TYPE
            self.arm_time       = config.BULLET_ARM_TIME
        else:
            # 调试模式下：半径翻倍，速度减半，寿命延长 3 倍，颜色改为红色
            self.radius         = 5 * scale
            self.mass           = 0.1 
            self.speed          = 240 * scale
            self.lifetime       = 10
            self.color          = (255, 0, 0)
            self.elasticity     = 1.0
            self.friction       = 0.0
            self.collision_type = 2
            self.arm_time       = 0.15

        # ———— 刚体与形状 ————
        self.space = space
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity     = self.elasticity
        self.shape.friction       = self.friction
        self.shape.collision_type = self.collision_type
        # 分组过滤，避免与发射者碰撞
        self.owner_id = owner_id
        self.shape.filter= pymunk.ShapeFilter(group=owner_id)

        self.armed      = False

        self.space.add(self.body, self.shape)

        # ———— 初速度 ————
        vx, vy = self.speed * math.sin(angle), -self.speed * math.cos(angle)
        self.body.velocity = vx, vy

        # ———— 生命周期 & 渲染 ————
        self.alive = True
        self.spawn_time = time.time()

        self.body.bullet = self
        self.shape.bullet = self

    def is_expired(self) -> bool:
        """根据生命周期判断是否过期。"""
        return time.time() - self.spawn_time > self.lifetime
    
    def update(self):
        """
        过了保险时间后，把 group 设回 0，子弹即可撞到任何坦克（含自己）。
        """
        if (not self.armed) and (time.time() - self.spawn_time >= self.arm_time):
            # 清掉 group → 让后续碰撞正常生效
            self.shape.filter = pymunk.ShapeFilter(group=0)
            self.armed = True

    def destroy(self):
        """
        把子弹从物理空间移除。  
        若已移除过，再调用也不会抛错。
        """
        if not self.alive:           # 已经销毁过，直接返回
            return

        self.alive = False           # 标记死亡

        # 子弹可能已在碰撞回调里被移除；body.space=None 时就什么都不用做
        if self.body.space is not None:
            self.space.remove(self.body, self.shape)

    def get_position(self):
        x, y = self.body.position
        return int(x), int(y)
