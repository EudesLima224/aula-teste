import pgzrun
from pygame import Rect
import time
# Definir tamanho da tela
WIDTH = 1200
HEIGHT = 900

#variavel de controle
running = False
button_start = Rect((WIDTH // 2 - 150), 220, 300, 80)
speed = 0
indice_frame = 0
animation = "idle"

#medir fps
frame_count = 0
last_time = time.time()
fps = 0

#delay animações
frame_counter = 0
frame_delay = 8

# Criar um Actor para a nuvem
cloud1 = Actor("cloud1", (200, 100))
cloud2 = Actor("cloud2", (650, 150))  
#cloud3 = Actor("cloud3", )
clouds = [cloud1, cloud2]

#criação chão
floor_height = HEIGHT - 20
grassy_grounds = [Actor("grassy_ground", (x, floor_height)) for x in range(0, WIDTH + 64 + 64, 64)]  


#criação do personagem
character_height = HEIGHT - 147
animation_now = "character_idle0"
character = Actor(animation_now, (300, floor_height - 128))
speed_y = 0
gravity = 0.8
jump_strength = -18
on_ground = True


#animação do personagem
walking_frames = [f"character_walk{n}" for n in range(8)]
character_idle = [f"character_idle{n}" for n in range(3)]
character_gun = [f"character_gun{n}" for n in range(3)]
shooting = False
shot = 0
bullets = []
indice_idle_frame = 0
indice_walking_frame = 0
indice_gun_frame = 0
character_jump = "character_jump"

#inimigos
enemy_frames = [f"enemy_robot_walk{n}" for n in range(8)]
enemies = []
enemy_spaw_time = 0
indice_enemy = 0

def draw():
    screen.clear()
    screen.fill((135,206,250))  # Cor de fundo azul(ceu)
    screen.draw.text(f"FPS: {int(fps)}", (10, 10), fontsize = 30, color="white")
    #menu
    if not running:
        #nuvems do menu
        for cloud in clouds:
            cloud.draw()
        #nome do jogo na placa
        screen.draw.filled_rect(Rect((WIDTH // 2 - 150), 45, 300, 80), "blue")
        screen.draw.text("Meu Jogo", (270, 60), fontsize = 80, color="white")
        #botão começar
        screen.draw.filled_rect(button_start, "blue")
        screen.draw.text("iniciar", (320, 240), fontsize=60, color="white")
    global character, animation_now
    if running:
        for floor in grassy_grounds:
            floor.draw()  # Desenha cada pedaço do chão
        character.image = animation_now
        character.draw()

        for bullet in bullets:
            bullet.draw()

        for enemy in enemies:
            enemy["actor"].draw()




def update():
    global last_time, frame_count, fps, grassy_grounds
    frame_count += 1
    current_time = time.time()
    elapsed_time = current_time - last_time

    #atualiza o fps a cada segundo
    if elapsed_time >= 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        last_time = current_time
    global indice_frame, speed, animation, frame_counter, character_height, floor_height, character_gun, indice_gun_frame
    global speed_y, on_ground, jump_strength, shooting, shot
    global enemy_spaw_time, enemie_frames, indice_enemy


    #verifica se ta andando-----------------------------
    if keyboard.right or keyboard.D:
        speed = 3
        animation = "walking"
    elif on_ground:
        speed = 0
        animation = "idle"
    #verifica o pulo
    #elif character_height >= floor_height - 128:
    if (keyboard.up or keyboard.W) and on_ground:
        animation = "jump"
        speed_y = jump_strength
        on_ground = False
    if keyboard.lctrl and shot == 0:
        shooting = True

    
    #controle de frames animação
    frame_counter += 1
    
    #animações
    global indice_idle_frame, indice_walking_frame, animation_now, character
    if animation == "walking":
        if frame_counter >= 8:
            frame_counter = 0
            if on_ground:
                animation_now = walking_frames[indice_walking_frame % len(walking_frames)]
                #print(animation_now)
                indice_walking_frame = (indice_walking_frame + 1) % len(walking_frames)
    

    elif animation == "jump":
            animation_now = character_jump
            #print(character.y)

    #gravidade
    speed_y += gravity
    character.y += speed_y
    for floor in grassy_grounds:
        if character.colliderect(floor):
            character.y = floor.top - character.height / 2
            speed_y = 0
            on_ground = True
            break  # Já colidiu com um, não precisa verificar os outros


    if animation == "idle":
        speed = 0
        if frame_counter >= 20:
            frame_counter = 0
            animation_now = character_idle[indice_idle_frame % len(character_idle)]
            #print(animation_now)
            if indice_idle_frame <= len(character_idle):
                indice_idle_frame = indice_idle_frame + 1
            elif indice_idle_frame > len(character_idle):
                indice_idle_frame = 0
    for bullet in bullets[:]:
        bullet.x += 10
        if bullet.x > WIDTH + 50:
            bullets.remove(bullet)
    if shooting and shot == 0:
        if frame_counter >= 1:
            frame_counter = 0
            animation_now = character_gun[indice_gun_frame % len(character_gun)]
            #print(animation_now)
            indice_gun_frame = (indice_gun_frame + 1) % len(character_gun)
            if animation_now == character_gun[2]:
                shooting = False
                shot = 20
                # Cria o tiro baseado na posição atual do personagem
                bullet = Actor("bullet", (character.x + 80, character.y + 50))
                bullets.append(bullet)
    if shot > 0:
        shot -= 1

    #spaw inimigos
    enemy_spaw_time += 1
    if enemy_spaw_time >= 90:
        enemy_spaw_time = 0
        enemy = {
            "actor": Actor(enemy_frames[0], (WIDTH + 50, floor_height - 128)),
            "frame_index": 0
        }
        enemies.append(enemy)

    #movimento dos inimigos
    for enemy in enemies[:]:
        # Calcula distância horizontal
        distancia = abs(enemy["actor"].x - character.x)
        if distancia > 700:  # só anda se estiver longe do personagem
            enemy["actor"].x -= 3

        # Atualiza animação
        if frame_counter % 8 == 0:
            enemy["frame_index"] = (enemy["frame_index"] + 1) % len(enemy_frames)
            enemy["actor"].image = enemy_frames[enemy["frame_index"]]

        # Remove se saiu da tela
        if enemy["actor"].x <= -50:
            enemies.remove(enemy)
    
    for enemy in enemies:
    

        #print(enemy.x)
        """for enemy in enemies[:]:  # cria uma cópia rasa da lista
            enemy["actor"].x -= 3
            if enemy["actor"].x <= -50:
                enemies.remove(enemy)"""



    #move o chão para a esquerda
    for floor in grassy_grounds:
        floor.x -= speed

    #se um pedaço sair da tela, remove ele e adiciona um novo
    if grassy_grounds[0].x < -64:
        grassy_grounds.pop(0) #remove o primeiro chao
        new_grassy_ground = Actor("grassy_ground", (grassy_grounds[-1].x + 64, floor_height))
        grassy_grounds.append(new_grassy_ground)#Adiciona o novo chao
    

    #spaw dos inimigos


def draw_floor(x, y):
    floor_width = 0
    while floor_width <= WIDTH:
        grassy_ground.draw( 0, 10, 20)
        floor_width += 20


        
def on_mouse_down(pos):
    global running
    if not running:
        if button_start.collidepoint(pos):  # Verifica se clicou no botão
            running = True

# Iniciar o jogo
pgzrun.go()
