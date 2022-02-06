import pygame
import math
from random import randint
from pygame.math import Vector2
from sys import exit


WIDTH = 832
HEIGHT = 512


class PLAYER():
	def __init__(self):
		super().__init__()
		self.player_surf = pygame.image.load("graphics/spaceship.png").convert_alpha()
		self.player_surf = pygame.transform.scale(self.player_surf, (36,45))
		self.player_rect = self.player_surf.get_rect(center = (WIDTH/2,HEIGHT/2))
		self.speed = 2
		self.pos = pygame.math.Vector2(WIDTH/2,HEIGHT/2)

		self.rocket_sound = pygame.mixer.Sound('audio/rocket.wav')
		self.rocket_sound.set_volume(0.05)

		self.explosion = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion.set_volume(0.3)

	def move_mouse(self):
		self.mousex, self.mousey = pygame.mouse.get_pos()

	def move_to(self, x, y):
		self.player_rect.move(x*64, y*64)

	def rotate_and_move(self):
		self.relx, self.rely = self.mousex - self.player_rect.x, self.mousey - self.player_rect.y
		self.rotate_angle = (180 / math.pi) * -math.atan2(self.rely, self.relx) - 90
		self.rotated_player = pygame.transform.rotate(self.player_surf, self.rotate_angle)

		self.dx, self.dy = self.mousex - self.pos.x, self.mousey - self.pos.y
		self.dist = math.hypot(self.dx, self.dy)
		self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
		self.pos.x += self.dx * self.speed
		self.pos.y += self.dy * self.speed

		self.player_rect = self.rotated_player.get_rect(center = (self.pos.x,self.pos.y))
		

	def update(self):
		self.move_mouse()
		self.rotate_and_move()
		self.rocket_sound.play()
		screen.blit(self.rotated_player, (self.player_rect.x, self.player_rect.y))

class OBSTACLES():
	def __init__(self, level, place):
		super().__init__()
		self.place = place

		# 13 obstacles horizontally and 8 vertically
		# Template level v
		# (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		# (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2), (9,2), (10,2), (11,2), (12,2), (13,2),
		# (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (10,3), (11,3), (12,3), (13,3),
		# (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4), (11,4), (12,4), (13,4),
		# (1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5), (11,5), (12,5), (13,5),
		# (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6), (9,6), (10,6), (11,6), (12,6), (13,6),
		# (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7), (9,7), (10,7), (11,7), (12,7), (13,7),
		# (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)

		self.obstacle_surf = pygame.image.load("graphics/obstacle.png")
		self.obstacle_rect = self.obstacle_surf.get_rect(bottomright = (self.place[0] * 64, self.place[1] * 64))
		screen.blit(self.obstacle_surf, self.obstacle_rect)

class ORB:
	def __init__(self):
		self.orb_1 = pygame.image.load("floaty/floaty1.png")
		self.orb_2 = pygame.image.load("floaty/floaty2.png")
		self.orb_3 = pygame.image.load("floaty/floaty3.png")
		self.orb_4 = pygame.image.load("floaty/floaty4.png")

		self.swoosh = pygame.mixer.Sound('audio/win.wav')
		self.swoosh.set_volume(1)

		self.frames = [self.orb_1, self.orb_2, self.orb_3, self.orb_4]

		self.anim_index = 0
		self.image = self.frames[int(self.anim_index)]
		self.orb_rect = self.image.get_rect()

	def animation_state(self):
		self.anim_index += 0.1
		if self.anim_index >= len(self.frames): self.anim_index = 0
		self.image = self.frames[int(self.anim_index)]

class GAME:
	def __init__(self):
		self.game_state = 0

		self.deaths = -1

		self.player = PLAYER()
		self.init = False

		self.orb = ORB()

		self.obstacle_group = []

		self.title_surf = pixel_font.render("Rocket Mayhem", False, (201, 107, 24))

		self.congrats_surf = pixel_font.render("Congratulations!", False, (201,107,24))
		self.congrats_rect = self.congrats_surf.get_rect(midtop = (WIDTH/2, 30))

		self.instr = pixel_font2.render("Press SPACE to start", False, (201,107,24))
		self.intr_rect = self.instr.get_rect(center = (WIDTH/2, HEIGHT/2 + 30))

		self.mouse_surf = pygame.image.load("graphics/cursor.png")
		self.mouse_rect = self.mouse_surf.get_rect()

		self.bg1 = pygame.image.load("graphics/bg/bg1.png")
		self.bg2 = pygame.image.load("graphics/bg/bg2.png")
		self.bg3 = pygame.image.load("graphics/bg/bg3.png")
		self.bg4 = pygame.image.load("graphics/bg/bg4.png")

	def game_update(self):
		self.orb.animation_state()
		self.player.update()
		self.collisions()
		self.mouse()

	def mouse(self):
		self.mx, self.my = pygame.mouse.get_pos()
		pygame.mouse.set_visible(False)
		self.mouse_rect.x, self.mouse_rect.y = self.mx, self.my
		screen.blit(self.mouse_surf, self.mouse_rect)


	def collisions(self):
		for obstacles in range(len(self.obstacle_group)):
			if self.player.player_rect.colliderect(self.obstacle_group[obstacles].obstacle_rect) or self.player.player_rect.colliderect(self.mouse_rect):
				self.player.rocket_sound.stop()
				self.player.explosion.play()
				self.game_state = 0
		if self.player.player_rect.colliderect(self.orb.orb_rect):
			self.player.rocket_sound.stop()
			self.orb.swoosh.play()
			self.init = False
			self.game_state += 1


	def statemanager(self):
		if self.game_state == 0:
			self.title()
		elif self.game_state == 1:
			self.level1()
			self.game_update()
		elif self.game_state == 2:
			self.level2()
			self.game_update()
		elif self.game_state == 3:
			self.level3()
			self.game_update()
		elif self.game_state == 4:
			self.level4()
			self.game_update()
		elif self.game_state == 5:
			self.level5()
			self.game_update()
		elif self.game_state == 6:
			self.level6()
			self.game_update()
		elif self.game_state == 7:
			self.level7()
			self.game_update()
		elif self.game_state == 8:
			self.level8()
			self.game_update()
		elif self.game_state == 9:
			self.level9()
			self.game_update()
		elif self.game_state == 10:
			self.level10()
			self.game_update()
		elif self.game_state == 11:
			self.end_game()
			

	def title(self):
		screen.blit(self.bg1, (0,0))
		screen.blit(self.title_surf, (20,20))
		screen.blit(self.instr, self.intr_rect)
		self.mouse()
		self.init = False

	def level1(self):
		screen.blit(self.bg1, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 11*64, 1*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 7*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2), (9,2), (10,2),                 (13,2),
		(1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (10,3),                 (13,3),
		(1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4),                 (13,4),
		(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5),                 (13,5),
		(1,6),                                                                                 (13,6),
		(1,7),                                                                                 (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level2(self):
		screen.blit(self.bg1, (0,0))
		self.obstacle_group.clear()
		self.orb.orb_rect.x, self.orb.orb_rect.y = 2*64, 1*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 7*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),                                                                                 (13,2),
		(1,3),                                                                                 (13,3),
		(1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4),                 (13,4),
		(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5),                 (13,5),
		(1,6),                                                                                 (13,6),
		(1,7),                                                                                 (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level3(self):
		screen.blit(self.bg2, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 7*64, 2*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 12*64 - 32, 2*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),                                                         (10,2),                 (13,2),
		(1,3),                                                         (10,3),                 (13,3),
		(1,4),               (4,4), (5,4), (6,4),                      (10,4),                 (13,4),
		(1,5),               (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5),                 (13,5),
		(1,6),                                                                                 (13,6),
		(1,7),                                                                                 (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level4(self):
		screen.blit(self.bg2, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 2*64, 6*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 2*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),                                                                                 (13,2),
		(1,3),                                    (7,3),                                       (13,3),
		(1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4),                 (13,4),
		(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5),                 (13,5),
		(1,6),                                                                                 (13,6),
		(1,7),                                                                                 (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level5(self):
		screen.blit(self.bg2, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 9*64, 4*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 2*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),               (4,2), (5,2),                                             (12,2), (13,2),
		(1,3),               (4,3), (5,3),                                             (12,3), (13,3),
		(1,4),               (4,4), (5,4),               (8,4),                        (12,4), (13,4),
		(1,5),               (4,5), (5,5),               (8,5),                        (12,5), (13,5),
		(1,6),                                           (8,6),                        (12,6), (13,6),
		(1,7),                                           (8,7), (9,7), (10,7), (11,7), (12,7), (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level6(self):
		screen.blit(self.bg2, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 7*64, 6*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 7*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2), (2,2), (3,2), (4,2),                                                            (13,2),
		(1,3), (2,3), (3,3),                                                                   (13,3),
		(1,4), (2,4),                             (7,4), (8,4), (9,4),                         (13,4),
		(1,5),                             (6,5), (7,5), (8,5),                                (13,5),
		(1,6),                      (5,6), (6,6), (7,6),                               (12,6), (13,6),
		(1,7),                      (5,7), (6,7), (7,7),                       (11,7), (12,7), (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level7(self):
		screen.blit(self.bg3, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 1*64, 1*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 6*64 - 32

		self.player.speed = 3

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),               (4,2), (5,2), (6,2), (7,2), (8,2), (9,2), (10,2), (11,2), (12,2), (13,2),
		(1,3),                                                                         (12,3), (13,3),
		(1,4),                                                                                 (13,4),
		(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5),                         (13,5),
		(1,6),                                                                                 (13,6),
		(1,7),                                                                                 (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level8(self):
		screen.blit(self.bg3, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 1*64, 3*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 3*64 - 32, 7*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),                                                                                 (13,2),
		(1,3),                                                                                 (13,3),
		(1,4),                      (5,4), (6,4),               (9,4),                         (13,4),
		(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5),                 (13,5),
		(1,6),                                                                                 (13,6),
		(1,7),                                    (7,7),                                       (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level9(self):
		screen.blit(self.bg4, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 11*64, 6*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 3*64 - 32, 7*64 - 32

		self.player.speed = 2

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),                                                                                 (13,2),
		(1,3),                                    (7,3),                                       (13,3),
		(1,4),               (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4),                 (13,4),
		(1,5),               (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5),                 (13,5),
		(1,6),               (4,6), (5,6), (6,6), (7,6), (8,6), (9,6), (10,6),                 (13,6),
		(1,7),               (4,7), (5,7), (6,7), (7,7), (8,7), (9,7), (10,7),                 (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def level10(self):
		screen.blit(self.bg4, (0,0))
		self.obstacle_group.clear()

		self.orb.orb_rect.x, self.orb.orb_rect.y = 1*64, 5*64
		screen.blit(self.orb.image, self.orb.orb_rect)
		if self.init == False:
			self.player.pos.x, self.player.pos.y = 2*64 - 32, 2*64 - 32

		self.player.speed = 3.5

		self.obstacle_list =  [
		(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
		(1,2),                                                                                 (13,2),
		(1,3),                                                                                 (13,3),
		(1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4),                 (13,4),
		(1,5),                                                                                 (13,5),
		(1,6),                                                                         (12,6), (13,6),
		(1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7), (9,7),                 (12,7), (13,7),
		(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8)]
		self.init = True
		for blocks in range(len(self.obstacle_list)):
			self.obstacle_group.append(OBSTACLES(1,self.obstacle_list[blocks]))

		self.level_surf = pixel_font.render(str(self.game_state), False, (255, 255, 255))
		self.level_rect = self.level_surf.get_rect(bottomright = (WIDTH - 10,HEIGHT))

		self.deaths_text_surf = pixel_font2.render(f'Deaths: {self.deaths}', False, (255,255,255))
		self.deaths_text_rect = self.deaths_text_surf.get_rect(topleft = (10,10))

		screen.blit(self.deaths_text_surf, self.deaths_text_rect)
		screen.blit(self.level_surf, self.level_rect)

	def end_game(self):
		screen.blit(self.bg2, (0,0))
		screen.blit(self.congrats_surf, self.congrats_rect)

		self.info = pixel_font2.render(f"Deaths: {self.deaths}", False, (201,107,24))
		self.info_rect = self.info.get_rect(center = (WIDTH/2, HEIGHT/2 + 10))
		screen.blit(self.info, self.info_rect)

		self.mouse()






# General
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Rocket Mayhem")

bg_music = pygame.mixer.Sound('audio/music.mp3')
bg_music.set_volume(0.3)
bg_music.play(loops = -1)

icon_surf = pygame.image.load("graphics/icon.png")
pygame.display.set_icon(icon_surf)

clock = pygame.time.Clock()

pixel_font = pygame.font.Font("Pixeltype.ttf", 120)
pixel_font2 = pygame.font.Font("Pixeltype.ttf", 50)

# Specific
game = GAME()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if game.game_state == 0:
						game.deaths += 1
						game.game_state = 1
					elif game.game_state == 11:
						game.deaths = -1
						game.game_state = 0




	game.statemanager()
	pygame.display.update()
	clock.tick(60)






