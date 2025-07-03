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

def register_collision_handlers(space: pymunk.Space, scores: dict):
    """
    子弹打到坦克的碰撞回调（Pymunk ≥7.0），非自杀击杀 +1 分
    负责人: Thousand，libobokabuto
    Args:
        space (pymunk.Space): 物理空间
        scores (dict): 玩家ID->得分映射，会在回调中被修改
    """
    def _on_bullet_hit_tank(arbiter, space_, _data):
        """
        子弹击中坦克时的回调函数。
        负责人: Thousand，libobokabuto
        Args:
            arbiter (pymunk.Arbiter): 碰撞信息
            space_ (pymunk.Space): 物理空间
            data: 用户数据（未使用）
        Returns:
            bool: 返回 False，阻止 Pymunk 对此碰撞做弹性处理
        """
        
        s1, s2 = arbiter.shapes
        if s1.collision_type == config.BULLET_COLLISION_TYPE:
            bullet_shape, tank_shape = s1, s2
        else:
            bullet_shape, tank_shape = s2, s1

        bullet = bullet_shape.bullet      # 来自 bullet.py :contentReference[oaicite:10]{index=10}
        tank   = tank_shape.tank          # 来自 tank.py   :contentReference[oaicite:11]{index=11}

        # 1) 击杀判断 & 加分（非自杀）
        if not tank.dead:
            if bullet.owner_id != tank.id:
                scores[bullet.owner_id] += 1

        # 2) 标记坦克死亡并移除其物理体
            tank.dead = True
            space_.remove(tank.body, tank.shape, tank.barrel_shape)

        # 3) 销毁子弹
        bullet.destroy()

        # 4) 禁止本次碰撞后续处理
        return False

        

    # 注册——顺序无所谓，只写一次即可
    space.on_collision(
        config.BULLET_COLLISION_TYPE,   # = 2   :contentReference[oaicite:12]{index=12}
        config.TANK_COLLISION_TYPE,     # = 1   :contentReference[oaicite:13]{index=13}
        begin=_on_bullet_hit_tank,
    )
