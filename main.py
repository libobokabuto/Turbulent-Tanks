# main.py
import pygame
from map import Game_map
from tank import Tank
from ui import UI
from bullet_manager import BulletManager
from hic import HCIManager

def main():
    """
    游戏主循环，整合地图、坦克、UI与子弹等模块。
    负责人: libobokabuto
    Returns:
        None
    """
    pygame.init()

    # --- 地图与 UI 初始化 ---
    game_map = Game_map()
    grid = game_map.generate_map()
    ui = UI()
    screen = pygame.display.set_mode((game_map.width * ui.cell_size, game_map.height * ui.cell_size))
    pygame.display.set_caption("Tank Trouble Clone")

    # --- 坦克与子弹管理器初始化 ---
    player_tank = Tank(id=1, x=50, y=50, color=(0, 100, 255), is_ai=False)
    bullet_manager = BulletManager()
    hci = HCIManager()  # 初始化HCIManager

    clock = pygame.time.Clock()
    running = True

    while running:
        # --- 事件处理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- 玩家操作输入 ---
        actions = ui.handle_input(player_tank, game_map)

        # --- 更新逻辑 ---
        player_tank.update(game_map, bullet_manager)
        bullet_manager.update_all(game_map)

        # --- 绘图 ---
        ui.draw_map(screen, grid)
        ui.draw_tank(screen, player_tank)
        ui.draw_bullets(screen, bullet_manager.get_all())

        # --- 播放音效 ---
        if actions["UP"]:
            player_tank.rotate('UP')
            player_tank.move(0, -player_tank.speed, game_map)
            hci.play_tank_move_sound(player_tank.id)  # 插入：播放坦克前进音效
        if actions["DOWN"]:
            player_tank.rotate('DOWN')
            player_tank.move(0, player_tank.speed, game_map)
            hci.play_tank_move_sound(player_tank.id)
        if actions["LEFT"]:
            player_tank.rotate('LEFT')
            player_tank.move(-player_tank.speed, 0, game_map)
            hci.play_tank_turn_sound(player_tank.id, "LEFT")  # 插入：播放坦克转向音效
        if actions["RIGHT"]:
            player_tank.rotate('RIGHT')
            player_tank.move(player_tank.speed, 0, game_map)
            hci.play_tank_turn_sound(player_tank.id, "RIGHT")
        if actions["SHOOT"]:
            player_tank.shoot(bullet_manager)
            hci.play_tank_fire_sound(player_tank.id)  # 插入：播放坦克开炮音效
        if actions["SWITCH_MENU"]:
            # 这里可以调用UI或其他模块切换界面
            hci.play_switch_menu_sound()  # 插入：播放界面切换音效
            pass

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
