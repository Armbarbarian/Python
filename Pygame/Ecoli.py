import pygame
import random
'''
import os
current_directory = os.getcwd()
print(current_directory)
directory_path = 'C:\\Users\\Danie\\Documents\\GitHub\\Python\\Pygame'
os.chdir(directory_path)
'''

player = 'C:\\Users\\Danie\\Documents\\GitHub\\Python\\Pygame\\player.png'
enemy = 'C:\\Users\\Danie\\Documents\\GitHub\\Python\\Pygame\\enemy.png'


import pygame
import random

# Initialize Pygame
pygame.init()

# Set the size of the game window
size = (800, 600)
screen = pygame.display.set_mode(size)

# Set the title of the game window
pygame.display.set_caption("E. coli Game")

# Load the player sprite
player_image = pygame.image.load(player)

# Create a rect for the player's position and size
player_rect = player_image.get_rect()

# Set the initial size of the player
player_size = 1

# Set the initial position of the player
player_rect.x = size[0] // 2
player_rect.y = size[1] // 2

# Load the enemy sprite
enemy_image = pygame.image.load(enemy)

# Create a list to store the enemies
enemies_list = []

# Spawn 10 enemies per level at random positions and varying sizes
for i in range(10):
    enemy_rect = enemy_image.get_rect()
    enemy_rect.x = random.randint(0, size[0] - enemy_rect.width)
    enemy_rect.y = random.randint(0, size[1] - enemy_rect.height)
    enemy_size = random.randint(10, 50)
    enemy = {"rect": enemy_rect, "size": enemy_size}
    enemies_list.append(enemy)

# Create a variable to store the player's score
score = 0

# Create a variable to store the game's running status
running = True

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player based on user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5

    # Check if the player is colliding with any enemies
    for enemy in enemies_list:
        if player_rect.colliderect(enemy["rect"]):
            # Increase the player's size
            player_size += enemy["size"]
            # Increase the player's score
            score += 1
            # Remove the enemy from the list
            enemies_list.remove(enemy)

    screen.fill((0, 0, 0))

    # Draw the player on the screen
    screen.blit(player_image, player_rect)

    # Draw the enemies on the screen
    for enemy in enemies_list:
        screen.blit(enemy_image, enemy["rect"])

    # Update the screen
    pygame.display.flip()

# Exit Pygame
pygame.quit()
