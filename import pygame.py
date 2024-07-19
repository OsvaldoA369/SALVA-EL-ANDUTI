import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ÑANDUTI GAME')

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Cargar imágenes
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')
item_img = pygame.image.load('ñanduti.png')
background_img = pygame.image.load('fondo.png')  # Cargar la imagen de fondo
menu_background_img = pygame.image.load('login.png')  # Fondo del menú principal

# Escalar imágenes
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 10))
item_img = pygame.transform.scale(item_img, (30, 30))
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))  # Escalar la imagen de fondo
menu_background_img = pygame.transform.scale(menu_background_img, (screen_width, screen_height))

# Cargar sonidos
pygame.mixer.music.load('music.mp3')  # Música de fondo
pain_sound = pygame.mixer.Sound('dolor.mp3')  # Sonido de dolor
fail_sound = pygame.mixer.Sound('fail.mp3')  # Sonido de derrota
win_sound = pygame.mixer.Sound('win.mp3')  # Sonido de victoria

# Reproducir la música de fondo en bucle
pygame.mixer.music.play(-1)

# Configuración del reloj
clock = pygame.time.Clock()

# Estados del juego
MENU = 0
JUEGO = 1
RESULTADO = 2
PAUSA = 3
NIVEL2 = 4
estado_juego = MENU

# Variables del juego
player_pos = [screen_width // 2, screen_height // 2]
player_speed = 7
player_lives = 3
enemy_size = 50
enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
enemy_speed = 3
enemy_direction = 0  # Dirección inicial del enemigo
enemy_max_health = 3  # Salud máxima del enemigo
current_enemy_health = enemy_max_health  # Salud actual del enemigo
bullet_size = 5
bullet_speed = 8
bullets = []
item_size = 100
item_pos = [random.randint(0, screen_width - item_size), random.randint(0, screen_height - item_size)]
item_collected = 0
item_appearance_time = 0
item_duration = 5000  # 5 segundos en milisegundos
player_direction = 0
direction_angles = {0: 270, 1: 180, 2: 90, 3: 0}
game_over_text = ""
win_text = ""

# Variables para controlar el disparo
shoot_delay = 1000  # 1000 milisegundos = 1 segundo
last_shot_time = 0  # Tiempo del último disparo

# Función para detectar colisiones
def detect_collision(object1_pos, object2_pos, object1_size, object2_size):
    o1_x, o1_y = object1_pos
    o2_x, o2_y = object2_pos
    return (o1_x < o2_x < o1_x + object1_size or o2_x < o1_x < o2_x + object2_size) and (o1_y < o2_y < o1_y + object1_size or o2_y < o1_y < o2_y + object2_size)

# Función para mostrar el menú principal
def mostrar_menu():
    screen.blit(menu_background_img, (0, 0))
    font = pygame.font.Font(None, 74)
    titulo_text = font.render('Juego del Ñanduti', True, WHITE)
    screen.blit(titulo_text, (screen_width//2 - titulo_text.get_width()//2, 100))

    font = pygame.font.Font(None, 36)
    iniciar_text = font.render('Iniciar Juego (Enter)', True, WHITE)
    salir_text = font.render('Salir (Esc)', True, WHITE)
    screen.blit(iniciar_text, (screen_width//2 - iniciar_text.get_width()//2, 300))
    screen.blit(salir_text, (screen_width//2 - salir_text.get_width()//2, 400))

    pygame.display.flip()

# Función para mostrar el resultado
def mostrar_resultado(texto):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    resultado_text = font.render(texto, True, WHITE)
    screen.blit(resultado_text, (screen_width//2 - resultado_text.get_width()//2, screen_height//2 - resultado_text.get_height()//2))
    pygame.display.flip()

# Función para mostrar pausa
def mostrar_pausa():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    pausa_text = font.render("Juego en Pausa", True, WHITE)
    screen.blit(pausa_text, (screen_width//2 - pausa_text.get_width()//2, screen_height//2 - pausa_text.get_height()//2))
    pygame.display.flip()

# Bucle principal del juego
running = True
pausa = False
mensaje_mostrado = False
tiempo_mensaje = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if estado_juego == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    estado_juego = JUEGO
                    player_pos = [screen_width // 2, screen_height // 2]
                    player_lives = 3
                    item_collected = 0
                    bullets = []
                    enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
                    current_enemy_health = enemy_max_health
                if event.key == pygame.K_ESCAPE:
                    running = False
        elif estado_juego == RESULTADO:
            if event.type == pygame.KEYDOWN:
                estado_juego = MENU
        elif estado_juego == PAUSA:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    estado_juego = JUEGO
        elif estado_juego == JUEGO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    estado_juego = PAUSA

    if estado_juego == MENU:
        mostrar_menu()
    elif estado_juego == RESULTADO:
        mostrar_resultado(game_over_text)
        if not mensaje_mostrado:
            tiempo_mensaje = pygame.time.get_ticks()
            mensaje_mostrado = True
        else:
            if pygame.time.get_ticks() - tiempo_mensaje >= 3000:
                estado_juego = MENU
                mensaje_mostrado = False
    elif estado_juego == PAUSA:
        mostrar_pausa()
    elif estado_juego == JUEGO:
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Movimiento del jugador
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
            player_direction = 2
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
            player_direction = 0
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
            player_direction = 3
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed
            player_direction = 1

        # Disparo de balas
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > shoot_delay:
                last_shot_time = current_time
                if player_direction == 0:
                    bullet_pos = [player_pos[0] + 50, player_pos[1] + 25]
                    bullet_dir = (bullet_speed, 0)
                elif player_direction == 1:
                    bullet_pos = [player_pos[0] + 25, player_pos[1] + 50]
                    bullet_dir = (0, bullet_speed)
                elif player_direction == 2:
                    bullet_pos = [player_pos[0], player_pos[1] + 25]
                    bullet_dir = (-bullet_speed, 0)
                elif player_direction == 3:
                    bullet_pos = [player_pos[0] + 25, player_pos[1]]
                    bullet_dir = (0, -bullet_speed)
                bullets.append((bullet_pos, bullet_dir))

        # Movimiento de las balas
        for bullet in bullets:
            bullet[0][0] += bullet[1][0]
            bullet[0][1] += bullet[1][1]

        # Eliminar balas fuera de la pantalla
        bullets = [bullet for bullet in bullets if 0 <= bullet[0][0] <= screen_width and 0 <= bullet[0][1] <= screen_height]

        # Movimiento del enemigo
        move_x, move_y = 0, 0
        if enemy_pos[0] < player_pos[0]:
            move_x = enemy_speed
            enemy_direction = 0
        elif enemy_pos[0] > player_pos[0]:
            move_x = -enemy_speed
            enemy_direction = 2
        if enemy_pos[1] < player_pos[1]:
            move_y = enemy_speed
            enemy_direction = 1
        elif enemy_pos[1] > player_pos[1]:
            move_y = -enemy_speed
            enemy_direction = 3
        enemy_pos[0] += move_x
        enemy_pos[1] += move_y

        # Detección de colisiones entre balas y enemigo
        for bullet in bullets:
            if detect_collision(bullet[0], enemy_pos, bullet_size, enemy_size):
                bullets.remove(bullet)
                current_enemy_health -= 1
                pain_sound.play()
                if current_enemy_health <= 0:
                    enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
                    current_enemy_health = enemy_max_health

        # Detección de colisiones entre jugador y enemigo
        if detect_collision(player_pos, enemy_pos, 50, enemy_size):
            player_lives -= 1
            pain_sound.play()
            if player_lives <= 0:
                fail_sound.play()
                game_over_text = "¡PERDISTE LOS ÑANDUTI!"
                estado_juego = RESULTADO
            enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]

        # Detección de recolección de ítems
        if detect_collision(player_pos, item_pos, 50, item_size):
            item_collected += 1
            item_pos = [random.randint(0, screen_width - item_size), random.randint(0, screen_height - item_size)]
            item_appearance_time = pygame.time.get_ticks()

        # Actualización de posición del ítem después de cierto tiempo
        current_time = pygame.time.get_ticks()
        if current_time - item_appearance_time >= item_duration:
            item_pos = [random.randint(0, screen_width - item_size), random.randint(0, screen_height - item_size)]
            item_appearance_time = current_time

        # Dibujo de imagen de fondo
        screen.blit(background_img, (0, 0))

        # Dibujo de jugador con rotación
        rotated_player = pygame.transform.rotate(player_img, direction_angles[player_direction])
        screen.blit(rotated_player, player_pos)

        # Dibujo de enemigo con rotación
        rotated_enemy = pygame.transform.rotate(enemy_img, direction_angles[enemy_direction])
        screen.blit(rotated_enemy, enemy_pos)

        # Dibujo de balas
        for bullet in bullets:
            screen.blit(bullet_img, bullet[0])

        # Dibujo de ítem
        screen.blit(item_img, item_pos)

        # Mostrar vidas e ítems recolectados
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f'Vidas: {player_lives}', True, WHITE)
        items_text = font.render(f'Ñandutis: {item_collected}/3', True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(items_text, (10, 50))

        # Dibujo de barra de vida del enemigo
        pygame.draw.rect(screen, BLACK, (screen_width - 110, 10, 100, 20))
        pygame.draw.rect(screen, WHITE, (screen_width - 110, 10, 100 * (current_enemy_health / enemy_max_health), 20))

        # Actualización de la pantalla
        pygame.display.flip()

        # Control de velocidad del bucle del juego
        clock.tick(30)

        # Verificación de condición de victoria
        if item_collected >= 3:
            win_sound.play()
            game_over_text = "¡SALVASTE EL ÑANDUTI!"
            estado_juego = RESULTADO

pygame.quit()
