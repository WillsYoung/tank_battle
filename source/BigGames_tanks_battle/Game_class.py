import pygame
from time import sleep
from math import sqrt
from Music_and_Background import *
from random import randint

# 给四个运动方向定义数字，方便产生随机方向
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# 游戏结束的字体图片
gameover_word = 'music/image/gameover.png'

# 玩家坦克图片加载
tank1_0 = 'music/image/tank_T1_0.png'
tank1_1 = 'music/image/tank_T1_1.png'
tank1_2 = 'music/image/tank_T1_2.png'
tank2_0 = 'music/image/tank_T2_0.png'
tank2_1 = 'music/image/tank_T2_1.png'
tank2_2 = 'music/image/tank_T2_2.png'

# 敌方坦克图片加载
enemytank1_0 = 'music/image/enemy_1_0.png'
enemytank1_1 = 'music/image/enemy_1_1.png'
enemytank1_2 = 'music/image/enemy_1_2.png'
enemytank1_3 = 'music/image/enemy_1_3.png'
enemytank2_0 = 'music/image/enemy_2_0.png'
enemytank2_1 = 'music/image/enemy_2_1.png'
enemytank2_2 = 'music/image/enemy_2_2.png'
enemytank2_3 = 'music/image/enemy_2_3.png'
enemytank3_0 = 'music/image/enemy_3_0.png'
enemytank3_1 = 'music/image/enemy_3_1.png'
enemytank3_2 = 'music/image/enemy_3_2.png'
enemytank3_3 = 'music/image/enemy_3_3.png'
enemytank4_0 = 'music/image/enemy_4_0.png'
enemytank4_1 = 'music/image/enemy_4_1.png'
enemytank4_2 = 'music/image/enemy_4_2.png'
enemytank4_3 = 'music/image/enemy_4_3.png'


# 设置坦克出生特效图片组，5毛特效
appear_picture = pygame.image.load('music/image/appear.png')
appear_picture0 = appear_picture.subsurface(0, 0, 48, 48)
appear_picture1 = appear_picture.subsurface(48, 0, 48, 48)
appear_picture2 = appear_picture.subsurface(96, 0, 48, 48)
appear_pictures = [appear_picture0, appear_picture1, appear_picture2]


class Appear(pygame.sprite.Sprite):

    def __init__(self, tank):
        super().__init__()
        self.images = appear_pictures
        self.num = 0
        self.image = self.images[self.num]
        self.rect = (tank.rect[0], tank.rect[1], 48, 48)

    def draw(self, screen):
        self.image = self.images[self.num % 3]
        self.num += 1
        screen.blit(self.image, self.rect)


# 设置爆炸特效初始图片组，传说中的5毛特效
# 不同爆炸特性调用不同的图片子表面位置
boom_picture = pygame.image.load('music/image/boom_dynamic.png')
boom_picture0 = boom_picture.subsurface(36, 36, 24, 24)
boom_picture1 = boom_picture.subsurface(126, 30, 36, 36)
boom_picture2 = boom_picture.subsurface(216, 24, 48, 48)
boom_picture3 = boom_picture.subsurface(306, 18, 60, 60)
boom_picture4 = boom_picture.subsurface(384, 0, 96, 96)
boom_picture5 = boom_picture.subsurface(504, 24, 48, 48)
boom_pictures = [boom_picture0, boom_picture1, boom_picture2,
                 boom_picture3, boom_picture4, boom_picture5]


# 砖块类，地图上的各种障碍物基础图片的一个单位，包括普通砖块，金砖，树，河流，冰面
class Brick(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        super().__init__()
        self.life = True
        self.name = 'brick'
        self.image = pygame.image.load('music/image/brick.png').convert_alpha()
        self.rect = (x, y, 24, 24)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# 玩家基地类，当它被击中时游戏结束
class HomeBase(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.life = True
        self.name = 'player_base'
        self.image = pygame.image.load('music/image/home.png').convert_alpha()
        self.rect = (456, 672, 48, 48)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class HomeWall(Brick):

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = 'homewall'
        self.isiron = 20
        self.exist = True
        self.home_wall_bricks = pygame.sprite.Group()
        # 创建老家的墙
        for i in range(4):
            rb = Brick(432, 720 - i * 24)
            self.home_wall_bricks.add(rb)
        for i in range(2):
            b = Brick(456 + i * 24, 648)
            self.home_wall_bricks.add(b)
        for i in range(4):
            rb = Brick(504, 720 - i * 24)
            self.home_wall_bricks.add(rb)

    def change(self):
        # self.isiron = 10
        self.home_wall_bricks = pygame.sprite.Group()
        for i in range(4):
            rb = Brick(432, 720 - i * 24)
            self.home_wall_bricks.add(rb)
        for i in range(2):
            b = Brick(456 + i * 24, 648)
            self.home_wall_bricks.add(b)
        for i in range(4):
            rb = Brick(504, 720 - i * 24)
            self.home_wall_bricks.add(rb)
        for brick in self.home_wall_bricks:
            brick.image = pygame.image.load('music/image/iron.png').convert_alpha()
            brick.life = 10000

    def degenerate(self):
        for brick in self.home_wall_bricks:
            brick.life = 1
            brick.image = pygame.image.load('music/image/brick.png').convert_alpha()


# 地图上各种障碍物的集合体，就是地图
class Map(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.home = HomeBase()
        self.bricks = pygame.sprite.Group()
        self.bricks.add(self.home)

        # 创建普通的墙
        for i in range(8):
            for j in range(3):
                for k in range(12):
                    rb = Brick(128 * i + j * 24, 150 + k * 24)
                    self.bricks.add(rb)

    def draw(self, screen):
        self.bricks.draw(screen)


# 玩家坦克类
class PlayerTank(pygame.sprite.Sprite):

    def __init__(self, which_player):
        super().__init__()

        if which_player == 1:
            self.name = 'p1'
            self.tank_l0 = pygame.image.load(tank1_0).convert_alpha()
            self.tank_l1 = pygame.image.load(tank1_1).convert_alpha()
            self.tank_l2 = pygame.image.load(tank1_2).convert_alpha()
            self.x = 384
            self.y = 672
        if which_player == 2:
            self.name = 'p2'
            self.tank_l0 = pygame.image.load(tank2_0).convert_alpha()
            self.tank_l1 = pygame.image.load(tank2_1).convert_alpha()
            self.tank_l2 = pygame.image.load(tank2_2).convert_alpha()
            self.x = 528
            self.y = 672
        self.rect = (self.x, self.y, 48, 48)
        # 初始都是一级坦克
        self.level = 1
        self.tank = self.tank_l0
        # 获取四个方向的坦克图片
        self.tankup = self.tank.subsurface(0, 0, 48, 48)
        self.tankdown = self.tank.subsurface(0, 48, 48, 48)
        self.tankleft = self.tank.subsurface(0, 96, 48, 48)
        self.tankright = self.tank.subsurface(0, 144, 48, 48)
        # 坦克初始方向都是向上,初始速度 3,初始生命为 1,并且初始状态可以动为True
        self.ismove = True
        self.dir = UP
        self.life = 1
        self.speed = 3
        self.bullet_speed = 10
        self.image = self.tankup
        self.mask = pygame.mask.from_surface(self.image)

    # 玩家吃到食物，坦克升级改变相应的图片与生命值
    def change_status(self, food, tank):
        if tank.name == 'p1':
            self.tank_l0 = pygame.image.load(tank1_0).convert_alpha()
            self.tank_l1 = pygame.image.load(tank1_1).convert_alpha()
            self.tank_l2 = pygame.image.load(tank1_2).convert_alpha()
        elif tank.name == 'p2':
            self.tank_l0 = pygame.image.load(tank2_0).convert_alpha()
            self.tank_l1 = pygame.image.load(tank2_1).convert_alpha()
            self.tank_l2 = pygame.image.load(tank2_2).convert_alpha()
        if food.name == 'gun':
            self.level = 3
            self.life = 3
        elif food.name == 'star':
            if self.level <= 3:
                self.level += 1
                self.life = self.level
        if self.level == 2:
            self.tank = self.tank_l1
            self.speed = 4
            self.bullet_speed = 15
            self.tankup = self.tank.subsurface(0, 0, 48, 48)
            self.tankdown = self.tank.subsurface(0, 48, 48, 48)
            self.tankleft = self.tank.subsurface(0, 96, 48, 48)
            self.tankright = self.tank.subsurface(0, 144, 48, 48)
        elif self.level == 3:
            self.tank = self.tank_l2
            self.speed = 5
            self.bullet_speed = 20
            self.tankup = self.tank.subsurface(0, 0, 48, 48)
            self.tankdown = self.tank.subsurface(0, 48, 48, 48)
            self.tankleft = self.tank.subsurface(0, 96, 48, 48)
            self.tankright = self.tank.subsurface(0, 144, 48, 48)

    def level_down(self, bullet):
        self.life -= bullet.life
        self.level = self.life
        if self.level == 2:
            self.tank = self.tank_l1
            self.tankup = self.tank.subsurface(0, 0, 48, 48)
            self.tankdown = self.tank.subsurface(0, 48, 48, 48)
            self.tankleft = self.tank.subsurface(0, 96, 48, 48)
            self.tankright = self.tank.subsurface(0, 144, 48, 48)
        # elif self.level == 3:
        #     self.tank = self.tank_l2
        #     self.tankup = self.tank.subsurface(0, 0, 48, 48)
        #     self.tankdown = self.tank.subsurface(0, 48, 48, 48)
        #     self.tankleft = self.tank.subsurface(0, 96, 48, 48)
        #     self.tankright = self.tank.subsurface(0, 144, 48, 48)
        elif self.level == 1:
            self.tank = self.tank_l0
            self.tankup = self.tank.subsurface(0, 0, 48, 48)
            self.tankdown = self.tank.subsurface(0, 48, 48, 48)
            self.tankleft = self.tank.subsurface(0, 96, 48, 48)
            self.tankright = self.tank.subsurface(0, 144, 48, 48)

    def change_dir(self, now_dir):
        self.dir = now_dir

    def move(self):
        if self.dir == UP:
            self.y -= self.speed
            self.image = self.tankup
            if self.y <= 0:
                self.y = 0
        elif self.dir == RIGHT:
            self.x += self.speed
            self.image = self.tankright
            if self.x + 48 >= 960:
                self.x = 912
        elif self.dir == DOWN:
            self.y += self.speed
            self.image = self.tankdown
            if self.y + 48 >= 720:
                self.y = 672
        elif self.dir == LEFT:
            self.x -= self.speed
            self.image = self.tankleft
            if self.x <= 0:
                self.x = 0
        self.rect = (self.x, self.y, 48, 48)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# 敌方坦克类
class EnemyTank(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        super().__init__()
        # 初始状态可以动为 True
        self.ismove = True
        self.level = randint(1, 20)
        self.name = 'enemy'
        self.ready_fire = True
        self.bullet_speed = 10
        if self.level in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            self.tank_l0 = pygame.image.load(enemytank1_0).convert_alpha()
            self.tank_l1 = pygame.image.load(enemytank1_1).convert_alpha()
            self.tank_l2 = pygame.image.load(enemytank1_2).convert_alpha()
            self.tank_l3 = pygame.image.load(enemytank1_3).convert_alpha()
            self.x = x
            self.y = y
            self.life = 1
            self.speed = 1
        elif self.level in [11, 12, 13, 14, 15, 16]:
            self.tank_l0 = pygame.image.load(enemytank2_0).convert_alpha()
            self.tank_l1 = pygame.image.load(enemytank2_1).convert_alpha()
            self.tank_l2 = pygame.image.load(enemytank2_2).convert_alpha()
            self.tank_l3 = pygame.image.load(enemytank2_3).convert_alpha()
            self.x = x
            self.y = y
            self.life = 2
            self.speed = 2
        elif self.level in [17, 18, 19]:
            self.tank_l0 = pygame.image.load(enemytank3_0).convert_alpha()
            self.tank_l1 = pygame.image.load(enemytank3_1).convert_alpha()
            self.tank_l2 = pygame.image.load(enemytank3_2).convert_alpha()
            self.tank_l3 = pygame.image.load(enemytank3_3).convert_alpha()
            self.x = x
            self.y = y
            self.life = 3
            self.speed = 3
        elif self.level == 20:
            self.tank_l0 = pygame.image.load(enemytank4_0).convert_alpha()
            self.tank_l1 = pygame.image.load(enemytank4_1).convert_alpha()
            self.tank_l2 = pygame.image.load(enemytank4_2).convert_alpha()
            self.tank_l3 = pygame.image.load(enemytank4_3).convert_alpha()
            self.x = x
            self.y = y
            self.life = 4
            self.speed = 4
        self.rect = (self.x, self.y, 48, 48)

        # 通过随机数选择不同的坦克颜色
        self.color = randint(0, 3)
        if self.color == 0:
            self.tank = self.tank_l0
        elif self.color == 1:
            self.tank = self.tank_l1
        elif self.color == 2:
            self.tank = self.tank_l2
        elif self.color == 3:
            self.tank = self.tank_l3

        # 获取四个方向的敌方坦克图片
        self.tankup = self.tank.subsurface(0, 0, 48, 48)
        self.tankdown = self.tank.subsurface(0, 48, 48, 48)
        self.tankleft = self.tank.subsurface(0, 96, 48, 48)
        self.tankright = self.tank.subsurface(0, 144, 48, 48)

        # 敌方坦克初始方向为 下 右 左 通过随机数产生
        self.dir = randint(1, 3)
        if self.dir == 1:
            self.image = self.tankright
        elif self.dir == 2:
            self.image = self.tankdown
        elif self.dir == 3:
            self.image = self.tankleft
        # 敌方坦克初始开火设置为不开火
        self.fire = 0
        # 掩码设置，方便碰撞时进行实际碰撞的位置检测
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.dir == UP:
            self.y -= self.speed
            self.image = self.tankup
            if self.y <= 0:
                self.y = 0
                self.dir = randint(0, 3)
        elif self.dir == RIGHT:
            self.x += self.speed
            self.image = self.tankright
            if self.x + 48 >= 960:
                self.x = 912
                self.dir = [0, 2, 3][randint(0, 2)]
        elif self.dir == DOWN:
            self.y += self.speed
            self.image = self.tankdown
            if self.y + 48 >= 720:
                self.y = 672
                self.dir = [0, 1, 3][randint(0, 2)]
        elif self.dir == LEFT:
            self.x -= self.speed
            self.image = self.tankleft
            if self.x <= 0:
                self.x = 0
                self.dir = randint(0, 2)
        self.rect = (self.x, self.y, 48, 48)
        self.fire = randint(1, 80)
        # if self.fire == 1:
        #     Bullet(self)

    def shoot(self):
        if self.fire == 1:
            return Bullet(self)
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# 子弹类，由玩家坦克或者敌方坦克发射，具有不同的威力
class Bullet(pygame.sprite.Sprite):

    def __init__(self, tank):
        super().__init__()
        self.dir = tank.dir
        self.speed = tank.bullet_speed
        self.x = tank.rect[0]
        self.y = tank.rect[1]
        # 子弹具有敌我识别属性，依靠name属性实现
        self.name = tank.name
        self.life = tank.life if tank.name != 'enemy' else 1
        # 只有当子弹存在的时候才会被画出来，并且还表示子弹的威力
        if self.dir == UP:
            self.image = pygame.image.load('music/image/bullet_up.png')
            self.rect = (self.x + 18, self.y, 12, 12)
        if self.dir == RIGHT:
            self.image = pygame.image.load('music/image/bullet_right.png')
            self.rect = (self.x + 48, self.y + 18, 12, 12)
        if self.dir == DOWN:
            self.image = pygame.image.load('music/image/bullet_down.png')
            self.rect = (self.x + 18, self.y + 48, 12, 12)
        if self.dir == LEFT:
            self.image = pygame.image.load('music/image/bullet_left.png')
            self.rect = (self.x, self.y + 18, 12, 12)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.dir == UP:
            self.y -= self.speed
            self.rect = (self.x + 18, self.y, 12, 12)
            if self.y <= 0:
                self.life = False
        if self.dir == RIGHT:
            self.x += self.speed
            self.rect = (self.x + 48, self.y + 18, 12, 12)
            if self.x + 48 >= 960:
                self.life = False
        if self.dir == DOWN:
            self.y += self.speed
            self.rect = (self.x + 18, self.y + 48, 12, 12)
            if self.y + 48 >= 720:
                self.life = False
        if self.dir == LEFT:
            self.x -= self.speed
            self.rect = (self.x, self.y + 18, 12, 12)
            if self.x <= 0:
                self.life = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# 所有坦克补给图片加载
food_tank = 'music/image/food_tank.png'        # 玩家增加一辆坦克
food_boom = 'music/image/food_boom.png'        # 炸毁当前地图上所有敌方坦克
food_clock = 'music/image/food_clock.png'      # 所有敌方坦克定身 8s
food_gun = 'music/image/food_gun.png'          # 使玩家的坦克等级为最高，生命值增加且子弹变为金枪，威力为3
food_iron = 'music/image/food_iron.png'        # 使玩家的老家变为金砖状态32s
food_protect = 'music/image/food_protect.png'  # 玩家坦克成为无敌状态16s
food_satr = 'music/image/food_star.png'        # 玩家坦克等级+1，生命和子弹威力 +1
supply_picture = [food_tank, food_boom, food_clock, food_gun, food_iron, food_protect, food_satr]
supply_name = ['tank', 'boom', 'clock', 'gun', 'iron', 'protect', 'star']


class Supply(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.life = True
        self.display = True
        self.flag = True
        self.num = randint(0, 6)
        self.name = supply_name[self.num]
        self.image = pygame.image.load(supply_picture[self.num]).convert_alpha()
        self.rect = (randint(0, 928), randint(0, 688), 32, 32)
        # self.rect = (410, 700, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Protect(pygame.sprite.Sprite):

    def __init__(self, tank):
        super().__init__()
        self.name = tank.name
        self.time = 16
        self.begin_image = pygame.image.load('music/image/begin_protect.png').convert_alpha()
        self.all_images = [self.begin_image.subsurface(0, 0, 48, 48), self.begin_image.subsurface(48, 0, 48, 48)]
        self.num = True
        self.image = self.all_images[self.num]
        self.rect = (0, 0, 0, 0)

    def move(self, tank):
        self.time -= 0.02
        self.rect = tank.rect

    def draw(self, screen):
        self.image = self.all_images[self.num]
        screen.blit(self.image, self.rect)
        self.num = not self.num