import pymunk

def init_space():
    """
    初始化物理空间，设置重力和碰撞类型。
    负责人: thousand
    Returns:
        pymunk.Space: 初始化的物理空间对象。
    """
    space = pymunk.Space()
    space.gravity = (0, 0)  # 设置重力为零
    return space