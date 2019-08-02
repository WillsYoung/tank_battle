import pygame
from threading import Thread
from time import sleep
from Music_and_Background import *
from Game_class import *


def tank_appear(n, screen):
    app = Brick()
    appear_picture = pygame.image.load(appear)
    if n == 1:
        app.rect = (384, 672, 48, 48)
    else:
        app.rect = (528, 672, 48, 48)
    for i in range(3):
        app.image = appear_picture.subsurface((i * 48, 0), (48, 48))
        app.draw(screen)
        pygame.display.flip()
        sleep(0.2)


def create_enemy_tank(n=1):
    if n == 1:
        return EnemyTank(randint(0, 3) * 240)
    return EnemyTank(), EnemyTank(240), EnemyTank(480), EnemyTank(720)


def create_food():
    chance = randint(1, 50)
    if chance == 1:
        return Supply()
    return False


def main():

    class FoodTimeThread(Thread):
        def run(self):
            while True:
                if len(foods) > 0:
                    sleep(8)
                    for f in foods:
                        f.life = False
                        foods.remove(f)
                else:
                    new_food = create_food()
                    if new_food:
                        foods.add(new_food)
                sleep(0.02)

    # 敌方坦克移动控制线程，主要用于玩家吃到定时时敌方坦克定身
    class EnemyTankMove(Thread):
        def run(self):
            for enemy in all_tanks:
                if enemy.name == 'enemy':
                    enemy.ismove = False
            sleep(8)
            for enemy in all_tanks:
                if enemy.name == 'enemy':
                    enemy.ismove = True

    class AllPictureDrawThread(Thread):
        def run(self):
            while True:
                screen.fill((0, 0, 0))
                # 将地图上的物件画出来
                # for brick in gamemap.bricks:
                #     if brick.name == 'homewall':
                #         brick.isiron = not brick.isiron
                #         if not brick.isiron:
                #             brick.degenerate()




                gamemap.draw(screen)
                # 判断所有坦克的生命值，将低于1的删除
                flag = True
                while flag:
                    flag = False
                    for tank in all_tanks:
                        if tank.life <= 0:
                            all_tanks.remove(tank)
                            flag = True

                # 判断所有子弹的生命值，低于1的即碰撞或者飞出界面之外的删除
                flag1 = True
                while flag1:
                    flag1 = False
                    for b in bullets:
                        if b.life <= 0:
                            bullets.remove(b)
                            flag1 = True

                all_tanks.draw(screen)   # 画出所有存活坦克
                bullets.draw(screen)     # 画出所有有效的子弹

                # 判断食物精灵组是否有食物，将它画出来
                if len(foods) > 0:
                    for f in foods:
                        if f.life:
                            if f.display:
                                f.draw(screen)        # 将食物画出来,并且处于一闪一闪状态
                            f.display = not f.display

                # 将坦克的保护套画出来
                for pro in protecteds:
                    if pro.time > 0:
                        pro.draw(screen)
                    else:
                        protecteds.remove(pro)

                pygame.display.flip()
                sleep(0.02)

    class TankMoveThread(Thread):
        def run(self):
            while True:
                nonlocal p1, p2
                # 所有有效坦克的移动，以及判断友方坦克是否吃到食物
                for tank in all_tanks:
                    if tank.ismove:
                        tank.move()
                        if tank.name == 'enemy' and tank.shoot():
                            bullets.add(tank.shoot())
                    # 判断保护套属于那辆坦克，并且其跟着坦克移动
                    for pro in protecteds:
                        if pro.name == tank.name:
                            pro.move(tank)

                    # 检测坦克有没有吃到食物，并且产生不同的效果
                    if tank.name == 'p1' or tank.name == 'p2':
                        tank_eat = pygame.sprite.spritecollide(tank, foods, True, pygame.sprite.collide_mask)
                        for food_eat in tank_eat:
                            print(food_eat.name)

                            if food_eat.name == 'iron':
                                for brik in gamemap.bricks:
                                    if brik.name == 'homewall':
                                        brik.change()
                            elif food_eat.name == 'boom':
                                for enemy_tank in all_tanks:
                                    if enemy_tank.name == 'enemy':
                                        enemy_tank.life = 0
                            elif food_eat.name == 'protect':
                                protecteds.add(Protect(tank))
                            elif food_eat.name == 'tank':
                                if tank.name == 'p1':
                                    p1 += 1
                                    print(p1)
                                else:
                                    p2 += 1
                                    print(p2)
                            elif food_eat.name == 'clock':
                                EnemyTankMove(daemon=True).start()
                            else:
                                tank.change_status(food_eat, tank)



                # 所有子弹的移动,不论敌我
                for i, bi in enumerate(bullets):
                    if bi.life:
                        bi.move()
                    for j, bj in enumerate(bullets):
                        if i != j:
                            # 检测所有子弹的碰撞，如果碰撞根据子弹威力的不同减少生命值
                            if pygame.sprite.collide_mask(bi, bj):
                                bi.life, bj.life = bi.life - bj.life, bj.life - bi.life

                sleep(0.02)

    def handle_keys(key):
        if t1.life > 0:
            if key == pygame.K_w:
                t1.change_dir(UP)
                # t1.speed = 3
            elif key == pygame.K_d:
                t1.change_dir(RIGHT)
                # t1.speed = 3
            elif key == pygame.K_s:
                t1.change_dir(DOWN)
                # t1.speed = 3
            elif key == pygame.K_a:
                t1.change_dir(LEFT)
                # t1.speed = 3
            elif key == pygame.K_SPACE:
                bullets.add(Bullet(t1))

        if t2.life > 0:
            if key == pygame.K_UP:
                t2.change_dir(UP)
                # t2.speed = 3
            elif key == pygame.K_RIGHT:
                t2.change_dir(RIGHT)
                # t2.speed = 3
            elif key == pygame.K_DOWN:
                t2.change_dir(DOWN)
                # t2.speed = 3
            elif key == pygame.K_LEFT:
                t2.change_dir(LEFT)
                # t2.speed = 3
            elif key == pygame.K_KP0:
                bullets.add(Bullet(t2))

        if key == pygame.K_F12:
            pass
        elif key == pygame.K_F11:
            pass
        elif key == pygame.K_F10:
            pass

    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption('坦克大战')

    # 建立子弹精灵组，建立玩家坦克精灵组,建立食物精灵组，home是地图是的砖块精灵组,创建保护套类
    protecteds = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_tanks = pygame.sprite.Group()
    foods = pygame.sprite.Group()
    # 创建出地图
    gamemap = Map()
    # 一个关卡所有敌方坦克共20辆
    all_enemy_tanks = 20
    # 玩家的初始坦克数量为3
    p1 = 3
    p2 = 3
    t1 = PlayerTank(1)
    t2 = PlayerTank(2)
    food = Supply()

    # 将所有的坦克放入到坦克精灵组中
    for e in create_enemy_tank(4):
        all_tanks.add(e)
    all_tanks.add(t1)
    all_tanks.add(t2)
    # 将食物放入到食物精灵组
    foods.add(food)

    pygame.init()

    AllPictureDrawThread(daemon=True).start()
    TankMoveThread(daemon=True).start()
    FoodTimeThread(daemon=True).start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keys(event.key)

        sleep(0.02)

    pygame.quit()


if __name__ == '__main__':
    main()