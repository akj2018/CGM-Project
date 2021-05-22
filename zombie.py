############################################################################################
###                                                                                      ###
###   PyGame with a SnowPea shoot bullet for defensing the zombie army coming            ###
###                                                                                      ###
###   Author: Junjie Shi                                                                 ###
###   Email : handsomestone@gmail.com                                                    ### 
###                                                                                      ### 
###   Do Enjoy the game!                                                                 ###
###   You need to have Python and PyGame installed to run it.                            ###
###   Run it by typing "python zombie.py" in the terminal                                ###
###                                                                                      ### 
###   This program is free software: you can redistribute it and/or modify               ### 
###   it under the terms of the GNU General Public License as published by               ### 
###   the Free Software Foundation, either version 3 of the License, or                  ### 
###   (at your option) any later version.                                                ### 
###                                                                                      ### 
###   This program is distributed in the hope that it will be useful,                    ### 
###   but WITHOUT ANY WARRANTY; without even the implied warranty of                     ### 
###   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                      ### 
###   GNU General Public License for more details.                                       ### 
###                                                                                      ### 
###   You should have received a copy of the GNU General Public License                  ### 
###   along with this program.  If not, see <http://www.gnu.org/licenses/>.              ###                                                                              ###
###                                                                                      ###
############################################################################################

import pygame, random, sys, time
from pygame.locals import *

#set up some variables
WINDOWWIDTH = 1024
WINDOWHEIGHT = 600
FPS = 60

MAXGOTTENPASS = 3
ZOMBIESIZE = 110 #includes newKindZombies
ADDNEWZOMBIERATE = 60
ADDNEWKINDZOMBIE = ADDNEWZOMBIERATE

NORMALZOMBIESPEED = 2
NEWKINDZOMBIESPEED = NORMALZOMBIESPEED / 2

PLAYERMOVERATE = 15
BULLETSPEED = 10
ADDNEWBULLETRATE = 15
MAXBULLETSPEED = 20
MINNEWBULLETRATE = 8

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

angle = 0

def terminate():
	pygame.quit()
	sys.exit()

def waitForPlayerToPressKey():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: # pressing escape quits
					terminate()
				if event.key == K_RETURN:
					return

def playerHasHitZombie(playerRect, zombies):
	for z in zombies:
		if playerRect.colliderect(z['rect']):
			return True
	return False

def bulletHasHitZombie(bullets, z):
	for b in bullets:
		if b['rect'].colliderect(z['rect']):
			bullets.remove(b)
			return True
	return False

def bulletHasHitCrawler(bullets, c):
	for b in bullets:
		if b['rect'].colliderect(c['rect']):
			bullets.remove(b)
			return True
	return False

def drawText(text, font, surface, x, y):
	textobj = font.render(text, 1, TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

def rotate(surface, rect, angle):
	rotated_surface = pygame.transform.rotozoom(surface,angle,1)
	rotated_rect = rotated_surface.get_rect(center = rect.center)
	return rotated_surface,rotated_rect

def plant_touches_sun(playerRect, sunRect):
	if playerRect.colliderect(sunRect):
		return True
	else :
		return False

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#, pygame.FULLSCREEN)
pygame.display.set_caption('Zombie Defence')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('grasswalk.mp3')

# set up images
playerImage = pygame.image.load('SnowPea.gif')
playerRect = playerImage.get_rect()

bulletImage = pygame.image.load('SnowPeashooterBullet.gif')
bulletRect = bulletImage.get_rect()

zombieImage = pygame.image.load('Normal.gif')

newKindZombieImage = pygame.image.load('ConeheadZombieAttack.png')

#sunImage = pygame.image.load("Sun.png")
#sunImage = pygame.transform.scale(sunImage,(75,75))
#sunRect = sunImage.get_rect(center=(600,300))


backgroundImage = pygame.image.load('background_2.jpg')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH + 100, WINDOWHEIGHT))


# show the "Start" screen
windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
drawText('Plants Vs Zombies', font, windowSurface, (WINDOWWIDTH / 4) + 80, (WINDOWHEIGHT / 4))
drawText('Press Enter to start', font, windowSurface, (WINDOWWIDTH / 4) + 80, (WINDOWHEIGHT / 3) + 50)
drawText("Don't let 3 zombies touch the left side!", font, windowSurface, (WINDOWWIDTH / 4) - 60, (WINDOWHEIGHT / 3) + 120)
drawText("Don't hit the zombie!", font, windowSurface, (WINDOWWIDTH / 4) + 80, (WINDOWHEIGHT / 3) + 160)
pygame.display.update()
waitForPlayerToPressKey()

x_coordinate = 0

while True:
	# set up the start of the game

	zombies = []
	newKindZombies = []
	bullets = []

	zombiesGottenPast = 0
	score = 0
	Level = 1
	Level_inc=True
	Level_change=20

	playerRect.topleft = (50, WINDOWHEIGHT /2)
	moveLeft = moveRight = False
	moveUp=moveDown = False
	shoot = False

	zombieAddCounter = 0
	newKindZombieAddCounter = 0
	bulletAddCounter = 40

	newSunTime=600
	newSunRange=[600,1200]
	sunTime=0
	sunHorizontalRange=[60,WINDOWWIDTH-80]
	sunVerticalRange=[60,WINDOWHEIGHT-40]
	sunDrop=0
	sunDropSpeed=5
	sunAlpha=30
	sun=0
	sunappear=0
	sunLimit=600
	ADDNEWBULLETRATE=15
	BULLETSPEED=10

	pygame.mixer.music.play(-1, 0.0)



	while True: # the game loop runs while the game part is playing
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()

			if event.type == KEYDOWN:
				if event.key == K_UP or event.key == ord('w'):
					moveDown = False
					moveUp = True
				if event.key == K_DOWN or event.key == ord('s'):
					moveUp = False
					moveDown = True
				if event.key == K_RIGHT or event.key == ord('d'):
					moveRight = True
					moveLeft = False
				if event.key == K_LEFT or event.key == ord('a'):
					moveLeft = True
					moveRight = False

				if event.key == K_SPACE:
					shoot = True

			if event.type == KEYUP:
				if event.key == K_ESCAPE:
						terminate()

				if event.key == K_UP or event.key == ord('w'):
					moveUp = False
				if event.key == K_DOWN or event.key == ord('s'):
					moveDown = False
				if event.key == K_RIGHT or event.key == ord('d'):
					moveRight = False
				if event.key == K_LEFT or event.key == ord('a'):
					moveLeft = False

				if event.key == K_SPACE:
					shoot = False

		# Add new zombies at the top of the screen, if needed.
		zombieAddCounter += 1
		if zombieAddCounter == ADDNEWKINDZOMBIE:
			zombieAddCounter = 0
			zombieSize = ZOMBIESIZE       
			newZombie = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-zombieSize-10), zombieSize, zombieSize),
						'surface':pygame.transform.scale(zombieImage, (zombieSize, zombieSize)),
						}

			zombies.append(newZombie)

		# Add new newKindZombies at the top of the screen, if needed.
		newKindZombieAddCounter += 1
		if newKindZombieAddCounter == ADDNEWZOMBIERATE:
			newKindZombieAddCounter = 0
			newKindZombiesize = ZOMBIESIZE
			newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindZombiesize-10), newKindZombiesize, newKindZombiesize),
						'surface':pygame.transform.scale(newKindZombieImage, (70, 140)),
						}
			newKindZombies.append(newCrawler)

		# add new bullet
		bulletAddCounter += 1
		if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
			bulletAddCounter = 0
			newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
						 'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
						}
			bullets.append(newBullet)

		# add new sun
		sunTime+=1
		if sunTime == newSunTime:
			if sun!=0:
				sunTime=0
			else:
				sunHorizontal=random.randint(sunHorizontalRange[0],sunHorizontalRange[1])
				sunVertical=random.randint(sunVerticalRange[0],sunVerticalRange[1])
				sunImage = pygame.image.load("Sun.png")
				sunImage = pygame.transform.scale(sunImage,(75,75))
				sunRect = sunImage.get_rect(center=(sunHorizontal,sunDrop))
				sun=1
				newSunTime=random.randint(newSunRange[0],newSunRange[1])
				sunAlphaSpeed=(255-30)//(sunVertical//sunDropSpeed)
				#print(sunRect)

		# Move the player around.
		if moveUp and playerRect.top > 30:
			playerRect.move_ip(0,-1 * PLAYERMOVERATE)
		if moveDown and playerRect.bottom < WINDOWHEIGHT-10:
			playerRect.move_ip(0,PLAYERMOVERATE)
		if moveRight and playerRect.right < WINDOWWIDTH - 10:
			playerRect.move_ip(PLAYERMOVERATE,0)
		if moveLeft and playerRect.left > 30:
			playerRect.move_ip(-1*PLAYERMOVERATE,0)

		# Move the zombies down.
		for z in zombies:
			z['rect'].move_ip(-1*NORMALZOMBIESPEED, 0)

		# Move the newKindZombies down.
		for c in newKindZombies:
			c['rect'].move_ip(-1*NEWKINDZOMBIESPEED,0)

		# move the bullet
		for b in bullets:
			b['rect'].move_ip(1 * BULLETSPEED, 0)

		# Delete zombies that have fallen past the bottom.
		for z in zombies[:]:
			if z['rect'].left < 0:
				zombies.remove(z)
				zombiesGottenPast += 1

		# Delete newKindZombies that have fallen past the bottom.
		for c in newKindZombies[:]:
			if c['rect'].left <0:
				newKindZombies.remove(c)
				zombiesGottenPast += 1
		
		for b in bullets[:]:
			if b['rect'].right>WINDOWWIDTH:
				bullets.remove(b)
				
		# check if the bullet has hit the zombie
		for z in zombies:
			if bulletHasHitZombie(bullets, z):
				score += 1
				zombies.remove(z)
	
		for c in newKindZombies:
			if bulletHasHitCrawler(bullets, c):
				score += 1
				newKindZombies.remove(c)      

		# check for collission of plant and sun
		if sun==2 and plant_touches_sun(playerRect,sunRect):
			if ADDNEWBULLETRATE>MINNEWBULLETRATE:
				ADDNEWBULLETRATE-=2
			if BULLETSPEED<MAXBULLETSPEED:
				BULLETSPEED+=4
			sun=0
			sunTime=0
			sunAlpha=30
			score+=10
			sunDrop=0
			sunappear=0
			#print('sun')

		if score!=0 and score%Level_change==0 and Level_inc:
			Level+=1
			Level_inc=False 
			if ADDNEWZOMBIERATE>15:
				ADDNEWZOMBIERATE-=2
			if ADDNEWKINDZOMBIE>15:
				ADDNEWKINDZOMBIE-=2
		elif score%Level_change!=0 and not Level_inc:
			Level_inc=True

		
		
		rel_x = x_coordinate % rescaledBackground.get_rect().width
		# Draw the game world on the window.
		windowSurface.blit(rescaledBackground, (rel_x - rescaledBackground.get_rect().width, 0))
		if (rel_x < rescaledBackground.get_rect().width) :
			 windowSurface.blit(rescaledBackground, (rel_x, 0))
		x_coordinate = x_coordinate - 1

		# Draw the player's rectangle, rails
		windowSurface.blit(playerImage, playerRect)
		
		# drop sun
		if sun==1:
			if sunDrop<sunVertical:
				if sunDrop+sunDropSpeed<sunVertical:
					sunDrop+=sunDropSpeed
				else:
					sunDrop=sunVertical
			else:
				sun=2
			if sunAlpha+sunAlphaSpeed<255:
				sunAlpha+=sunAlphaSpeed
			else:
				sunAlpha=255
			sunImage.set_alpha(sunAlpha)
			sunRect=sunImage.get_rect(center=(sunHorizontal,sunDrop))
			windowSurface.blit(sunImage,sunRect)

		# draw sun
		if sun==2:
			sunappear+=1
			if sunappear>=sunLimit:
				sun=0
				sunTime=0
				sunAlpha=30
				sunDrop=0
				sunappear=0
			angle = angle + 1
			sunImage.set_alpha(255)
			sun_rotated, sun_rotated_rect = rotate(sunImage,sunRect,angle)
			windowSurface.blit(sun_rotated,sun_rotated_rect)

		


		# Draw each baddie
		for z in zombies:
			windowSurface.blit(z['surface'], z['rect'])

		for c in newKindZombies:
			windowSurface.blit(c['surface'], c['rect'])

		# draw each bullet
		for b in bullets:
			windowSurface.blit(b['surface'], b['rect'])

		
		# Draw the score and how many zombies got past
		drawText('zombies gotten past: %s' % (zombiesGottenPast), font, windowSurface, 10, 20)
		drawText('score: %s' % (score), font, windowSurface, 10, 50)
		drawText('Level: %s' % (Level),font,windowSurface,800,20)

		# update the display
		pygame.display.update()
			
		# Check if any of the zombies has hit the player.
		if playerHasHitZombie(playerRect, zombies):
			break
		if playerHasHitZombie(playerRect, newKindZombies):
			break
		
		# check if score is over MAXGOTTENPASS which means game over
		if zombiesGottenPast >= MAXGOTTENPASS:
			break

		mainClock.tick(FPS)

	# Stop the game and show the "Game Over" screen.
	pygame.mixer.music.stop()
	gameOverSound.play()
	time.sleep(1)
	if zombiesGottenPast >= MAXGOTTENPASS:
		windowSurface.blit(rescaledBackground, (0, 0))
		windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
		drawText('score: %s' % (score), font, windowSurface, 10, 30)
		drawText('Level: %s' % (Level), font, windowSurface, 800, 30)
		drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3) + 40, (WINDOWHEIGHT / 3))
		drawText('YOUR COUNTRY HAS BEEN DESTROIED', font, windowSurface, (WINDOWWIDTH / 4)- 80, (WINDOWHEIGHT / 3) + 100)
		drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
		pygame.display.update()
		waitForPlayerToPressKey()
	if playerHasHitZombie(playerRect, zombies):
		windowSurface.blit(rescaledBackground, (0, 0))
		windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
		drawText('score: %s' % (score), font, windowSurface, 10, 30)
		drawText('Level: %s' % (Level), font, windowSurface, 800, 30)
		drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3)+40, (WINDOWHEIGHT / 3))
		drawText('YOU HAVE BEEN KISSED BY THE ZOMMBIE', font, windowSurface, (WINDOWWIDTH / 4) - 110, (WINDOWHEIGHT / 3) +100)
		drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 90, (WINDOWHEIGHT / 3) + 150)
		pygame.display.update()
		waitForPlayerToPressKey()
	if playerHasHitZombie(playerRect, newKindZombies):
		windowSurface.blit(rescaledBackground, (0, 0))
		windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
		drawText('score: %s' % (score), font, windowSurface, 10, 30)
		drawText('Level: %s' % (Level), font, windowSurface, 800, 30)
		drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3)+40, (WINDOWHEIGHT / 3))
		drawText('YOU HAVE BEEN KISSED BY THE ZOMMBIE', font, windowSurface, (WINDOWWIDTH / 4) - 110, (WINDOWHEIGHT / 3) +100)
		drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 90, (WINDOWHEIGHT / 3) + 150)
		pygame.display.update()
		waitForPlayerToPressKey()
	gameOverSound.stop()
