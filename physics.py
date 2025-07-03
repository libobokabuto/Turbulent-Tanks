import pymunk
import config

def init_space():
    """
    初始化物理空间，设置重力和碰撞类型。
    负责人: thousand
    Returns:
        pymunk.Space: 初始化的物理空间对象。
    """
    space = pymunk.Space()
    space.gravity = config.SPACE_GRAVITY  # 设置重力为零
    space.damping = config.SPACE_DAMPING    # 关闭全局阻尼
    return space

def register_collision_handlers(space: pymunk.Space):
    """
    子弹打到坦克的回调（Pymunk ≥7.0）
    """
    def _on_bullet_hit_tank(arbiter, space_, _data):
        # 判定哪边是子弹哪边是坦克
        s1, s2 = arbiter.shapes
        if s1.collision_type == config.BULLET_COLLISION_TYPE:
            bullet_shape, tank_shape = s1, s2
        else:
            bullet_shape, tank_shape = s2, s1

        bullet = bullet_shape.bullet      # 来自 bullet.py :contentReference[oaicite:10]{index=10}
        tank   = tank_shape.tank          # 来自 tank.py   :contentReference[oaicite:11]{index=11}

        # 1) 子弹销毁
        bullet.destroy()

        # 2) 坦克判死 & 把刚体/形状移出空间
        if not tank.dead:
            tank.dead = True
            space_.remove(tank.body, tank.shape, tank.barrel_shape)

        # 3) 阻止 Chipmunk 再做反弹等处理
        arbiter.process_collision = False

    # 注册——顺序无所谓，只写一次即可
    space.on_collision(
        config.BULLET_COLLISION_TYPE,   # = 2   :contentReference[oaicite:12]{index=12}
        config.TANK_COLLISION_TYPE,     # = 1   :contentReference[oaicite:13]{index=13}
        begin=_on_bullet_hit_tank,
    )
