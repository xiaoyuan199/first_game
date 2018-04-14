import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb):
	#监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_RIGHT:
                           ship.moving_right = True
                     elif event.key == pygame.K_LEFT:
                              ship.moving_left = True
                     elif event.key == pygame.K_SPACE:
                             #创建一颗子弹，并将他加入到编组bullets中
                             new_bullet = Bullet(ai_settings,screen,ship)
                             bullets.add(new_bullet)
                     elif  event.key == pygame.K_q:
                             sys.exit()
                        
                             
            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                            ship.moving_right = False
                    elif event.key == pygame.K_LEFT:
                             ship.moving_left = False
                             
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb)



def  check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb):
        """在玩家点击Play按钮时开始游戏"""
        if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
                stats.game_active = True

                #重置游戏设置
                ai_settings.initialize_dynamic_settings()
                
                #设置光标不可见
                pygame.mouse.set_visible(False)
                
                #重置游戏统计信息
                stats.reset_stats()

                #重置记分牌图像
                sb.prep_score()
                sb.prep_level()

                #清空外星人列表和子弹列表
                aliens.empty()
                bullets.empty()

                #创建一群新的外星人
                create_fleet(ai_settings,screen,aliens,ship)
                ship.center_ship()

                                             
               

def update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb):
        """更新屏幕上的图像，并切换到新屏幕"""
          #m每次循环时都重绘屏幕
        screen.fill(ai_settings.bg_color)

        #在飞船和外星人后面重绘制所有子弹
        for bullet in bullets.sprites():
                bullet.draw_bullet()

        #绘制飞船
        ship.blitme()
        #绘制外星人
        aliens.draw(screen)

        #显示分数函数
        sb.show_score()

        #如果游戏处于非活跃状态，就绘制开始游戏按钮
        if not stats.game_active:
                play_button.draw_button()
        
        #让最近绘制的屏幕可见
        pygame.display.flip()


        
        
def update_bullets(ai_settings,screen,ship,bullets,aliens,sb,stats):
        
        #检测子弹位置更新函数
        bullets.update()

        #删除已经消失的子弹
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
                
       #调用响应外星人和子弹的碰撞函数
        check_bullet_alien_collisions(ai_settings,screen,ship,bullets,aliens,sb,stats)        
       

 

def check_bullet_alien_collisions(ai_settings,screen,ship,bullets,aliens,sb,stats):
        """响应外星人和子弹的碰撞函数"""
        #检测是否有子弹击中了外星人
        #如果是的话就删除子弹和外星人
        collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
        #检测外星人是否为空
        if len(aliens)==0:
                #删除所有剩余的子弹并新建一批外星人,提高一个等级
                bullets.empty()
                create_fleet(ai_settings,screen,aliens,ship)
                ai_settings.increase_speed()

                #提高等级
                stats.level +=1
                sb.prep_level()
        #有外星人被击落，开始计分
        if collisions:
                for aliens in collisions.values():
                        stats.score += ai_settings.alien_points
                        sb.prep_score()
                
                
            

def get_number_aliens_x(ai_settings,alien_width):
        """计算一行可容纳多少个外星人"""
        available_space_x = ai_settings.screen_width - 2 * alien_width
        #"""一行可以放的外星人数量"""
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
        """计算屏幕可容纳多少个外星人"""
        available_space_y = (ai_settings.screen_height - (3 * alien_height)-ship_height)
        number_rows = int (available_space_y / (2 * alien_height))
        return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
         #c创建一盒外星人并将其加入当前行
        alien = Alien(ai_settings,screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)
        

def create_fleet(ai_settings,screen,aliens,ship):
        """创建外星人群"""
        #创建一个外星人，
        #外星人间距为外星人宽度
        alien = Alien(ai_settings,screen)
        number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
        number_rows  = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

        #创建外星人群
        for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                        create_alien(ai_settings,screen,aliens,alien_number,row_number)
                
def update_aliens(ai_settings,aliens,ship,stats,screen,bullets):
        """检查是否有外星人位于屏幕边缘，并更新所有外星人的位置"""
        check_fleet_edges(ai_settings,aliens)
        aliens.update()
        
        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(ship,aliens):
                ship_hit(ai_settings,aliens,ship,stats,screen,bullets)
                
        #检测是否外星人到达屏幕底端
        check_aliens_bottom(ai_settings,aliens,ship,stats,screen,bullets)


def check_fleet_edges(ai_settings,aliens):
        """"有外星人到达时采取相应的措施"""
        for alien in aliens.sprites():
                if alien.check_edges():
                        change_fleet_direction(ai_settings,aliens)
                        break   


def change_fleet_direction(ai_settings,aliens):
        """有外星人到达边缘时采取相应的措施"""
        for alien in aliens.sprites():
                alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1        

def ship_hit(ai_settings,aliens,ship,stats,screen,bullets):
        """响应外星人撞到的飞船"""
        if stats.ships_left > 0:
                #将ships_left减一
                stats.ships_left -=1

                #清空外星人列表和子弹列表
                aliens.empty()
                bullets.empty()

                #c创建一群新的外星人，并将飞船放到屏幕底端中央
                create_fleet(ai_settings,screen,aliens,ship)
                ship.center_ship()

                #暂停
                sleep(1)
        else:
                stats.game_active = False
                pygame.mouse.set_visible(True)
                


def check_aliens_bottom(ai_settings,aliens,ship,stats,screen,bullets):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = screen.get_rect()

        for alien in aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                        #像处理外星人撞到飞船那样处理
                        ship_hit(ai_settings,aliens,ship,stats,screen,bullets)
                        break
        



        

                
