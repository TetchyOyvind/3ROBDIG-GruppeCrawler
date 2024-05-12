import pygame
import carMotion as robot

direction = 0
armed = False

print("Press the SPACE-key to engage")

pygame.init()
screen = pygame.display.set_mode((100, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("Up arrow pressed")
                direction = 1
            elif event.key == pygame.K_DOWN:
                print("Down arrow pressed")
                direction = -1
            elif event.key == pygame.K_LEFT:
                print("Left arrow pressed")
                direction = 2
            elif event.key == pygame.K_RIGHT:
                print("Right arrow pressed")
                direction = 3
            elif event.key == pygame.K_SPACE:
                armed = not armed
                print(armed)
                if not armed:
                    robot.stop()
            if armed:
                robot.direction(direction)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                print("Key released")
                direction = 0
                robot.direction(direction)
