import pgzrun
import pygame
import time

# Definir tamanho da tela
WIDTH = 1200
HEIGHT = 900

# Variável de controle
running = False
button_start = Rect((WIDTH // 2 - 150), 220, 300, 80)
speed = 0
indice_frame = 0
animation = "idle"

# Medir FPS
frame_count = 0
last_time = time.time()
fps = 0

# Delay animações
frame_counter = 0
frame_delay = 8

# Criar nuvens
cloud1 = Actor("cloud1", (200, 100))
cloud2 = Actor("cloud2", (650, 150))
clouds = [cloud1, cloud2]

# Criar chão
floor_height = HEIGHT - 20
grassy_grounds = [Actor("grassy_ground", (x, floor_height)) for x in range(0, WIDTH + 64 + 64, 64)]  

# Criar personagem
character_height = HEIGHT - 147
animation_now = "character_idle0"
character = Actor(animation_now, (300, character_height))

# Variáveis do pulo e gravidade
speed_y = 0
gravity = 0.5
jump_strength = -10
on_ground = True

# Animações do personagem
walking_frames = [f"character_walk{n}" for n in range(8)]
character_idle = [f"character_idle{n}" for n in range(3)]
indice_idle_frame = 0
indice_walking_frame = 0
character_jump = "character_jump"

def draw():
    screen.clear()
    screen.fill((135, 206, 250))  # Cor de fundo azul (céu)
    screen.draw.text(f"FPS: {int(fps)}", (10, 10), fontsize=30, color="white")

    # Menu inicial
    if not running:
        for cloud in clouds:
            cloud.draw()
        screen.draw.filled_rect(Rect((WIDTH // 2 - 150), 45, 300, 80), "blue")
        screen.draw.text("Meu Jogo", (270, 60), fontsize=80, color="white")
        screen.draw.filled_rect(button_start, "blue")
        screen.draw.text("iniciar", (320, 240), fontsize=60, color="white")
    else:
        for floor in grassy_grounds:
            floor.draw()  
        character.y = character_height  # Atualiza a posição do personagem
        character.draw()


def update():
    global last_time, frame_count, fps
    frame_count += 1
    current_time = time.time()
    elapsed_time = current_time - last_time

    # Atualiza o FPS a cada segundo
    if elapsed_time >= 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        last_time = current_time

    global indice_frame, speed, animation, frame_counter, character_height
    global speed_y, on_ground, jump_strength

    # Movimento lateral
    if keyboard.right or keyboard.D:
        speed = 3
        animation = "walking"

    # Pulo
    if (keyboard.up or keyboard.W) and on_ground:
        animation = "jump"
        speed_y = jump_strength
        on_ground = False

    # Gravidade
    speed_y += gravity  # Aplica a gravidade
    character_height += speed_y  # Atualiza a altura do personagem

    # Verifica colisão com o chão
    if character_height >= HEIGHT - 147:
        character_height = HEIGHT - 147
        speed_y = 0
        on_ground = True

    # Controle de frames da animação
    frame_counter += 1
    global indice_idle_frame, indice_walking_frame, animation_now

    if animation == "walking":
        if frame_counter >= 8:
            frame_counter = 0
            animation_now = walking_frames[indice_walking_frame % len(walking_frames)]
            indice_walking_frame = (indice_walking_frame + 1) % len(walking_frames)

    elif animation == "jump":
        animation_now = character_jump

    if animation == "idle":
        speed = 0
        if frame_counter >= 20:
            frame_counter = 0
            animation_now = character_idle[indice_idle_frame % len(character_idle)]
            indice_idle_frame = (indice_idle_frame + 1) % len(character_idle)

    # Movimentação do chão
    for floor in grassy_grounds:
        floor.x -= speed
    if grassy_grounds[0].x < -64:
        grassy_grounds.pop(0)
        new_grassy_ground = Actor("grassy_ground", (grassy_grounds[-1].x + 64, floor_height))
        grassy_grounds.append(new_grassy_ground)


def on_mouse_down(pos):
    global running
    if not running and button_start.collidepoint(pos):
        running = True


# Iniciar o jogo
pgzrun.go()
