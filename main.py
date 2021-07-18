import pygame,random,sys,time

# Initialize Pygame
pygame.init()

# Creating Screen of size 1000 * 600 px
screen = pygame.display.set_mode((1000, 600))

clock = pygame.time.Clock()

# Title And Icon
pygame.display.set_caption("Space Arcade")
icon = pygame.image.load("Icons/game_icon.png")
pygame.display.set_icon(icon)

def Insert_image():
    global background,player_image,enemy_image,bullet_image,life_image

    # Adding Background Images
    background=[]
    for i in range(3):
        background.append(pygame.transform.scale(pygame.image.load(f"Background/{i+1}.png").convert(), (1000, 600)))

    # Adding Player Image
    player_image = pygame.transform.scale(pygame.image.load("Icons/battleship.png"), (64, 64))

    # Adding Enenmy Images
    enemy_image = []
    for i in range(5):
        enemy_image.append(pygame.transform.scale(pygame.image.load(f"Icons/enemy{i+1}.png"), (64, 64)))

    # Adding Bullet Image
    bullet_image = pygame.transform.scale(pygame.image.load("Icons/bullet.png"), (40, 40))  # Resizing Image

    # Adding Life Image
    life_image = pygame.image.load("Icons/heart.png")

Insert_image()

def object_values():
    global player_x, player_y,player_speed
    global enemy_x, enemy_y , enemy_xspeed , enemy_yspeed , no_of_ememies
    global bullet_x, bullet_y, bullet_state ,bullet_speed
    global score, score_change,sc_count, no_of_life

    #Player Values
    player_x=480
    player_y=500
    player_speed = 1

    #Enemy Values
    enemy_x,enemy_y,enemy_xspeed,enemy_yspeed = [],[],[],[]
    no_of_ememies = 5
    for i in range(no_of_ememies):
        enemy_x.append(random.randint(0, 936))
        enemy_y.append(0)
        enemy_xspeed.append(2)
        enemy_yspeed.append(0.5)
        if enemy_x[i] < 468:
            enemy_xspeed[i] = -enemy_xspeed[i]

    #Bullet Values
    bullet_x=0
    bullet_y=480
    bullet_speed = 10
    bullet_state="ready"

    #Score Values
    score=0
    score_change=50
    sc_count = 1

    #Number Of Lifes
    no_of_life=3

def text_print(text, size,color,coordinate):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_img = font.render(str(text), True, color)
    screen.blit(text_img, coordinate)

def start_page():
    # Start Page
    screen.blit(background[0], (0, 0))
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

start_page()

pygame.key.set_repeat(True)

def mainwindow():
    global player_x, player_y, player_speed
    global enemy_x, enemy_y, enemy_xspeed, enemy_yspeed, no_of_ememies
    global bullet_x, bullet_y, bullet_state, bullet_speed
    global score, score_change,sc_count, no_of_life

    object_values()

    # Game Page
    running = True
    while running:
        # Display Background
        screen.blit(background[1], (0, 0))

        # Getting Input From User
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player_x < 940:
                        player_x += player_speed
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player_x > 0:
                        player_x -=player_speed
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_x = player_x + 16
                        bullet_state = "fire"

        # Display Player
        screen.blit(player_image, (player_x, player_y))

        # Changing Enemy Position
        for i in range(no_of_ememies):
            if enemy_x[i] <= 0 or enemy_x[i] >= 936:
                enemy_xspeed[i] = -enemy_xspeed[i]
            enemy_x[i] += enemy_xspeed[i]
            enemy_y[i] += enemy_yspeed[i]
            # Display Enemy
            screen.blit(enemy_image[i], (enemy_x[i], enemy_y[i]))

        # Bullet Movement
        if bullet_y <= 0:
            bullet_state = "ready"
            bullet_y = 480
        if bullet_state == "fire":
            bullet_y -= bullet_speed
            screen.blit(bullet_image, (bullet_x, bullet_y))

        # Enemy Collision and Score Update
        for i in range(no_of_ememies):
            #Checking Collision
            if bullet_y <= enemy_y[i] + 64 and bullet_y >= enemy_y[i] and bullet_state=="fire":
                if bullet_x + 16 >= enemy_x[i] and bullet_x + 16 <= enemy_x[i] + 64:
                    bullet_state = "ready"
                    bullet_y = 480
                    enemy_x[i] = random.randint(0, 936)
                    enemy_y[i] = 0
                    if enemy_x[i] < 468:
                        enemy_xspeed[i] *= -1
                    score += 1

            #Printing Score
            text_print("SCORE  " + str(score),20,(255,0,0),(10, 10))

            # Updating Life and Increasing Enemy Speed
            if score == sc_count * score_change:
                no_of_life += 1
                sc_count += 1
                for i in range(no_of_ememies):
                    enemy_xspeed[i]*=1.1
                    enemy_yspeed[i]*=1.1

            # Respawning enemy to Top
            if enemy_y[i] >= 427:
                enemy_y[i] = 0
                no_of_life -= 1

        # Displaying Life
        for i in range(no_of_life):
            screen.blit(life_image, (976 - (i * 24), 0))

        # Updating Display
        pygame.display.update()
        clock.tick(120)

        # Game Over
        if no_of_life <= 0:
            time.sleep(1.2)
            running = False

    if score<=10:
        color=(255,0,0)
    elif score>10 and score<=50:
        color=(255,255,0)
    else:
        color=(0,255,0)

    screen.blit(background[2], (0, 0))
    score_x_cod = 465 - (len(str(score)) - 1) * 30
    text_print(score, 110, color, (score_x_cod, 210))
    pygame.display.update()

    # Ending Screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    mainwindow()

mainwindow()