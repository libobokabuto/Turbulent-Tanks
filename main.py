import pygame
import sys
from pygame.locals import *

from ui import UI
from physics import init_space, register_collision_handlers
from map import Game_map
from tank import Tank
from hic import HCIManager
from bullet import Bullet


def init_game(debug: bool = True):
    """
    Create and wire‑up all core objects, returning them as a tuple.
    负责人: Thousand

    Returns:
        ui, screen, clock, space, game_map, hci, tanks, bullets
    """
    ui = UI(debug=debug)
    screen, clock = ui.init_pygame()

    space = init_space()
    

    game_map = Game_map(debug=debug)
    game_map.generate_map()
    game_map.create_static_walls(space, ui)

    # --- entities ---------------------------------------------------------
    spawn_pts = game_map.get_spawn_points(2, ui)
    tanks = [
        Tank(id=1, x=spawn_pts[0][0], y=spawn_pts[0][1], color=(0, 128, 0),
             game_map=game_map, space=space, debug=debug),
        Tank(id=2, x=spawn_pts[1][0], y=spawn_pts[1][1], color=(200, 30, 30),
             game_map=game_map, space=space, debug=debug),
    ]

    hci = HCIManager()
    bullets: list[Bullet] = []

    return ui, screen, clock, space, game_map, hci, tanks, bullets


def handle_tank_actions(tanks, actions, bullets, space):
    """
    应用玩家输入到每辆坦克，管理开火与冷却
    负责人: libobokabuto
    Args:
        tanks (list[Tank]): 坦克列表
        actions (list[dict]): 两个坦克对应的动作字典
        bullets (list[Bullet]): 子弹列表
        space (pymunk.Space): 物理空间
    Returns:
        None
    """
    for tank, act in zip(tanks, actions):
        if tank.dead:
            continue

        # rotation / thrust -------------------------------------------------
        tank.apply_actions(act)
        tank.limit_speed()

        # fire control ------------------------------------------------------
        own_bullets = sum(
            1 for b in bullets if b.owner_id == tank.id and b.alive
        )
        if act["SHOOT"] and own_bullets < tank.max_exist_ammo and tank.can_fire():
            tip_x, tip_y, ang = tank.get_barrel_tip()
            bullets.append(
                Bullet(space, tip_x, tip_y, ang, tank.id, tank.scale, debug=True)
            )
            tank.mark_fired()


def update_bullets(bullets):
    """
    推进子弹生命周期并清理过期或死亡子弹
    负责人: Thousand
    Args:
        bullets (list[Bullet]): 子弹列表
    Returns:
        None
    """
    for b in bullets[:]:
        b.update()
        if (not b.alive) or b.is_expired():
            b.destroy()
            bullets.remove(b)


def render(screen, ui, game_map, tanks, bullets):
    screen.fill(ui.BG_COLOR)
    ui.draw_map(screen, game_map)
    ui.draw_bullets(screen, bullets)
    for t in tanks:
        if not t.dead:
            ui.draw_tank(screen, t)
        #ui.draw_tank_collision_shapes(screen, t)
    pygame.display.flip()


def main():
    # 初始化游戏及 UI 状态
    ui, screen, clock, space, game_map, hci, tanks, bullets = init_game(debug=True)
    scores = {t.id: 0 for t in tanks}
    # 2) 初始化记分板并注册碰撞回调
    register_collision_handlers(space, scores)
    # 3) 设置界面数据
    settings = {"音量": 5, "难度": "普通"}
    selected_setting = 0
    state = 'menu'

    # 仅存一人时倒计时开始时间（毫秒）
    countdown_start = None
    

    running = True
    while running:
        # 事件收集
        for event in pygame.event.get():
            # —— 事件收集 & 状态切换 ——
            if event.type == QUIT:
                running = False
                break
            # 游戏中按 ESC/Tab 返回主菜单
            elif state == 'game' and event.type == KEYDOWN and event.key in (K_ESCAPE, K_TAB):
                state = 'menu'
                break

            # 菜单状态下的上下左右和回车
            elif state == 'menu' and event.type == KEYDOWN:
                if event.key == K_UP:
                    ui.selected_option = (ui.selected_option - 1) % len(ui.menu_options)
                elif event.key == K_DOWN:
                    ui.selected_option = (ui.selected_option + 1) % len(ui.menu_options)
                elif event.key == K_RETURN:
                    choice = ui.menu_options[ui.selected_option]
                    idx = ui.selected_option
                    if idx == 0:       # 开始游戏
                        state = 'game'
                    elif idx == 1:     # 设置
                        state = 'settings'
                    elif idx == 2:     # 退出
                        running = False
                        break
             # 设置界面下的交互       
            elif state == 'settings' and event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    state = 'menu'
                elif event.key == K_UP:
                    selected_setting = (selected_setting - 1) % len(settings)
                elif event.key == K_DOWN:
                    selected_setting = (selected_setting + 1) % len(settings)
                elif event.key == K_LEFT and isinstance(list(settings.values())[selected_setting], int):
                    key = list(settings.keys())[selected_setting]
                    settings[key] = max(0, settings[key] - 1)
                elif event.key == K_RIGHT and isinstance(list(settings.values())[selected_setting], int):
                    key = list(settings.keys())[selected_setting]
                    settings[key] += 1
                elif event.key == K_RETURN:
                    # 暂无额外操作，按 ENTER 返回菜单
                    state = 'menu'

        if not running:
            break     
        
        # 游戏逻辑
        if state == 'game':
            # 1) 先处理所有输入，包含退出、菜单切换、重启
            running, restart, act0, act1 = hci.handle_events()
            if not running:
                break
            # Esc 或 Tab ⇒ 返回主菜单
            if act0["SWITCH_MENU"] or act1["SWITCH_MENU"]:
                state = 'menu'
                continue

            # 按 R ⇒ 重新开始本局
            if restart:
                # 判断胜利者并记录分数
                alive = [t for t in tanks if not t.dead]
                if len(alive) == 1:
                    scores[alive[0].id] += 1
                ui, screen, clock, space, game_map, hci, tanks, bullets = init_game(debug=True)
                register_collision_handlers(space, scores)
                state = 'game'
                continue

            handle_tank_actions(tanks, [act0, act1], bullets, space)
            space.step(1 / ui.FPS)
            update_bullets(bullets)

            # —— 自动重启逻辑 —— 
            # 当场上只剩 1 辆坦克时开始计时，10s 后自动重启
            alive = [t for t in tanks if not t.dead]
            if len(alive) == 1:
                if countdown_start is None:
                    countdown_start = pygame.time.get_ticks()
                else:
                    elapsed = (pygame.time.get_ticks() - countdown_start) / 1000
                    if elapsed >= 10:
                        # 记录胜利者得分
                        scores[alive[0].id] += 1
                        # 重新初始化游戏并重注册碰撞回调
                        ui, screen, clock, space, game_map, hci, tanks, bullets = init_game(debug=True)
                        register_collision_handlers(space, scores)
                        state = 'game'
                        countdown_start = None
                        continue
            else:
                # 如果存活坦克超过 1 辆，重置倒计时
                countdown_start = None
            
        # 渲染
        screen.fill(ui.BG_COLOR)
        if state == 'menu':
            ui.draw_main_menu(screen)

        elif state == 'game':
            ui.draw_map(screen, game_map)
            ui.draw_bullets(screen, bullets)
            for t in tanks:
                if not t.dead:
                    ui.draw_tank(screen, t)
            # 记分板移到底部，记得传入 game_map
            ui.draw_scoreboard(screen, scores, game_map)
        elif state == 'settings':
            ui.draw_settings(screen, settings, selected_setting)

        pygame.display.flip()
        clock.tick(ui.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
