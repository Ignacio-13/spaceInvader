import pygame
import random
import math
import sys
import os

# Inicializar pygame
pygame.init()

# Establece el tamaño de la pantalla
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Función para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar imagen de fondo
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

# Cargar icono de ventana
asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

# Cargar sonido de fondo
asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

# Cargar imagen del jugador
asset_playerimg = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

# Cargar imagen de bala
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# Cargar fuente para texto de game over
asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

# Cargar fuente para texto de puntaje
asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

# Establecer título de ventana
pygame.display.set_caption("Space Invader")

# Establecer icono de ventana
pygame.display.set_icon(icon)

# Reproducir sonido de fondo en loop
pygame.mixer.music.play(-1)

# Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Posición inicial del jugador
playerX = 270
playerY = 480
playerx_change = 0

# Lista para almacenar posiciones de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

# Se inicializan las variables para guardar las posiciones de los enemigos
for i in range(no_of_enemies):
    if i % 2 == 0:
        enemy_img_path = 'assets/images/enemy1.png'
    else:
        enemy_img_path = 'assets/images/enemy2.png'
    enemy_img = resource_path(enemy_img_path)
    enemyimg.append(pygame.image.load(enemy_img))
    enemyX.append(random.randint(0, 536))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Se inicializan las variables para guardar la posición de la bala
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Se inicializa la puntuación en 0
score = 0

# Función para mostrar la puntuación en la pantalla
def show_score():
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

# Función para dibujar al jugador en la pantalla
def player(x, y):
    screen.blit(playerimg, (x, y))

# Función para dibujar al enemigo en la pantalla
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Función para disparar la bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# Función para comprobar si ha habido una colisión entre la bala y el enemigo
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Función para mostrar el texto de game over en pantalla
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = over_text.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(over_text, text_rect)

# Función principal del juego
def gameloop():
    global score
    global playerX
    global playerx_change
    global bulletX
    global bulletY
    global bullet_state

    in_game = True
    while in_game:
        # Limpia la pantalla
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerx_change = -5
                if event.key == pygame.K_RIGHT:
                    playerx_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerx_change = 0

        # Aquí se está actualizando la posición del jugador
        playerX += playerx_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 536:
            playerX = 536

        # Bucle que se ejecuta para cada enemigo
        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                in_game = False
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 536:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            # Aquí se comprueba si ha habido una colisión entre enemigo y una bala
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 536)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        if bulletY < 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score()

        pygame.display.update()
        clock.tick(120)

gameloop()