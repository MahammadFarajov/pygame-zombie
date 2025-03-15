import pygame
import math
import time
import random

pygame.init()

screen_width = 800 
screen_height = 600

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))

font_style = pygame.font.SysFont(None, 50)

def message(msg, color, coords):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, coords)

def gameloop():
    game_over = False
    game_close = False

    x1_change = 0
    y1_change = 0


    zombie_spawnpoint = random.choice([[0, round(random.randrange(0, screen_height), 10)],  [screen_width, round(random.randrange(0, screen_height), 10)], [round(random.randrange(0, screen_width), 10), 0],  [round(random.randrange(0, screen_width), 10), screen_height]])

    zombie = pygame.Rect((zombie_spawnpoint[0], zombie_spawnpoint[1], 50, 50))


    player = pygame.Rect((screen_width / 2, screen_height / 2, 50, 50))
    sword_base = pygame.image.load('./sword.png').convert_alpha()
    sword_scale = pygame.transform.scale(sword_base, (170, 50))
    sword_scale_ability = pygame.transform.scale(sword_base, (250, 50))

    SPAWN_ENEMY = pygame.USEREVENT + 1
    while not game_over:
        
        while game_close:
            screen.fill('black')
            message('Game Over', 'red', [screen_width / 2.5, screen_height / 2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameloop()
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -10
                    y1_change = 0
                if event.key == pygame.K_d:
                    x1_change = 10
                    y1_change = 0
                if event.key == pygame.K_w:
                    y1_change = -10
                    x1_change = 0
                if event.key == pygame.K_s:
                    y1_change = 10          
                    x1_change = 0      
                if event.key == pygame.K_z:
                    pygame.time.set_timer(sword_scale_ability, 7000)
            if event.type == pygame.KEYUP:
                x1_change = 0
                y1_change = 0
            if event.type == SPAWN_ENEMY:
                zombie_spawnpoint = random.choice([[0, round(random.randrange(0, screen_height), 10)],  [screen_width, round(random.randrange(0, screen_height), 10)], [round(random.randrange(0, screen_width), 10), 0],  [round(random.randrange(0, screen_width), 10), screen_height]])
                zombie = pygame.Rect((zombie_spawnpoint[0], zombie_spawnpoint[1], 50, 50))
                pygame.draw.rect(screen, 'green', zombie)
        player.x += x1_change
        player.y += y1_change

        sword_x = player.x + 40
        sword_y = player.y + 25

        screen.fill('white')

        if zombie.x > player.x:
            zombie.x -= 5
        if zombie.x < player.x:
            zombie.x += 5
        if zombie.y > player.y:
            zombie.y -= 5
        if zombie.y < player.y:
            zombie.y += 5

        if player.x < 0:
            player.x = 0
        if player.x >= screen_width - 50:
            player.x = screen_width - 50
        if player.y < 0:
            player.y = 0
        if player.y >= screen_height - 50:
            player.y = screen_height - 50



        pygame.draw.rect(screen, 'black', player)
        pygame.draw.rect(screen, 'green', zombie)

        pos = pygame.mouse.get_pos()

        x_dist = (pos[0] - sword_x)
        y_dist = (pos[1] - sword_y)

        sword_angle = math.degrees(math.atan2(x_dist, y_dist))

        sword = pygame.transform.rotate(sword_scale, sword_angle - 90)
        sword_rect = sword.get_rect(center = (sword_x, sword_y))

        if pygame.mouse.get_pressed()[0] and pos[0] >= player.x:
            sword = pygame.transform.rotate(sword_scale, sword_angle - 120)
        elif pygame.mouse.get_pressed()[0] and pos[0] < player.x:
            sword = pygame.transform.rotate(sword_scale, sword_angle - 60)

        if zombie.colliderect(player):
            game_close = True


        if sword_rect.colliderect(zombie) and pygame.mouse.get_pressed()[0]:
            zombie_spawnpoint = random.choice([[0, round(random.randrange(0, screen_height), 10)],  [screen_width, round(random.randrange(0, screen_height), 10)], [round(random.randrange(0, screen_width), 10), 0],  [round(random.randrange(0, screen_width), 10), screen_height]])
            zombie = pygame.Rect((zombie_spawnpoint[0], zombie_spawnpoint[1], 50, 50))
            pygame.draw.rect(screen, 'green', zombie)

            

        screen.blit(sword, sword_rect)

        pygame.display.update()
        
        clock.tick(15)

    
    pygame.quit()


gameloop()