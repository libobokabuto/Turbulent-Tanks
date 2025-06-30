# 人机交互模块，仅提供类和方法，由主程序(main.py)调用，无需main函数

import pygame

class HCIManager:
    """
    人机交互管理器：只负责监听玩家输入，并将输入动作以事件字典形式返回。
    具体的游戏逻辑、界面切换、模块联动由主循环或其他模块完成。
    """

    def handle_events(self):
        """
        监听并处理游戏内操作与事件，返回退出标志和本帧玩家操作。
        Returns:
            running (bool): 是否继续运行
            actions (dict): 当前帧玩家操作，如 {"UP":True, "LEFT":False, "SHOOT":True, "SWITCH_MENU":False}
        """
        running = True
        actions = {
            "UP": False, "DOWN": False, "LEFT": False, "RIGHT": False,
            "SHOOT": False, "SWITCH_MENU": False
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                    actions["SWITCH_MENU"] = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            actions["UP"] = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            actions["DOWN"] = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            actions["LEFT"] = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            actions["RIGHT"] = True
        if keys[pygame.K_SPACE]:
            actions["SHOOT"] = True

        return running, actions

    # 预留：按键反馈动画接口
    def play_key_animation(self, key):
        """预留：播放按键反馈动画（如高亮、闪烁等）。"""
        pass

    # 预留：播放按键音效接口
    def play_key_sound(self, key):
        """预留：播放按键音效（如点击、移动、射击等）。"""
        pass

    # 预留：播放界面切换音效
    def play_switch_menu_sound(self):
        """预留：播放界面切换时的音效。"""
        pass

    # 预留：坦克前进音效
    def play_tank_move_sound(self, tank_id):
        """预留：播放指定坦克前进时的音效。"""
        pass

    # 预留：坦克转向音效
    def play_tank_turn_sound(self, tank_id, direction):
        """预留：播放指定坦克转向时的音效。"""
        pass

    # 预留：坦克开炮音效
    def play_tank_fire_sound(self, tank_id):
        """预留：播放指定坦克开炮时的音效。"""
        pass

    # 预留：坦克受击音效
    def play_tank_hit_sound(self, tank_id):
        """预留：播放指定坦克受击时的音效。"""
        pass

    # 预留：子弹发射音效（可区分不同类型子弹）
    def play_bullet_fire_sound(self, bullet_type="normal"):
        """预留：播放不同类型子弹发射时的音效。"""
        pass

    # 预留：子弹命中音效
    def play_bullet_hit_sound(self, bullet_type="normal"):
        """预留：播放不同类型子弹命中时的音效。
        """
        pass