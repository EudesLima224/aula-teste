import pgzrun
from pygame import Rect
import random

# === CONFIGURAÇÕES ===
WIDTH = 1200
HEIGHT = 900
FLOOR_HEIGHT = HEIGHT - 20
CHARACTER_Y = FLOOR_HEIGHT - 128
CLOUD_POSITIONS = [(200, 100), (650, 150)]
FRAME_DELAY = 8
music_on = True
sound_on = True
game_over_time = 0
sound_game_over = True

# === VARIÁVEIS GLOBAIS ===
running = False
player_direction = 0  # -1 esquerda, 1 direita, 0 parado
world_speed = 0       # velocidade do mundo (chão, inimigos etc)
speed_y = 0
gravity = 0.8
jump_strength = -18
on_ground = True
frame_counter = 0
shot_cooldown = 0
shooting = False
enemy_spawn_timer = 0

# === INTERFACE ===
button_start = Rect((WIDTH // 2 - 200), 400, 400, 80)
button_music = Rect((WIDTH // 2 - 200), 500, 180, 80)
button_sound = Rect((WIDTH // 2 + 20), 500, 180, 80)

# === CENÁRIO ===
clouds = [Actor(f"cloud{i+1}", pos) for i, pos in enumerate(CLOUD_POSITIONS)]
grassy_grounds = [Actor("grassy_ground", (x, FLOOR_HEIGHT)) for x in range(0, WIDTH + 128, 64)]

# === PERSONAGEM ===
character = Actor("character_idle0", (250, CHARACTER_Y))
animation_state = "idle"
indice_idle = indice_walk = indice_gun = 0
character_idle = [f"character_idle{i}" for i in range(3)]
character_walk = [f"character_walk{i}" for i in range(8)]
character_walk_left = [f"character_walk_left{i}" for i in range(8)]
character_gun = [f"character_gun{i}" for i in range(3)]
character_jump = "character_jump"

# ===munição===
bullets = []
icon_bullets = 4
bullets_magazine = []
bulletsicon = Actor("life")
bulletsicon_position = {"x": 20, "y": 60}
for icon in range(icon_bullets):
    bullets_magazine.append(Actor("bulleticon", (bulletsicon_position["x"], bulletsicon_position["y"])))
    bulletsicon_position["x"] += 30
spawn_bullet = 0

# ===vida===
lifes_character = []
life = Actor("life")
life_character = 5
life_position = {"x": 20, "y": 20}
for life in range(life_character):
    lifes_character.append(Actor("life", (life_position["x"], life_position["y"])))
    life_position["x"] += 30
CHARACTER_LIMIT_RIGHT = 300
CHARACTER_LIMIT_LEFT = 20


# === INIMIGOS ===
enemies = []
enemy_frames = [f"enemy_robot_walk{i}" for i in range(8)]
enemy_attack_frames = [f"enemy_robot_attack{i}" for i in range(2)]
enemy_bullets = []
life_enemy = 3
enemy_spawn_delay = 50

# === FUNÇÕES PRINCIPAIS ===
def draw():
    screen.clear()
    screen.fill((135, 206, 250))
    start_music()
    if not running:
        draw_menu()
    else:
        draw_gameplay()

def update():
    if not running:
        return

    update_player_input()
    update_character()
    update_bullets()
    update_enemy_bullets()  # <- Adicionado aqui
    update_enemies()
    update_floor()


def on_mouse_down(pos):
    global running, music_on, sound_on, shooting, shot_cooldown
    if not running and button_start.collidepoint(pos):
        running = True
    if not running and button_music.collidepoint(pos):
        music_on = not music_on
        if music_on:
            print("Música ligada")
            start_music()
        else:
            print("Música desligada")
            stop_music()
    if not running and button_sound.collidepoint(pos):
        sound_on = not sound_on
        if sound_on:
            print("som ligado")
        else:
            print("som desligado")
    if running and shot_cooldown == 0 and len(bullets_magazine) > 0:
        shooting = True


# === DESENHO ===
def draw_menu():
    for cloud in clouds:
        cloud.draw()

    screen.draw.filled_rect(Rect((WIDTH // 2 - 250), 45, 500, 80), "blue")
    screen.draw.text("Robotic Adventures", ((WIDTH // 2 - 200), 65), fontsize=60, color="white")
    screen.draw.filled_rect(button_start, "blue")
    screen.draw.text("iniciar", ((WIDTH // 2 - 65), 420), fontsize=60, color="white")
    #botão musica
    if music_on:
        screen.draw.filled_rect(button_music, "blue")
    else:
        screen.draw.filled_rect(button_music, "red")
    screen.draw.text("music", ((WIDTH // 2 - 175), 520), fontsize=60, color="white")
    if sound_on:
        screen.draw.filled_rect(button_sound, "blue")
    else:
        screen.draw.filled_rect(button_sound, "red")
    screen.draw.text("sound", ((WIDTH // 2 + 50), 520), fontsize=60, color="white")

def draw_gameplay():
    global frame_counter, game_over_time, sound_game_over, running
    for floor in grassy_grounds:
        floor.draw()

    character.draw()

    for bullet in bullets:
        bullet.draw()


    for enemy in enemies:
        enemy["actor"].draw()

    for bullet in enemy_bullets:
        bullet.draw()
    
    for life in lifes_character:
        life.draw()
    for bulletincon in bullets_magazine:
        bulletincon.draw()

    if life_character <=0:
        screen.draw.filled_rect(Rect((WIDTH // 2 - 250), 520, 500, 100), "blue")
        screen.draw.text("GAME OVER!",((WIDTH // 2 - 200), 540), fontsize=90, color='white')
        game_over_time += 1
        stop_music()
        if sound_game_over and sound_on:
            sounds.game_over.play()
            sound_game_over = False
        if game_over_time > 300:
            reset_game()
            running = False
            game_over_time = 0
            sound_game_over = True


def reset_game():
    global enemies, bullets, enemy_bullets, speed, speed_y, on_ground, life_character
    enemies = []
    bullets = []
    enemy_bullets = []
    speed = 0
    speed_y = 0
    on_ground = True
    character.x = 300
    character.y = CHARACTER_Y
    life_character = 5
    life_position = {"x": 20, "y": 20}
    for life in range(life_character):
        lifes_character.append(Actor("life", (life_position["x"], life_position["y"])))
        life_position["x"] += 30

    # Resetar chão
    grassy_grounds.clear()
    for x in range(0, WIDTH + 128, 64):
        grassy_grounds.append(Actor("grassy_ground", (x, FLOOR_HEIGHT)))



# === CONTROLE DO JOGADOR ===
def update_player_input():
    global player_direction, speed_y, on_ground, shooting, animation_state, shot_cooldown

    keys = keyboard
    player_direction = 0

    if keys.right or keys.d:
        player_direction = 1
        animation_state = "walking"
        character.flip_x = False
    elif keys.left or keys.a:
        player_direction = -1
        animation_state = "walking_left"
    elif on_ground:
        animation_state = "idle"

    if (keys.up or keys.w) and on_ground:
        animation_state = "jump"
        speed_y = jump_strength
        if sound_on:
            sounds.jump1.play()
        on_ground = False

    if keys.lctrl and shot_cooldown == 0 and len(bullets_magazine) > 0:
            shooting = True

# === ANIMAÇÃO DO PERSONAGEM ===
def update_character():
    global frame_counter, character, speed_y, on_ground
    global animation_state, indice_idle, indice_walk, indice_gun, shot_cooldown, shooting

    frame_counter += 1

    # Atualiza a animação do personagem
    if animation_state == "walking" and on_ground:
        if frame_counter >= FRAME_DELAY:
            character.image = character_walk[indice_walk % len(character_walk)]
            indice_walk += 1
            frame_counter = 0
    if animation_state == "walking_left" and on_ground:
        if frame_counter >= FRAME_DELAY:
            character.image = character_walk_left[indice_walk % len(character_walk_left)]
            indice_walk += 1
            frame_counter = 0
    elif animation_state == "jump":
        character.image = character_jump
    elif animation_state == "idle":
        if frame_counter >= 20:
            character.image = character_idle[indice_idle % len(character_idle)]
            indice_idle = (indice_idle + 1) % len(character_idle)
            frame_counter = 0

    # Animação de tiro
    if shooting and shot_cooldown == 0:
        if frame_counter >= 1:
            character.image = character_gun[indice_gun % len(character_gun)]
            indice_gun += 1
            frame_counter = 0
            if indice_gun >= len(character_gun):
                indice_gun = 0
                shooting = False
                shot_cooldown = 20
                bullets.append(Actor("bullet", (character.x + 80, character.y + 50)))
                bullets_magazine.pop(-1)
                if sound_on:
                    sounds.laserretro_004.play()

    if shot_cooldown > 0:
        shot_cooldown -= 1

    # Gravidade
    speed_y += gravity
    character.y += speed_y

    for floor in grassy_grounds:
        if character.colliderect(floor):
            character.y = floor.top - character.height / 2
            speed_y = 0
            on_ground = True
            break

    # Movimento horizontal com limites de tela
    if player_direction != 0:
        if player_direction == -1 and character.x > CHARACTER_LIMIT_LEFT:
            character.x += player_direction * 3
        elif player_direction == 1 and character.x < CHARACTER_LIMIT_RIGHT:
            character.x += player_direction * 3
        else:
            if player_direction == 1:
                move_world(-3)





# === TIROS DO JOGADOR ===
def update_bullets():
    global spawn_bullet
    spawn_bullet += 1
    if spawn_bullet >= 75 and len(bullets_magazine) <= 4:
        print(spawn_bullet, len(bullets_magazine), "foi adicionado bala")
        bullets_magazine.append(Actor("bulleticon", (len(bullets_magazine) * 30 + 20, 60)))
        spawn_bullet = 0
    for bullet in bullets[:]:
        bullet.x += 10
        if bullet.x > WIDTH + 50:
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy["actor"]):
                    enemy["life"] -= 1
                    if enemy["life"] <= 0:
                        enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break

# === INIMIGOS ===
def update_enemies():
    global enemy_spawn_timer, enemy_spawn_delay
    enemy_spawn_timer += 1

    if enemy_spawn_timer >= enemy_spawn_delay:
        print(f"{enemy_spawn_delay}")
        spawn_enemy()
        enemy_spawn_timer = 0
        enemy_spawn_delay = random.randint(100, 340)

    for enemy in enemies[:]:
        update_enemy(enemy)
        if enemy["actor"].x <= -50:
            enemies.remove(enemy)

def spawn_enemy():
    if sound_on:
        sounds.powerup12.play()
    enemy = {
        "actor": Actor(enemy_frames[0], (WIDTH + 50, FLOOR_HEIGHT - 128)),
        "frame_index": 0,
        "attacking": False,
        "attack_timer": 0,
        "shot": False,
        "life": 3
    }
    enemies.append(enemy)

def update_enemy(enemy):
    dist = abs(enemy["actor"].x - character.x)
    if dist <= 750:
        enemy["attacking"] = True
        enemy["attack_timer"] += 1

        if enemy["attack_timer"] < 30:
            enemy["actor"].image = enemy_attack_frames[0]
        elif enemy["attack_timer"] == 30:
            enemy["actor"].image = enemy_attack_frames[1]
            if not enemy["shot"]:
                bullet = Actor("bullet", (enemy["actor"].x - 40, enemy["actor"].y + 50))
                bullet.direction = -1
                enemy_bullets.append(bullet)
                enemy["shot"] = True
                if sound_on:
                    sounds.lasersmall_003.play()
        elif enemy["attack_timer"] > 60:
            enemy["attack_timer"] = 0
            enemy["shot"] = False
    else:
        enemy["actor"].x -= 1.8
        enemy["attacking"] = False
        enemy["attack_timer"] = 0
        enemy["shot"] = False

        if frame_counter % 8 == 0:
            enemy["frame_index"] = (enemy["frame_index"] + 1) % len(enemy_frames)
            enemy["actor"].image = enemy_frames[enemy["frame_index"]]

# === CHÃO ===
def update_floor():
    global world_speed
    for floor in grassy_grounds:
        floor.x -= world_speed

    if grassy_grounds[0].x < -64:
        grassy_grounds.pop(0)
        new_floor = Actor("grassy_ground", (grassy_grounds[-1].x + 64, FLOOR_HEIGHT))
        grassy_grounds.append(new_floor)

def update_enemy_bullets():
    global life_character
    for bullet in enemy_bullets[:]:
        bullet.x += bullet.direction * 10
        if bullet.right < 0 or bullet.left > WIDTH:
            enemy_bullets.remove(bullet)
        elif bullet.colliderect(character):
            life_character -= 1
            if life_character >= 0:
                lifes_character.pop(-1)
            print(lifes_character)
            print("Personagem atingido!", life_character)
            enemy_bullets.remove(bullet)

def move_world(offset):
    # Move o chão
    for floor in grassy_grounds:
        floor.x += offset

    # Move os inimigos
    for enemy in enemies:
        enemy["actor"].x += offset

    # Move as balas
    for bullet in bullets:
        bullet.x += offset

    for bullet in enemy_bullets:
        bullet.x += offset

# === MUSICA ===
def start_music():
    if music_on and not music.is_playing("music"):
        music.set_volume(0.6)
        music.play("music")
        music.queue("music")

def stop_music():
    if music.is_playing("music"):
        music.stop()

#def sons(som):
    

# === INICIAR O JOGO ===
pgzrun.go()
