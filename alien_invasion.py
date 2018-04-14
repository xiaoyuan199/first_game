import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    #初始化游戏并创建一个屏幕、设置对象
    pygame.init() #初始化背景
    
    ai_settings = Settings()
    
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")

    #创建一个按钮
    play_button = Button(ai_settings,screen,"Play")

    #创建一艘飞船
    ship = Ship(screen,ai_settings)

    #创建一个用于存储子弹的编组
    bullets = Group()

    #创建一个存储外星人的编组
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,aliens,ship)

    #创建一个用于存储游戏统计信息的实例
    stats= GameStats(ai_settings)

    #创建储存游戏统计分数的实例
    sb = Scoreboard(ai_settings,screen,stats)

 

    #开始游戏主循环
    while True:
        #检测键盘事件
        gf.check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb)

        if stats.game_active:
            
            #检测飞船位置更新函数
            ship.update()

            #检测子弹更新函数
            gf.update_bullets(ai_settings,screen,ship,bullets,aliens,sb,stats)

            #更新外星人位置
            gf.update_aliens(ai_settings,aliens,ship,stats,screen,bullets)
      
        #更新屏幕函数
        gf.update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb)
                
      
        
run_game()                
