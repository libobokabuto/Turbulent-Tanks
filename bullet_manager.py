from bullet import Bullet
import pygame

class BulletManager:
    def __init__(self):
        """
        初始化子弹管理器
        负责人: wobudao1a​
        """
        self.bullets = []

    def spawn(self, x: int, y: int, direction: str, owner_id: int):
        """
        生成新子弹
        负责人: wobudao1a​
        Args:
            x (int): 生成x坐标
            y (int): 生成y坐标
            direction (str): 移动方向（'UP'/'DOWN'/'LEFT'/'RIGHT'）
            owner_id (int): 发射者ID
        """
        new_bullet = Bullet(x, y, direction, owner_id)
        self.bullets.append(new_bullet)

    def update_all(self, game_map, tanks: list):
        """
        更新所有子弹状态
        负责人: wobudao1a​
        Args:
            game_map (Game_map): 地图对象
            tanks (list): 坦克列表
        """
        for bullet in self.bullets:
            bullet.update(game_map)
            if bullet.check_collision(tanks):
                self.bullets.remove(bullet)
        self.bullets = [b for b in self.bullets if b.alive]

    def get_all(self):
        """
        获取所有存活子弹
        负责人: wobudao1a​
        Returns:
            list: 存活子弹列表
        """
        return self.bullets

    def clear(self):
        """
        清空所有子弹
        负责人: wobudao1a​
        """
        self.bullets.clear()