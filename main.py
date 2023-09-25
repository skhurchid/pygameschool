import pygame
import os 
pygame.font.init()

width, height = 900, 500
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alien Shooter")

orange = (185, 120, 42)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

border = pygame.Rect(width//2, 0, 10, height)

points_font = pygame.font.SysFont('comicsans', 40)

fps = 60
velocity = 5
bullet_velocity = 7
max_bullets = 10
spaceship_width, spaceship_height = 55, 40

red_hit = pygame.USEREVENT + 1
yellow_hit = pygame.USEREVENT + 2

yellow_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height)), 270)
red_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height)), 90)

space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'ssspace.png')), (width, height))


def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_points, red_points):
   WIN.blit(space, (0,0))
   pygame.draw.rect(WIN, black, border)

   yellow_points_text = points_font.render("Points: " + str(yellow_points), 1, white)
   red_points_text = points_font.render("Points: " + str(red_points), 1, white)
   WIN.blit(yellow_points_text), (width - yellow_points_text.get_width() - 10, 10)
   WIN.blit(red_points_text, (10,10))


   WIN.blit(yellow_spaceship, (yellow.x, yellow.y))
   WIN.blit(red_spaceship, (red.x, red.y))

   for bullet in yellow_bullets:
       pygame.draw.rect(WIN, 'yellow', bullet)

   for bullet in red_bullets:
       pygame.draw.rect(WIN, 'red', bullet)

   pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - velocity > -1: #left
        red.x -= velocity
    if keys_pressed[pygame.K_d] and red.x + velocity + red.width < border.x + 10: #right
        red.x += velocity    
    if keys_pressed[pygame.K_w] and red.y - velocity > 0: #up
        red.y -= velocity
    if keys_pressed[pygame.K_s] and red.y + velocity + red.height < height - 15: #down
        red.y += velocity

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - velocity > border.x + 10: #left
        yellow.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and yellow.x + velocity < width - 40: #right
         yellow.x += velocity    
    if keys_pressed[pygame.K_UP] and yellow.y - velocity > 0: #up
        yellow.y -= velocity
    if keys_pressed[pygame.K_DOWN] and yellow.y + velocity + yellow.height < height - 15: #down
        yellow.y += velocity

def handle_bullets(red_bullets, yellow_bullets, red, yellow, yellow_points, red_points):
    for bullet in red_bullets:
        bullet.x += bullet_velocity
        if yellow.colliderect(bullet):
           pygame.event.post(pygame.event.Event(yellow_hit))
           red_bullets.remove(bullet)
        elif bullet.x > width:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x -= bullet_velocity
        if red.colliderect(bullet):
           pygame.event.post(pygame.event.Event(red_hit))
           yellow_bullets.remove(bullet)    
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


def main():
    red = pygame.Rect(100, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(700, 300, spaceship_width, spaceship_height)

    yellow_bullets = []
    red_bullets = []

    yellow_points = 0
    red_points = 0


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(red_bullets) < max_bullets:
                    bullet =  pygame.Rect(red.x + red.width, red.y + red.height//2 + 2, 10, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < max_bullets:    
                    bullet =  pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
            
            if event.type == yellow_hit:
                red_points += 1

            if event.type == red_hit:
                yellow_points += 1
            print(red_points, yellow_points)
        winner_text = ""
        if red_points == 30:
            winner_text = "Red Wins!"

        if yellow_points == 30:
            winner_text = "Yellow wins!"

        if winner_text != "":
            pass # Someone Won
             
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)
        
        handle_bullets(red_bullets, yellow_bullets, red, yellow, yellow_points, red_points)





        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_points, red_points)
    pygame.quit()

if __name__ == "__main__":
    main()
