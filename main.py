import pgzrun
from pygame import Rect
import random

# === CONFIGURAÇÕES ===
WIDTH = 1200
HEIGHT = 900
FLOOR_HEIGHT = HEIGHT - 20
CLOUD_POSITIONS = [(200, 100), (650, 150)]
FRAME_DELAY = 8
music_on = True
sound_on = True
game_over_time = 0
sound_game_over = True

# === VARIÁVEIS GLOBAIS ===
running = False
player_direction = 0  # -1 esquerda, 1 direita, 0 parado
speed_y = 0
gravity = 0.8
jump_strength = -18
on_ground = True
frame_counter = 0
shot_cooldown = 0
shooting = False
enemy_spawn_timer = 0
enemy_spawn_delay = 150
enemy_bullets = []


# === INTERFACE ===
button_start = Rect((WIDTH // 2 - 200), 400, 400, 80)
button_music = Rect((WIDTH // 2 - 200), 500, 180, 80)
button_sound = Rect((WIDTH // 2 + 20), 500, 180, 80)
button_quit = Rect((WIDTH// 2 - 200), 600, 400, 80)

# === CENÁRIO ===
clouds = [Actor(f"cloud{i+1}", pos) for i, pos in enumerate(CLOUD_POSITIONS)]
grassy_grounds = [Actor("grassy_ground", (x, FLOOR_HEIGHT)) for x in range(0, WIDTH + 128, 64)]


class Character:
    def __init__(self):
        self.actor = Actor("character_idle0", (250, FLOOR_HEIGHT - 128))
        self.animation_state = "idle"
        self.indice_idle = 0
        self.indice_walk = 0
        self.indice_gun = 0
        self.idle = [f"character_idle{i}" for i in range(3)]
        self.walk = [f"character_walk{i}" for i in range(8)]
        self.walk_left = [f"character_walk_left{i}" for i in range(8)]
        self.gun = [f"character_gun{i}" for i in range(3)]
        self.jump = "character_jump"
        self.life = 5
    def draw(self):
        self.actor.draw()

# === PERSONAGEM ===
player = Character()

# ===munição===
bullets = []
icon_bullets = 4
bullets_magazine = []
bulletsicon_position = {"x": 20, "y": 60}
for icon in range(icon_bullets):
    bullets_magazine.append(Actor("bulleticon", (bulletsicon_position["x"], bulletsicon_position["y"])))
    bulletsicon_position["x"] += 30
spawn_bullet = 0

# ===vida===
lifes_character = []
life_position = {"x": 20, "y": 20}
for life in range(player.life):
    lifes_character.append(Actor("life", (life_position["x"], life_position["y"])))
    life_position["x"] += 30
CHARACTER_LIMIT_RIGHT = 300
CHARACTER_LIMIT_LEFT = 20

class Enemy:
    def __init__(self, x, y):
        self.actor = Actor("enemy_robot_walk0", (x, y))
        self.walk_frames = [f"enemy_robot_walk{i}" for i in range(8)]
        self.attack_frames = [f"enemy_robot_attack{i}" for i in range(2)]
        self.frame_index = 0
        self.attacking = False
        self.attack_timer = 0
        self.shot = False
        self.life = 3
        self.direction = -1
        self.speed = 1.8

    def update(self):
        dist = abs(self.actor.x - player.actor.x)
        if dist <= 750:
            self.attacking = True
            self.attack_timer += 1
            if self.attack_timer < 30:
                self.actor.image = self.attack_frames[0]
            elif self.attack_timer == 30:
                self.actor.image = self.attack_frames[1]
                if not self.shot:
                    bullet = Actor("bullet", (self.actor.x - 40, self.actor.y + 50))
                    bullet.direction = -1
                    enemy_bullets.append(bullet)
                    self.shot = True
                    if sound_on:
                        sounds.lasersmall_003.play()
            elif self.attack_timer > 60:
                self.attack_timer = 0
                self.shot = False
        else:
            self.attacking = False
            self.attack_timer = 0
            self.shot = False
            self.actor.x += self.direction * self.speed
            if frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.actor.image = self.walk_frames[self.frame_index]

    def draw(self):
        self.actor.draw()


# === INIMIGOS ===
enemies = []

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
    update_enemy_bullets()
    update_enemies()
    update_floor()


def on_mouse_down(pos, button):
    global running, music_on, sound_on, shooting, shot_cooldown
    if button == mouse.LEFT:
        if not running and button_start.collidepoint(pos):
            running = True
        if not running and button_music.collidepoint(pos):
            music_on = not music_on
            if music_on:
                start_music()
            else:
                stop_music()
        if not running and button_sound.collidepoint(pos):
            sound_on = not sound_on
        if running and shot_cooldown == 0 and len(bullets_magazine) > 0:
            shooting = True
        if button_quit.collidepoint(pos) and not running:
            quit()


# === DESENHO ===
def draw_menu():
    for cloud in clouds:
        cloud.draw()

    screen.draw.filled_rect(Rect((WIDTH // 2 - 250), 45, 500, 80), "blue")
    screen.draw.text("Robotic Adventures", ((WIDTH // 2 - 200), 65), fontsize=60, color="white")
    screen.draw.filled_rect(button_start, "blue")
    screen.draw.text("Start", ((WIDTH // 2 - 55), 420), fontsize=60, color="white")
    screen.draw.filled_rect(button_quit, "blue")
    screen.draw.text("Quit", ((WIDTH // 2 - 55), 620), fontsize=60, color="white")
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
    for group in (grassy_grounds, bullets, enemies, enemy_bullets, lifes_character, bullets_magazine):
        for intem in group:
            intem.draw()
    player.draw()
    if player.life <=0:
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
    global enemies, bullets, enemy_bullets, speed_y, on_ground, player
    enemies = []
    bullets = []
    enemy_bullets = []
    speed_y = 0
    on_ground = True
    player = Character()
    life_position = {"x": 20, "y": 20}
    for life in range(player.life):
        lifes_character.append(Actor("life", (life_position["x"], life_position["y"])))
        life_position["x"] += 30


# === CONTROLE DO JOGADOR ===
def update_player_input():
    global player_direction, speed_y, on_ground, shooting, shot_cooldown

    keys = keyboard
    player_direction = 0

    if keys.right or keys.d:
        player_direction = 1
        player.animation_state = "walking"
    elif keys.left or keys.a:
        player_direction = -1
        player.animation_state = "walking_left"
    elif on_ground:
        player.animation_state = "idle"
    if (keys.up or keys.w) and on_ground:
        on_ground = False
        player.animation_state = "jump"
        speed_y = jump_strength
        if sound_on:
            sounds.jump1.play()
    if keys.lctrl and shot_cooldown == 0 and len(bullets_magazine) > 0:
            shooting = True

# === ANIMAÇÃO DO PERSONAGEM ===
def update_character():
    global shot_cooldown, shooting, frame_counter, speed_y, on_ground

    frame_counter += 1

    # Atualiza a animação do personagem
    if player.animation_state == "walking" and on_ground:
        if frame_counter >= FRAME_DELAY:
            player.actor.image = player.walk[player.indice_walk % len(player.walk)]
            player.indice_walk += 1
            frame_counter = 0
    if player.animation_state == "walking_left" and on_ground:
        if frame_counter >= FRAME_DELAY:
            player.actor.image = player.walk_left[player.indice_walk % len(player.walk_left)]
            player.indice_walk += 1
            frame_counter = 0
    elif player.animation_state == "jump":
        player.actor.image = player.jump
    elif player.animation_state == "idle":
        if frame_counter >= 20:
            player.actor.image = player.idle[player.indice_idle % len(player.idle)]
            player.indice_idle = (player.indice_idle + 1) % len(player.idle)
            frame_counter = 0

    # Animação de tiro
    if shooting and shot_cooldown == 0:
        if frame_counter >= 1:
            player.actor.image = player.gun[player.indice_gun % len(player.gun)]
            player.indice_gun += 1
            frame_counter = 0
            if player.indice_gun >= len(player.gun):
                player.indice_gun = 0
                shooting = False
                shot_cooldown = 20
                bullets.append(Actor("bullet", (player.actor.x + 60, player.actor.y + 50)))
                bullets_magazine.pop(-1)
                if sound_on:
                    sounds.laserretro_004.play()

    if shot_cooldown > 0:
        shot_cooldown -= 1

    # Gravidade
    speed_y += gravity
    player.actor.y += speed_y
    for floor in grassy_grounds:
        if player.actor.colliderect(floor):
            player.actor.y = floor.top - player.actor.height / 2
            speed_y = 0
            on_ground = True
            break

    # Movimento horizontal com limites de tela
    if player_direction != 0:
        if player_direction == -1 and player.actor.x > CHARACTER_LIMIT_LEFT:
            player.actor.x += player_direction * 3
        elif player_direction == 1 and player.actor.x < CHARACTER_LIMIT_RIGHT:
            player.actor.x += player_direction * 3
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
                if bullet.colliderect(enemy.actor):
                    enemy.life -= 1
                    if enemy.life <= 0:
                        enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break

# === INIMIGOS ===
def update_enemies():
    global enemy_spawn_timer, enemy_spawn_delay

    enemy_spawn_timer += 1

    if enemy_spawn_timer >= enemy_spawn_delay:
        spawn_enemy()
        enemy_spawn_timer = 0
        enemy_spawn_delay = random.randint(100, 340)

    for enemy in enemies[:]:
        enemy.update()
        if enemy.actor.x <= -50:
            enemies.remove(enemy)


def spawn_enemy():
    if sound_on:
        sounds.powerup12.play()
    enemy = Enemy(WIDTH + 50, FLOOR_HEIGHT - 128)
    enemies.append(enemy)


# === CHÃO ===
def update_floor():
    if grassy_grounds[0].x < -64:
        grassy_grounds.pop(0)
        new_floor = Actor("grassy_ground", (grassy_grounds[-1].x + 64, FLOOR_HEIGHT))
        grassy_grounds.append(new_floor)

def update_enemy_bullets():
    for bullet in enemy_bullets[:]:
        bullet.x += bullet.direction * 6  #
        if bullet.x < -50 or bullet.x > WIDTH + 50:
            enemy_bullets.remove(bullet)
        elif bullet.colliderect(player.actor):
            enemy_bullets.remove(bullet)
            player.life -= 1
            if len(lifes_character) > 0:
                lifes_character.pop(-1)


def move_world(offset):
    for group in (grassy_grounds, bullets, enemy_bullets):
        for item in group:
            item. x += offset
    # Move os inimigos
    for enemy in enemies:
        enemy.actor.x += offset

# === MUSICA ===
def start_music():
    if music_on and not music.is_playing("music"):
        music.set_volume(0.6)
        music.play("music")
        music.queue("music")

def stop_music():
    if music.is_playing("music"):
        music.stop()


# === INICIAR O JOGO ===
pgzrun.go()
