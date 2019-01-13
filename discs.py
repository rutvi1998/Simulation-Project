import pygame
import random
import math
from pygame import mixer

pygame.font.init()
mixer.init()

background_color = (255, 255, 255)
(width, height) = (450, 450)
background = pygame.image.load("table.jpg")
boundary = pygame.mixer.Sound("boundary.wav")
collision = pygame.mixer.Sound("collide.wav")
myfont = pygame.font.SysFont('Comic Sans MS', 10)
drag = 0.99
friction = 0.75
density = random.randint(10, 15)
	
def addVectors((angle1, length1), (angle2, length2)) :
	x = math.sin(angle1) * length1 + math.sin(angle2) * length2 
	y = math.cos(angle1) * length1 + math.cos(angle2) * length2 


	angle = 0.5 * math.pi - math.atan2(y, x)
	length = math.hypot(x, y)
	
	return (angle, length)

def findDisc(discs, x, y) :
	for disc in discs :
		if math.hypot(disc.x - x, disc.y - y) <= disc.size :
			return disc

def collide(disc1, disc2) :
	dx = disc1.x - disc2.x
	dy = disc1.y - disc2.y

	distance = math.hypot(dx, dy)
	if distance < disc1.size + disc2.size :
		collision.play()
		angle = math.atan2(dy, dx) + 0.5 * math.pi
		total_mass = disc1.mass + disc2.mass
		
		(disc1.angle, disc1.speed) = addVectors((disc1.angle, disc1.speed * (disc1.mass - disc2.mass) / total_mass), (angle, 2 * disc2.speed * disc2.mass /  total_mass))
		(disc2.angle, disc2.speed) = addVectors((disc2.angle, disc2.speed * (disc2.mass - disc1.mass) / total_mass), (angle + math.pi, 2 * disc1.speed * disc1.mass /  total_mass))
		disc1.speed *= friction
		disc2.speed *= friction
		
		overlap = 0.5 * (disc1.size + disc2.size - distance + 1) 
		disc1.x += math.sin(angle) * overlap
		disc1.y -= math.cos(angle) * overlap
		disc2.x -= math.sin(angle) * overlap
		disc2.y += math.cos(angle) * overlap

class Disc :
	def __init__(self, num, (x, y), size, mass = 1) :
		self.num = str(num)		
		self.x = x
		self.y = y
		self.size = size
		self.colour = (0, 0, 0)
		self.thickness = 5
		self.speed = 0
		self.angle = 0
		self.mass = mass

	def display(self) :
		pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
		textsurface = myfont.render(self.num, True, (0, 0, 0))
		screen.blit(textsurface, (int(self.x), int(self.y) - 2 * self.size))	

	def move(self) :
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
		self.speed *= drag	

	def bounce(self) :
		if self.x > width - self.size :
			boundary.play() 
			self.x = 2 * (width - self.size) - self.x
			self.angle = -self.angle
			self.speed *= friction

		elif self.x < self.size :
			boundary.play() 
			self.x = 2 * self.size - self.x
			self.angle = -self.angle
			self.speed *= friction
			
		if self.y > height - self.size :
			boundary.play() 
			self.y = 2 * (height - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= friction

		elif self.y < self.size :
			boundary.play()  
			self.y = 2 * self.size - self.y
			self.angle = math.pi - self.angle
			self.speed *= friction
		
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Discs on Table')

number_of_discs = 5
my_discs = []

for n in range(number_of_discs) :
	size = random.randint(10, 20)
	x = random.randint(size, width-size)
	y = random.randint(size, height-size)

	disc = Disc(n + 1, (x, y), size, density * size ** 2)
	disc.speed = random.random()
	disc.angle = random.uniform(0, math.pi * 2)

	my_discs.append(disc)

selected_disc = None
running = True
while running :
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN :
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_disc = findDisc(my_discs, mouseX, mouseY)
		elif event.type == pygame.MOUSEBUTTONUP :
			selected_disc = None

	if selected_disc :
		(mouseX, mouseY) = pygame.mouse.get_pos()
		dx = mouseX - selected_disc.x
		dy = mouseY - selected_disc.y
		selected_disc.angle = 0.5 * math.pi + math.atan2(dy, dx)
		selected_disc.speed = math.hypot(dx, dy) * 0.1		

	screen.blit(background, (0, 0))

	for i, disc in enumerate(my_discs) :
		disc.move()
		disc.bounce()
		for disc2 in my_discs[i + 1 : ] :
			collide(disc, disc2)
		disc.display()

	pygame.display.flip()
