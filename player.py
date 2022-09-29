from pygame import *
import pyganim
import blocks
import monsters
from settings import MOVE_SPEED, MOVE_EXTRA_SPEED, WIDTH, HEIGHT, COLOR, JUMP_POWER, JUMP_EXTRA_POWER, GRAVITY, \
    ANIMATION_DELAY, ANIMATION_SUPER_SPEED_DELAY, ANIMATION_RIGHT, ANIMATION_LEFT, ANIMATION_JUMP_LEFT, \
    ANIMATION_JUMP_RIGHT, ANIMATION_JUMP, ANIMATION_STAY, SCREEN_START


class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x_val = 0
        self.y_val = 0
        self.start_x = x
        self.start_y = y
        self.on_ground = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))

        bolt_anim = [(anim, ANIMATION_DELAY) for anim in ANIMATION_LEFT]
        bolt_anim_super_speed = [(anim, ANIMATION_SUPER_SPEED_DELAY) for anim in ANIMATION_LEFT]
        """for anim in ANIMATION_LEFT:
            bolt_anim.append((anim, ANIMATION_DELAY))
            bolt_anim_super_speed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        """
        self.bolt_anim_left = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_left.play()
        self.bolt_anim_left_super_speed = pyganim.PygAnimation(bolt_anim_super_speed)
        self.bolt_anim_left_super_speed.play()

        """bolt_anim = [(anim, ANIMATION_DELAY) for anim in ANIMATION_RIGHT]
        bolt_anim_super_speed = [(anim, ANIMATION_SUPER_SPEED_DELAY) for anim in ANIMATION_RIGHT]
        for anim in ANIMATION_RIGHT:
            bolt_anim.append((anim, ANIMATION_DELAY))
            bolt_anim_super_speed.append((anim, ANIMATION_SUPER_SPEED_DELAY))"""
        self.bolt_anim_right = pyganim.PygAnimation([(anim, ANIMATION_DELAY) for anim in ANIMATION_RIGHT])
        self.bolt_anim_right.play()
        self.bolt_anim_right_super_speed = pyganim.PygAnimation([(anim, ANIMATION_SUPER_SPEED_DELAY) for anim in
                                                                 ANIMATION_RIGHT])
        self.bolt_anim_right_super_speed.play()

        self.bolt_anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.bolt_anim_stay.play()

        self.bolt_anim_stay.blit(self.image, SCREEN_START)

        self.bolt_anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.bolt_anim_jump_left.play()

        self.bolt_anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.bolt_anim_jump_right.play()

        self.bolt_anim_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.bolt_anim_jump.play()
        self.winner = False

    def update(self, left, right, up, running, platforms):

        if up:
            if self.on_ground:
                self.y_val = - JUMP_POWER
                if running and (left or right):
                    self.y_val -= JUMP_EXTRA_POWER
                self.image.fill(Color(COLOR))
                self.bolt_anim_jump.blit(self.image, SCREEN_START)

        if left:
            self.x_val = - MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.x_val -= MOVE_EXTRA_SPEED
                if not up:
                    self.bolt_anim_left_super_speed.blit(self.image, SCREEN_START)
            else:
                if not up:
                    self.bolt_anim_left.blit(self.image, SCREEN_START)
            if up:
                self.bolt_anim_jump_left.blit(self.image, SCREEN_START)

        if right:
            self.x_val = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.x_val += MOVE_EXTRA_SPEED
                if not up:
                    self.bolt_anim_right_super_speed.blit(self.image, SCREEN_START)
            else:
                if not up:
                    self.bolt_anim_right.blit(self.image, SCREEN_START)
            if up:
                self.bolt_anim_jump_right.blit(self.image, SCREEN_START)

        if not (left or right):
            self.x_val = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.bolt_anim_stay.blit(self.image, SCREEN_START)

        if not self.on_ground:
            self.y_val += GRAVITY

        self.on_ground = False
        self.rect.y += self.y_val
        self.collide(0, self.y_val, platforms)
        self.rect.x += self.x_val
        self.collide(self.x_val, 0, platforms)

    def collide(self, x_val, y_val, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if isinstance(platform, blocks.BlockDie) or isinstance(platform, monsters.Monster):
                    self.die()
                elif isinstance(platform, blocks.BlockTeleport):
                    self.teleporting(platform.go_x, platform.go_y)
                elif isinstance(platform, blocks.Princess):
                    self.winner = True
                else:
                    if x_val > 0:
                        self.rect.right = platform.rect.left
                    if x_val < 0:
                        self.rect.left = platform.rect.right
                    if y_val > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_ground = True
                        self.y_val = 0
                    if y_val < 0:
                        self.rect.top = platform.rect.bottom
                        self.y_val = 0

    def teleporting(self, go_x, go_y):
        self.rect.x = go_x
        self.rect.y = go_y

    def die(self):
        time.wait(500)
        self.teleporting(self.start_x, self.start_y)
