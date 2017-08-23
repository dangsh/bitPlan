import pygame
import traceback
import sys
from pygame.locals import *
import myPlane
import enemy
import bullet

# 定义颜色
BLACK = (0,0,0);
RED = (255,0,0);
GREEN = (0,255,0);
BLUE = (0,0,255);
WHITE = (255,255,255);



pygame.init();

# # 加载音频资源
# pygame.mixer.init();
# pygame.mixer.music.load("mp3/game_music.wav");
# pygame.mixer.music.set_volume(1);


# bullet = pygame.mixer.Sound("mp3/bullet.mp3"); 
# bullet.set_volume(.6);


bg_size = width , height = 320 , 568

screen = pygame.display.set_mode(bg_size);
pygame.display.set_caption("微信打飞机");

background = pygame.image.load("gameArts/background_2.png").convert_alpha();

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size);
        group1.add(e1);
        group2.add(e1);
def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size);
        group1.add(e2);
        group2.add(e2);
def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size);
        group1.add(e3);
        group2.add(e3);



#增加所有飞机的速度
def increseEnemySpeed(enemyList):
    for each in enemyList:
        each.speed += 1;

    



def main():
    clock = pygame.time.Clock();
    # pygame.mixer.music.play(-1);

    #用于切换图片
    switchImage = True;

    #用于延迟
    delay = 100;

        
    #分数
    score = 0;
    score_font = pygame.font.Font("AaxiaoNangua.ttf",36);


    #设置游戏难度级别
    level = 1;

    running = True;

    # 创建英雄飞机
    me = myPlane.MyPlane(bg_size);
    enemies = pygame.sprite.Group();

    # 生成普通子弹
    bullet1 = [];
    bullet1_index = 0;
    bullet1_num = 4;

    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))


    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group();
    add_small_enemies(enemies,small_enemies,15);


    #生成敌方中型飞机
    mid_enemies = pygame.sprite.Group();
    add_mid_enemies(enemies,mid_enemies,4);


    #生成敌方大型飞机
    big_enemies = pygame.sprite.Group();
    add_big_enemies(enemies,big_enemies,2);

    #中弹图片索引
    e1_destroy_index = 0;
    e2_destroy_index = 0;
    e3_destroy_index = 0;
    me_destroy_index = 0;


    
    # 游戏运行
    while running:

        # 根据用户的得分情况，改变游戏级别
        if level == 1 and score > 100:
            level = 2;
            add_small_enemies(small_enemies,enemies,3);
            add_mid_enemies(mid_enemies,enemies,2);
            add_big_enemies(big_enemies,enemies,1);
            increseEnemySpeed(enemies);
        elif level == 2 and score >200:
            level = 3;
            add_small_enemies(small_enemies,enemies,3);
            add_mid_enemies(mid_enemies,enemies,2);
            add_big_enemies(big_enemies,enemies,1);
            increseEnemySpeed(enemies);
        elif level == 3 and score >500:
            level = 4;
            add_small_enemies(small_enemies,enemies,3);
            add_mid_enemies(mid_enemies,enemies,2);
            add_big_enemies(big_enemies,enemies,1);
            increseEnemySpeed(enemies);

        # 事件队列
        for event in pygame.event.get():
            # 退出事件
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();

        # 检测用户的键盘操作
        key_pressed = pygame.key.get_pressed();
        if key_pressed[K_w] or key_pressed[pygame.K_UP]:
            me.moveUp();
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown();
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft();
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight();
        
        # 渲染游戏对象
        screen.blit(background , (0 , 0));


        # 开始发射子弹
        if not delay%10:
            bullet1[bullet1_index].reset(me.rect.midtop);
            bullet1_index = (bullet1_index + 1) % bullet1_num;

        # 检测子弹是否击中敌人飞机
        for b in bullet1:
            if b.active:
                b.move();
                screen.blit(b.image,b.rect);
                enemy_hit = pygame.sprite.spritecollide(b , enemies , False ,pygame.sprite.collide_mask);
                if enemy_hit:
                    b.active = False ;
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies:
                            e.hp -= 1;
                            e.hit = True;

                            if e.hp == 0:
                                e.active = False;

                        else:
                            e.active = False;

                        


        # 绘制大型飞机
        for each in big_enemies:
            if each.active:
                each.move();
                if each.hit:
                    screen.blit(each.image_hit , each.rect);
                    each.hit =False;
                else:
                    if switchImage:
                        screen.blit(each.image1,each.rect);
                    else:
                        screen.blit(each.image2,each.rect);

                # 绘制血槽
                pygame.draw.line(screen , BLACK , (each.rect.left,each.rect.top - 10), (each.rect.right,each.rect.top - 10), 2);
                # 当生命大于20%的时候显示绿色，否则红色
                enemy_remain = each.hp / enemy.BigEnemy.hp;
                if enemy_remain >0.2:
                    yanse = GREEN;
                else:
                    yanse = RED;


                pygame.draw.line(screen , yanse , (each.rect.left,each.rect.top - 10) , (each.rect.left + each.rect.width * enemy_remain ,each.rect.top - 10) , 2);

            else:
                #毁灭
                    if not (delay % 4):
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect);
                        e3_destroy_index=(e3_destroy_index + 1) % 7;
                        if e3_destroy_index == 0:
                            each.reset();

                    

        # 绘制中型飞机
        for each in mid_enemies:
            
            if each.active:
                each.move();
                if each.hit:
                    screen.blit(each.image_hit , each.rect);
                    each.hit =False;
                else:
                    screen.blit(each.image,each.rect);

                # 绘制血槽
                pygame.draw.line(screen , BLACK , (each.rect.left,each.rect.top - 10), (each.rect.right,each.rect.top - 10), 2);
                 # 当生命大于20%的时候显示绿色，否则红色
                enemy_remain = each.hp / enemy.MidEnemy.hp;
                if enemy_remain >0.2:
                    yanse = GREEN;
                else:
                    yanse = RED;


                pygame.draw.line(screen , yanse , (each.rect.left,each.rect.top - 10) , (each.rect.left + each.rect.width * enemy_remain ,each.rect.top - 10) , 2);

            else:
                    #毁灭
                    if not (delay % 4):
                        screen.blit(each.destroy_images[e2_destroy_index],each.rect);
                        e2_destroy_index=(e2_destroy_index + 1) % 4;
                        if e2_destroy_index == 0:
                            each.reset();    
        # 绘制小型飞机
        for each in small_enemies:
            if each.active:
                each.move();
                screen.blit(each.image,each.rect);
            else:
                    #毁灭
                    if not (delay % 4):
                        screen.blit(each.destroy_images[e1_destroy_index],each.rect);
                        e1_destroy_index=(e1_destroy_index + 1) % 4;
                        if e1_destroy_index == 0:
                            score += 10;
                            each.reset();   


        # 检查是否被碰撞
        # enemies_down = pygame.sprite.spritecollide(me,enemies,False);
        enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask);
        if enemies_down:
            me.active = False;
            for e in enemies_down:
                e.active = False;

    
        # 绘制我方飞机
        if me.active:
            if switchImage:
                screen.blit(me.image1 , me.rect);
            else:  
                screen.blit(me.image2 , me.rect);
        else:
                    #毁灭
                    if not (delay % 4):
                        screen.blit(me.destroy_images[me_destroy_index],each.rect);
                        me_destroy_index=(me_destroy_index + 1) % 4;
                        if me_destroy_index == 0:
                            # me.reset();

                            #退出游戏
                            running = False;



        #显示分数
        score_text = score_font.render("分数： %s" % str(score),True,RED);
        screen.blit(score_text,(0,0));


        #切换图片

        if not (delay%5):
            switchImage = not switchImage;

        delay -=1;
        if not delay:
            delay = 100;

        # 更新游戏对象到界面上
        pygame.display.flip();
        clock.tick(60);

# 运行游戏
if __name__ == "__main__":
    main();