import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600
TITLE = "Jogo com personagem, chão e inimigos"

# === Personagem ===
character = Actor("char1", (100, 460))
character.facing_right = True
character.vy = 0  # Velocidade vertical
on_ground = True
gravity = 1
jump_power = -15
speed = 0
CHARACTER_LIMIT_LEFT = 100
CHARACTER_LIMIT_RIGHT = 400

# === Piso ===
grassy_grounds = []
FLOOR_HEIGHT = 520

for i in range(13):
    grassy_grounds.append(Actor("grassy_ground", (i * 64, FLOOR_HEIGHT)))

# === Inimigos ===
enemies = []

def create_enemy():
    enemy = Actor("zombie1", (randint(WIDTH, WIDTH + 500), FLOOR_HEIGHT - 40))
    enemy.facing_right = False
    enemies.append({"actor": enemy, "vy": 0, "alive": True})

for _ in range(5):
    create_enemy()

# === Tiro ===
bullets = []
enemy_bullets = []

def fire_bullet():
    if character.facing_right:
        bullet = Actor("bullet", (character.x + 30, character.y))
        bullet.vx = 10
    else:
        bullet = Actor("bullet", (character.x - 30, character.y))
        bullet.vx = -10
    bullets.append(bullet)

def fire_enemy_bullet(enemy):
    bullet = Actor("bullet", (enemy.x, enemy.y))
    bullet.vx = -5
    enemy_bullets.append(bullet)

# === Nuvens ===
clouds = [Actor("cloud1", (200, 100)), Actor("cloud1", (600, 150))]

# === Lógica principal ===

def update():
    global speed, on_ground

    # Gravidade
    character.vy += gravity
    character.y += character.vy

    # Verifica se está no chão
    if character.y >= FLOOR_HEIGHT - 60:
        character.y = FLOOR_HEIGHT - 60
        character.vy = 0
        on_ground = True
    else:
        on_ground = False

    # Movimento lateral
    if keyboard.right:
        speed = 5
        character.facing_right = True
    elif keyboard.left:
        speed = -5
        character.facing_right = False
    else:
        speed = 0

    scroll_world()
    update_bullets()
    update_enemies()
    update_floor()
    update_clouds()

def scroll_world():
    if speed > 0:
        if character.x < CHARACTER_LIMIT_RIGHT:
            character.x += speed
        else:
            move_world(-speed)
    elif speed < 0:
        if character.x > CHARACTER_LIMIT_LEFT:
            character.x += speed
        else:
            character.x = CHARACTER_LIMIT_LEFT  # Trava no limite esquerdo

def move_world(offset):
    for floor in grassy_grounds:
        floor.x += offset
    for enemy in enemies:
        enemy["actor"].x += offset
    for bullet in bullets:
        bullet.x += offset
    for bullet in enemy_bullets:
        bullet.x += offset
    for cloud in clouds:
        cloud.x += offset * 0.5  # Parallax nas nuvens

def update_bullets():
    for bullet in bullets[:]:
        bullet.x += bullet.vx
        if bullet.x < 0 or bullet.x > WIDTH:
            bullets.remove(bullet)

    for bullet in enemy_bullets[:]:
        bullet.x += bullet.vx
        if bullet.x < 0 or bullet.x > WIDTH:
            enemy_bullets.remove(bullet)

def update_enemies():
    for enemy in enemies:
        if enemy["alive"]:
            if randint(0, 100) < 1:
                fire_enemy_bullet(enemy["actor"])

def update_floor():
    # Reposiciona o piso se ele sair da tela
    if grassy_grounds and grassy_grounds[0].x < -64:
        grassy_grounds.pop(0)
        new_block = Actor("grassy_ground", (grassy_grounds[-1].x + 64, FLOOR_HEIGHT))
        grassy_grounds.append(new_block)

def update_clouds():
    for cloud in clouds:
        cloud.x -= 0.2
        if cloud.x < -100:
            cloud.x = WIDTH + 100

def draw():
    screen.clear()
    screen.fill((135, 206, 235))  # Céu azul

    for cloud in clouds:
        cloud.draw()

    for floor in grassy_grounds:
        floor.draw()

    for enemy in enemies:
        if enemy["alive"]:
            enemy["actor"].draw()

    for bullet in bullets:
        bullet.draw()

    for bullet in enemy_bullets:
        bullet.draw()

    character.draw()

def on_key_down(key):
    if key == keys.SPACE and on_ground:
        character.vy = jump_power
    if key == keys.RETURN:
        fire_bullet()

pgzrun.go()
