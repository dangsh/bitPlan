import pygame
import traceback
import sys
from pygame.locals import *
import myPlane
import enemy

pygame.init();

bg_size = width , height =320 ,568 ;
screen=pygame.display.set_mode(bg_size);
pygame.display.set_caption("微信打飞机");
background = pygame.image.load("gameArts/background_2.png").convert_alpha();

def main():
    clock = pygame.time.Clock();
    screen.blit(background,(0,0));




if __name__ =="__main__":
    main();