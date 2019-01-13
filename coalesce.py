import pygame
import random
import math
from pygame import mixer

pygame.font.init()
mixer.init()

background_color = (255, 255, 255)
(width, height) = (450, 450)
background = pygame.image.load("night.jpg")
coalescence = pygame.mixer.Sound("coalesce.wav")
myfont = pygame.font.SysFont('Comic Sans MS', 10)
friction = 0.75
density = random.randint(10, 15)

def addVectors((angle1, length1), (angle2, length2)) :
	x = math.sin(angle1) * length1 + math.sin(angle2) * length2 
	y = math.cos(angle1) * length1 + math.cos(angle2) * length2 


	angle = 0.5 * math.pi - math.atan2(y, x)
	length = math.hypot(x, y)
	
	return (angle, length)

def attract(particle1, particle2) :
	dx = particle1.x - particle2.x
	dy = particle1.y - particle2.y

	distance = math.hypot(dx, dy)
	
	angle = math.atan2(dy, dx)
	force = 0.2 * particle1.mass * particle2.mass / distance ** 2
		
	(particle1.angle, particle1.speed) = addVectors((particle1.angle, particle1.speed), (angle - 0.5 * math.pi, force/particle1.mass))
	(particle2.angle, particle2.speed) = addVectors((particle2.angle, particle2.speed), (angle - 0.5 * math.pi, force/particle2.mass))
		
def coalesce(particle1, particle2) :
	if math.hypot(particle1.x - particle2.x, particle1.y - particle2.y) < particle1.size + particle2.size :
		total_mass = particle1.mass + particle2.mass
		particle1.x = (particle1.x * particle1.mass + particle2.x * particle2.mass)/total_mass
		particle1.y = (particle1.y * particle1.mass + particle2.y * particle2.mass)/total_mass
		
		(particle1.angle, particle1.speed) = addVectors((particle1.angle, particle1.speed * particle1.mass / total_mass), (particle2.angle, particle2.speed * particle2.mass / total_mass)) 
		particle1.speed *= friction ** 2
		particle1.mass += particle2.mass
		particle1.size = math.sqrt(particle1.mass / density)
		my_particles.remove(particle2)
		pygame.mixer.Sound.play(coalescence)		

class Particle :
	def __init__(self, num, (x, y), size, mass = 1) :
		self.num = str(num)		
		self.x = x
		self.y = y
		self.size = size
		self.colour = (255, 255, 255)
		self.thickness = 0
		self.speed = 0
		self.angle = 0
		self.mass = mass

	def display(self) :
		pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.size), self.thickness)
		textsurface = myfont.render(self.num, True, (255, 255, 255))
		screen.blit(textsurface, (int(self.x), int(self.y) - 2 * self.size))	

	def move(self) :
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed

	def bounce(self) :
		if self.x > width - self.size :
			self.x = 2 * (width - self.size) - self.x
			self.angle = -self.angle
			self.speed *= friction
			
		elif self.x < self.size :
			self.x = 2 * self.size - self.x
			self.angle = -self.angle
			self.speed *= friction
			
		if self.y > height - self.size :	
			self.y = 2 * (height - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= friction
			
		elif self.y < self.size :			
			self.y = 2 * self.size - self.y
			self.angle = math.pi - self.angle
			self.speed *= friction 
		
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Coalescence of Particles')

number_of_particles = 5
my_particles = []

for n in range(number_of_particles) :
	size = random.randint(10, 20)
	x = random.randint(size, width-size)
	y = random.randint(size, height-size)

	particle = Particle(n + 1, (x, y), size, density * size ** 2)
	particle.speed = random.random()
	particle.angle = random.uniform(0, math.pi * 2)

	my_particles.append(particle)

running = True
while running :
	pygame.time.delay(25)
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			running = False

	screen.blit(background, (0, 0))

	for i, particle in enumerate(my_particles) :
		particle.move()
		particle.bounce()
		for particle2 in my_particles[i + 1 : ] :
			attract(particle, particle2)
			coalesce(particle, particle2)
		particle.display()

	pygame.display.flip()
