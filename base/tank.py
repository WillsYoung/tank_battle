from copy import deepcopy
import time
import pygame

from config.base_config import SCREEN_SIZE, UP, DOWN, RIGHT, LEFT, TANK_SIZE, BULLET_SIZE, \
                               SCREEN_REFRESH




# 游戏结束的字体图片
gameover_word = 'source/image/gameover.png'

# 子弹图片加载，所有等级的子弹都一样，只是威力、速度变化
bullet_up = 'source/image/bullet_up.png'
bullet_right = 'source/image/bullet_right.png'
bullet_down = 'source/image/bullet_down.png'
bullet_left = 'source/image/bullet_left.png'

# 玩家坦克图片加载
tank1_0 = 'source/image/tank_T1_0.png'
tank1_1 = 'source/image/tank_T1_1.png'
tank1_2 = 'source/image/tank_T1_2.png'
tank2_0 = 'source/image/tank_T2_0.png'
tank2_1 = 'source/image/tank_T2_1.png'
tank2_2 = 'source/image/tank_T2_2.png'

# 敌方坦克图片加载
enemytank1_0 = 'source/image/enemy_1_0.png'
enemytank1_1 = 'source/image/enemy_1_1.png'
enemytank1_2 = 'source/image/enemy_1_2.png'
enemytank1_3 = 'source/image/enemy_1_3.png'
enemytank2_0 = 'source/image/enemy_2_0.png'
enemytank2_1 = 'source/image/enemy_2_1.png'
enemytank2_2 = 'source/image/enemy_2_2.png'
enemytank2_3 = 'source/image/enemy_2_3.png'
enemytank3_0 = 'source/image/enemy_3_0.png'
enemytank3_1 = 'source/image/enemy_3_1.png'
enemytank3_2 = 'source/image/enemy_3_2.png'
enemytank3_3 = 'source/image/enemy_3_3.png'
enemytank4_0 = 'source/image/enemy_4_0.png'
enemytank4_1 = 'source/image/enemy_4_1.png'
enemytank4_2 = 'source/image/enemy_4_2.png'
enemytank4_3 = 'source/image/enemy_4_3.png'

# 设置爆炸特效初始图片组，传说中的5毛特效
# 不同爆炸特性调用不同的图片子表面位置
boom_picture = pygame.image.load('source/image/boom_dynamic.png')
boom_picture0 = boom_picture.subsurface(36, 36, 24, 24)
boom_picture1 = boom_picture.subsurface(126, 30, 36, 36)
boom_picture2 = boom_picture.subsurface(216, 24, 48, 48)
boom_picture3 = boom_picture.subsurface(306, 18, 60, 60)
boom_picture4 = boom_picture.subsurface(384, 0, 96, 96)
boom_picture5 = boom_picture.subsurface(504, 24, 48, 48)
boom_pictures = [boom_picture0, boom_picture1, boom_picture2,
                 boom_picture3, boom_picture4, boom_picture5]


class Tank(object):

    def __init__(self):
        self.__image = pygame.image.load(tank1_0).convert_alpha()

        # 获取四个方向的坦克图片
        self.__tank_image_up = self.__image.subsurface(0, 0, TANK_SIZE, TANK_SIZE)
        self.__tank_image_down = self.__image.subsurface(0, TANK_SIZE, TANK_SIZE, TANK_SIZE)
        self.__tank_image_left = self.__image.subsurface(0, TANK_SIZE*2, TANK_SIZE, TANK_SIZE)
        self.__tank_image_right = self.__image.subsurface(0, TANK_SIZE*3, TANK_SIZE, TANK_SIZE)
        self.__tank = self.__tank_image_up
        # 设置初始方向、速度、生命、等级、武器、移动状态、位置、初始矩形
        self.__dir = UP
        self.__speed = 0.5
        self.__hp = 1
        self.__level = 1
        self.__weapon = None
        self.__fired_bullets = []
        self.__is_move = False
        self.__x = 300
        self.__y = SCREEN_SIZE[1] - TANK_SIZE
        self.__rect = (self.__x, self.__y, TANK_SIZE, TANK_SIZE)
        # 设置掩码碰撞，只有图片内部真正碰到才会碰撞
        self.mask = pygame.mask.from_surface(self.__tank)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_level(self):
        return self.__level

    def set_is_move(self, is_move):
        if self.__is_move is not None:
            self.__is_move = is_move

    def change_is_move(self):
        if self.__is_move is None:
            self.__is_move = False
        else:
            self.__is_move = None

    def set_dir(self, new_dir):
        self.__dir = new_dir

    def get_dir(self):
        return self.__dir

    def moving(self):
        if self.__is_move:
            if self.__dir == UP:
                self.__y -= self.__speed
                self.__tank = self.__tank_image_up
                if self.__y <= 0:
                    self.__y = 0
            elif self.__dir == RIGHT:
                self.__x += self.__speed
                self.__tank = self.__tank_image_right
                if self.__x + TANK_SIZE >= SCREEN_SIZE[0]:
                    self.__x = SCREEN_SIZE[0] - TANK_SIZE
            elif self.__dir == DOWN:
                self.__y += self.__speed
                self.__tank = self.__tank_image_down
                if self.__y + TANK_SIZE >= SCREEN_SIZE[1]:
                    self.__y = SCREEN_SIZE[1] - TANK_SIZE
            else:
                self.__x -= self.__speed
                self.__tank = self.__tank_image_left
                if self.__x <= 0:
                    self.__x = 0
        # print(self.__x, self.__y)
        # print(self.__is_move)
        self.__rect = (self.__x, self.__y, TANK_SIZE, TANK_SIZE)

    def fire(self, screen):
        self.reload()
        fired_bullet = deepcopy(self.__weapon)
        self.__fired_bullets.append(fired_bullet)
        fired_bullet.attack(screen)
        self.__weapon = None


    def reload(self):
        if self.__level == 1:
            sleep_time = 0.2
        elif self.__level == 2:
            sleep_time = 0.1
        else:
            sleep_time = 0.01
        time.sleep(sleep_time)
        self.__weapon = Weapon()
        self.__weapon.ready(self)

    def level_up(self):
        pass

    def level_down(self):
        pass

    def draw(self, screen):
        if self.__hp > 0:
            screen.blit(self.__tank, self.__rect)
            # for bullet in self.__fired_bullets:
            #     print(bullet.get_attack())
            #     if bullet.get_attack() > 0:
            #         print("fired bullet hp", bullet)
            #         bullet.draw(screen)
            #     # else:
            #     #     print(bullet)
                #     self.__fired_bullets.remove(bullet)
            # pygame.display.flip()


class Weapon(object):
    """武器类，依托坦克实现"""
    def __init__(self):
        self.__bullet_up = None
        self.__bullet_left = None
        self.__bullet_down = None
        self.__bullet_right = None
        # 设置初始速度、攻击力、等级、位置、方向
        self.__speed = 0
        self.__attack = 0
        self.__level = 1
        self.__bullet = None
        self.__dir = None
        self.__x = 0
        self.__y = 0
        self.__rect = None

    def do_init(self):
        self.__bullet_up = pygame.image.load(bullet_up).convert_alpha()
        self.__bullet_left = pygame.image.load(bullet_left).convert_alpha()
        self.__bullet_down = pygame.image.load(bullet_down).convert_alpha()
        self.__bullet_right = pygame.image.load(bullet_right).convert_alpha()

    def get_attack(self):
        return self.__attack

    def ready(self, tank):
        self.__x, self.__y = self.get_location(tank.get_x(), tank.get_y(), tank.get_dir())
        self.__attack = self.__level = tank.get_level()
        self.__speed = self.__level + 2
        self.__dir = tank.get_dir()

    def attack(self, screen):
        self.do_init()
        print(self.__x, self.__y)
        while self.__attack > 0:
            self.moving()
            self.draw(screen)
            time.sleep(SCREEN_REFRESH)

    def moving(self):
        print(self.__x, self.__y)
        if self.__dir == UP:
            self.__bullet = self.__bullet_up
            self.__y -= self.__speed
            if self.__y <= 0:
                self.__y = 0
                self.__attack = 0
        elif self.__dir == RIGHT:
            self.__bullet = self.__bullet_right
            self.__x += self.__speed
            if self.__x + BULLET_SIZE >= SCREEN_SIZE[0]:
                self.__x = SCREEN_SIZE[0] - BULLET_SIZE
                self.__attack = 0
        elif self.__dir == DOWN:
            self.__bullet = self.__bullet_down
            self.__y += self.__speed
            if self.__y + BULLET_SIZE >= SCREEN_SIZE[1]:
                self.__y = SCREEN_SIZE[1] - BULLET_SIZE
                self.__attack = 0
        else:
            self.__bullet = self.__bullet_left
            self.__x -= self.__speed
            if self.__x <= 0:
                self.__x = 0
                self.__attack = 0
        # print(self.__x, self.__y)
        self.__rect = (self.__x, self.__y, BULLET_SIZE, BULLET_SIZE)

    def get_location(self, x, y, tank_dir):
        temp_size = (TANK_SIZE - BULLET_SIZE) / 2
        if tank_dir == UP:
            self.__x = x + temp_size
            self.__y = y
        elif tank_dir == LEFT:
            self.__x = x
            self.__y = y + temp_size
        elif tank_dir == DOWN:
            self.__x = x + temp_size
            self.__y = y + TANK_SIZE - BULLET_SIZE
        else:
            self.__x = x + TANK_SIZE - BULLET_SIZE
            self.__y = y + temp_size
        return self.__x, self.__y


    def draw(self, screen):
        if self.__attack > 0:
            print("画出子弹")
            print(self.__bullet)
            print(self.__rect)
            screen.blit(self.__bullet, self.__rect)