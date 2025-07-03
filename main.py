import pygame
from ui import UI
from physics import init_space
from map import Game_map
from tank import Tank
from hic import HCIManager


def main():
    # 初始化 UI 和屏幕
    ui = UI(debug=True)
    screen, clock = ui.init_pygame()

    # 初始化物理空间
    space = init_space()

    # 生成地图并创建静态墙体
    game_map = Game_map(debug=True)
    game_map.generate_map()
    # 根据 map.py 中定义的方法调用
    game_map.create_static_walls(space, ui)

    # 创建坦克
    tank = Tank(id=1, x=100, y=100, color=(0, 128, 0), game_map=game_map, space=space, debug=True)

    # 人机交互管理
    hci = HCIManager()

    # 主循环
    running = True
    while running:
        # 处理输入并获取动作
        running, actions = hci.handle_events()
        # 应用坦克动作（旋转与推进）
        tank.apply_actions(actions)
        # 物理步进
        space.step(1 / ui.FPS)
        # 限速与阻尼
        tank.limit_speed()
        # 渲染一帧
        ui.render(screen, game_map, tank)
        # 控制帧率
        clock.tick(ui.FPS)

    # 退出
    pygame.quit()


if __name__ == '__main__':
    main()
