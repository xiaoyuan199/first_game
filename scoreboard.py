# -*- coding: utf-8 -*-
import pygame.font

class Scoreboard():
    """显示分数的信息类"""

    def __init__(self,ai_settings,screen,stats):
        """初始化得分需要涉及的属性"""

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.stats  = stats

        #显示得分信息时使用的文字的字体信息属性设置
        self.text_color= (30,30,30)
        self.font = pygame.font.SysFont('SimHei',40)

        self.font1 = pygame.font.SysFont('SimHei',20)

        #准备初始得分图像
        self.prep_score()

        #z准备初始化等级图像
        self.prep_level()

   

    def prep_score(self):
        """将得分转换为一副渲染的图像"""
        rounded_score = int(round(self.stats.score,-1))
        score_str = "{:,}".format(rounded_score)
        
        self.score_image = self.font.render(score_str,True,self.text_color,
                                            self.ai_settings.bg_color)
        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
        """将分数标签渲染为图像"""
        self.score_note_image = self.font1.render("分数:",True
                                                  ,self.text_color,self.ai_settings.bg_color)
        self.score_note_rect = self.score_note_image.get_rect()
        self.score_note_rect.right = self.score_rect.left-10
        self.score_note_rect.bottom = self.score_rect.bottom -2

    def show_score(self):
        """在屏幕上显示得分和等级"""
        self.screen.blit(self.score_note_image,self.score_note_rect)
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.level_note_image,self.level_note_rect)
        self.screen.blit(self.level_image,self.level_rect)
        
   
        

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level),True
                                            ,self.text_color,self.ai_settings.bg_color)

        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom +10

        """将等级便签渲染为图像"""
        self.level_note_image = self.font1.render(str("等级:"),True
                                                 ,self.text_color,self.ai_settings.bg_color)

        self.level_note_rect = self.level_note_image.get_rect()
        self.level_note_rect.right = self.level_rect.left-10
        self.level_note_rect.bottom = self.level_rect.bottom-2

      

    
        

        




        
        
