import pygame
import random
import os.path
from settings import BLACK
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join("images", "jet1.png")).convert()
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect(left=80, top=200)
        self.radius = int(self.rect.height * 0.8 // 2)

    # move player within the screen boundary
    def update(self):
        speed = 10
        pressed_keys = pygame.key.get_pressed()
        screen_width, screen_height = pygame.display.get_window_size()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < screen_width - 5:
            self.rect.move_ip(speed, 0)
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -speed)
        if pressed_keys[K_DOWN] and self.rect.bottom < screen_height - 5:
            self.rect.move_ip(0, speed)

        pygame.display.update()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        num = random.randint(1, 8)
        screen_width, screen_height = pygame.display.get_window_size()
        self.surf = pygame.image.load(
            "images{}cloud{}.png".format(os.path.sep, str(num))
        ).convert()
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 100, screen_width + 200),
                random.randint(10, screen_height),
            )
        )
        self.speed = random.randint(8, 12)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

        pygame.display.update()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        m = random.randint(1, 8)
        screen_width, screen_height = pygame.display.get_window_size()
        self.surf = pygame.image.load(
            "images{}missile{}.png".format(os.path.sep, str(m))
        ).convert()
        self.surf.set_colorkey(BLACK)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 100, screen_width + 110),
                random.randint(10, screen_height - 10),
            )
        )
        self.radius = int(self.rect.height // 2)
        self.speed = random.randint(15, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

        pygame.display.update()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Explosion, self).__init__()
        self.anim_list = self.get_animation_frames()
        self.surf = self.anim_list[0]
        self.rect = self.surf.get_rect(center=pos)
        self.frame = 0
        self.frame_rate = 100
        self.last_update = pygame.time.get_ticks()

    def get_animation_frames(self):
        anim_list = []
        separator = os.path.sep
        for i in range(0, 9):
            name = f"images{separator}explosion{separator}regularExplosion0{i}.png"
            surface = pygame.transform.scale(pygame.image.load(name), (100, 100))
            anim_list.append(surface)
        return anim_list

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim_list):
                self.kill()
            else:
                self.surf = self.anim_list[self.frame]
                self.rect = self.surf.get_rect(center=self.rect.center)
