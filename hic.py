# hic.py
import pygame


class HCIManager:
    """
    人机交互模块：监听玩家输入，并分别返回 0 号和 1 号坦克的动作。、
    负责人：Yiv(第一版)
           Thousand(第二版)
           libobokabuto(第三版)
    """
    @staticmethod
    def _blank_actions():
        """
        生成空的动作字典
        所有动作均为 False
        负责人: Yiv(第一版)
           Thousand(第二版)
           libobokabuto(第三版)
        Returns:
            dict: 键为动作名，值均为 False 的动作字典
        """
        return {
            "UP": False, "DOWN": False, "LEFT": False, "RIGHT": False,
            "SHOOT": False, "SWITCH_MENU": False
        }

    def handle_events(self):
        """
        处理所有 Pygame 事件并返回游戏状态与玩家动作
        监听窗口关闭、重启、菜单切换及坦克操作输入
        负责人: Yiv(第一版)
                Thousand(第二版)
                libobokabuto(第三版)
        Returns:
            running (bool): False ⇒ 退出游戏
            restart (bool): True ⇒ 重启当前关卡
            actions_p0 (dict): 0 号坦克（WASD / SPACE）的动作字典
            actions_p1 (dict): 1 号坦克（方向键 / 鼠标左键）的动作字典
        """
        # 重启标志 & 空动作初始值
        restart = False
        actions_p0 = self._blank_actions()
        actions_p1 = self._blank_actions()

        # 扫描所有事件
        for event in pygame.event.get():
            # 检测到窗口关闭，立即退出
            if event.type == pygame.QUIT:
                return False, False, self._blank_actions(), self._blank_actions()

            # 切换菜单（Esc/Tab）
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                actions_p0["SWITCH_MENU"] = actions_p1["SWITCH_MENU"] = True

            # 按 R 重启
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart = True

        # 连续按键与鼠标状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restart = True
            
        mb   = pygame.mouse.get_pressed(3)

        # ------ 0 号坦克：W A S D + SPACE ------
        if keys[pygame.K_w]:      actions_p0["UP"]    = True
        if keys[pygame.K_s]:      actions_p0["DOWN"]  = True
        if keys[pygame.K_a]:      actions_p0["LEFT"]  = True
        if keys[pygame.K_d]:      actions_p0["RIGHT"] = True
        if keys[pygame.K_SPACE]:  actions_p0["SHOOT"] = True

        # ------ 1 号坦克：方向键 + 鼠标左键 ------
        if keys[pygame.K_UP]:     actions_p1["UP"]    = True
        if keys[pygame.K_DOWN]:   actions_p1["DOWN"]  = True
        if keys[pygame.K_LEFT]:   actions_p1["LEFT"]  = True
        if keys[pygame.K_RIGHT]:  actions_p1["RIGHT"] = True
        if mb[0]:                 actions_p1["SHOOT"] = True

        # 正常运行，返回 running=True
        return True, restart, actions_p0, actions_p1
