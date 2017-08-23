import pygame

class MyPlane(pygame.sprite.Sprite):
    def __init__(self , bg_size):
        pygame.sprite.Sprite.__init__(self);

        self.image1 = pygame.image.load("gameArts/hero_fly_1.png").convert_alpha();
        self.image2 = pygame.image.load("gameArts/hero_fly_2.png").convert_alpha();
        self.rect = self.image1.get_rect();
        self.width , self.height = bg_size[0] , bg_size[1];

        self.rect.left , self.rect.top = (self.width - self.rect.width) / 2 , self.height - self.rect.height - 60;
        self.speed = 5;

        self.active=True;
        self.mask = pygame.mask.from_surface(self.image1);
        self.destroy_images = [];
        self.destroy_images.extend([
            pygame.image.load("gameArts/hero_blowup_1.png").convert_alpha(),
            pygame.image.load("gameArts/hero_blowup_2.png").convert_alpha(),
            pygame.image.load("gameArts/hero_blowup_3.png").convert_alpha(),
            pygame.image.load("gameArts/hero_blowup_4.png").convert_alpha()

        ])

    def moveUp(self):
        if self.rect.top >= 0:
            self.rect.top -= self.speed;
        else:
            self.rect.top = 0;


    def moveDown(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed;
        else:
            self.rect.bottom = self.height - 60;


    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed;
        else:
            self.rect.left = 0;


    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed;
        else:
            self.rect.right = self.width; 
    def reset(self):
        self.active = True;
        # self.rect.left , self.rect.top = (self.width - self.rect.width) / 2 , self.height - self.rect.height - 60;
