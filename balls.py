import pygame
import random
import math
from pygame import mixer

pygame.font.init()
mixer.init()

background_color = (255, 255, 255)
(width, height) = (450, 450)
background = pygame.image.load("field.jpg")
boundary = pygame.mixer.Sound("boundary.wav")
ground = pygame.mixer.Sound("ground.wav")
collision = pygame.mixer.Sound("collide.wav")
myfont = pygame.font.SysFont('Comic Sans MS', 10)
mass_of_air = 0.2
friction = 0.75
gravity = (math.pi, 0.002)
density = random.randint(10, 15)

def addVectors((angle1, length1), (angle2, length2)) :
	x = math.sin(angle1) * length1 + math.sin(angle2) * length2 
	y = math.cos(angle1) * length1 + math.cos(angle2) * length2 


	angle = 0.5 * math.pi - math.atan2(y, x)
	length = math.hypot(x, y)
	
	return (angle, length)


def findBall(balls, x, y) :
	for ball in balls :
		if math.hypot(ball.x - x, ball.y - y) <= ball.size :
			return ball

def collide(ball1, ball2) :
	dx = ball1.x - ball2.x
	dy = ball1.y - ball2.y

	distance = math.hypot(dx, dy)
	if distance < ball1.size + ball2.size :
		collision.play()
		angle = math.atan2(dy, dx) + 0.5 * math.pi
		total_mass = ball1.mass + ball2.mass
		
		(ball1.angle, ball1.speed) = addVectors((ball1.angle, ball1.speed * (ball1.mass - ball2.mass) / total_mass), (angle, 2 * ball2.speed * ball2.mass /  total_mass))
		(ball2.angle, ball2.speed) = addVectors((ball2.angle, ball2.speed * (ball2.mass - ball1.mass) / total_mass), (angle + math.pi, 2 * ball1.speed * ball1.mass /  total_mass))
		ball1.speed *= friction
		ball2.speed *= friction
		
		overlap = 0.5 * (ball1.size + ball2.size - distance + 1) 
		ball1.x += math.sin(angle) * overlap
		ball1.y -= math.cos(angle) * overlap
		ball2.x -= math.sin(angle) * overlap
		ball2.y += math.cos(angle) * overlap

class Ball :
	def __init__(self, num, (x, y), size, mass = 1) :
		self.num = str(num)		
		self.x = x
		self.y = y
		self.size = size
		self.colour = (255, 0, 0)
		self.thickness = 0
		self.speed = 0
		self.angle = 0
		self.mass = mass
		self.drag = (self.mass / (self.mass + mass_of_air)) ** self.size

	def display(self) :
		pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
		label = myfont.render(self.num, True, (255, 0, 0))
		screen.blit(label, (int(self.x), int(self.y) - 2 * self.size))	

	def move(self) :
		(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
		self.speed *= self.drag	

	def bounce(self) :
		ground.set_volume(self.speed*25)
		
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
			if int(self.speed * 100) != 0 :
				ground.play()			
			self.y = 2 * (height - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= friction
					
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Falling Balls')

number_of_balls = 5
my_balls = []

for n in range(number_of_balls) :
	size = random.randint(10, 20)
	x = random.randint(size, width-size)

	ball = Ball(n + 1, (x, 30), size, density * size ** 2)
	ball.speed = random.random()
	ball.angle = random.uniform(0, math.pi * 2)

	my_balls.append(ball)

selected_ball = None
running = True
while running :
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN :
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_ball = findBall(my_balls, mouseX, mouseY)
		elif event.type == pygame.MOUSEBUTTONUP :
			selected_ball = None

	if selected_ball :
		(mouseX, mouseY) = pygame.mouse.get_pos()
		dx = mouseX - selected_ball.x
		dy = mouseY - selected_ball.y
		selected_ball.angle = 0.5 * math.pi + math.atan2(dy, dx)
		selected_ball.speed = math.hypot(dx, dy) * 0.1		

	screen.blit(background, (0, 0))

	for i, ball in enumerate(my_balls) :
		ball.move()
		ball.bounce()
		for ball2 in my_balls[i + 1 : ] :
			collide(ball, ball2)
		ball.display()
	
	pygame.display.update()
