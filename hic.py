# 人机交互模块，仅提供类和方法，由主程序(main.py)调用，无需main函数

import pygame

class HCIManager:
    """
    人机交互模块，只负责监听玩家输入，并将输入动作以事件字典形式返回。
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