# hic.py
import pygame


class HCIManager:
    """
    人机交互模块：监听玩家输入，并分别返回 0 号和 1 号坦克的动作。
    """
    @staticmethod
    def _blank_actions():
        return {
            "UP": False, "DOWN": False, "LEFT": False, "RIGHT": False,
            "SHOOT": False, "SWITCH_MENU": False
        }

    def handle_events(self):
        """
        Returns
        -------
        running : bool
            False ⇒ 退出游戏
        actions_p0 : dict
            0 号坦克（WASD / SPACE）
        actions_p1 : dict
            1 号坦克（方向键 / 鼠标左键）
        """
        running = True
        restart  = False          # ←★ 先初始化
        actions_p0 = self._blank_actions()
        actions_p1 = self._blank_actions()

        # 事件（QUIT、Esc/Tab、鼠标按下）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                actions_p0["SWITCH_MENU"] = actions_p1["SWITCH_MENU"] = True
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                    actions_p0["SWITCH_MENU"] = actions_p1["SWITCH_MENU"] = True
                elif event.key == pygame.K_r:
                    restart = True

        # 连续按键、鼠标状态
        keys = pygame.key.get_pressed()
        mb   = pygame.mouse.get_pressed(3)

        # ------ 0 号坦克：W A S D + SPACE ------
        if keys[pygame.K_w]: actions_p0["UP"]   = True
        if keys[pygame.K_s]: actions_p0["DOWN"] = True
        if keys[pygame.K_a]: actions_p0["LEFT"] = True
        if keys[pygame.K_d]: actions_p0["RIGHT"]= True
        if keys[pygame.K_SPACE]: actions_p0["SHOOT"] = True

        # ------ 1 号坦克：方向键 + 鼠标左键 ------
        if keys[pygame.K_UP]:    actions_p1["UP"]   = True
        if keys[pygame.K_DOWN]:  actions_p1["DOWN"] = True
        if keys[pygame.K_LEFT]:  actions_p1["LEFT"] = True
        if keys[pygame.K_RIGHT]: actions_p1["RIGHT"]= True
        if mb[0]:                actions_p1["SHOOT"]= True   # 鼠标左键

        return running, restart,actions_p0, actions_p1
