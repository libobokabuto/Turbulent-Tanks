import pygame

from ui import UI
from physics import init_space, register_collision_handlers
from map import Game_map
from tank import Tank
from hic import HCIManager
from bullet import Bullet


def init_game(debug: bool = True):
    """Create and wire‑up all core objects, returning them as a tuple."""
    ui = UI(debug=debug)
    screen, clock = ui.init_pygame()

    space = init_space()
    register_collision_handlers(space)

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
    """Apply input to each tank, manage firing & cooldowns."""
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
    """Advance bullet lifetime & clean up dead ones."""
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
    ui, screen, clock, space, game_map, hci, tanks, bullets = init_game(debug=True)

    running = True
    while running:
        running, restart, act0, act1 = hci.handle_events()
        if restart:
            # Tear‑down current world (let GC reclaim) and build fresh one
            ui, screen, clock, space, game_map, hci, tanks, bullets = init_game(debug=True)
            continue  # skip the rest of this frame

        handle_tank_actions(tanks, [act0, act1], bullets, space)

        space.step(1 / ui.FPS)
        update_bullets(bullets)
        render(screen, ui, game_map, tanks, bullets)

        clock.tick(ui.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
