import pgzrun
import random

WIDTH = 800
HEIGHT = 400

# Estado do som
sound_on = True

# --- CLASSES ---

class Character:
    def __init__(self):
        self.actor = Actor("character_idle1", pos=(100, 300))
        self.velocity_y = 0
        self.on_ground = True
        self.animation_index = 0
        self.animation_timer = 0
        self.sprites = ["character_idle1", "character_idle2"]

    def update(self):
        self.apply_gravity()
        self.animate()

    def draw(self):
        self.actor.draw()

    def apply_gravity(self):
        self.actor.y += self.velocity_y
        self.velocity_y += 0.5
        if self.actor.y >= 300:
            self.actor.y = 300
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = -10
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

    def shoot(self):
        bullet = Bullet(self.actor.x + 30, self.actor.y)
        game.bullets.append(bullet)
        if sound_on:
            sounds.pew.play()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer > 10:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.sprites)
            self.actor.image = self.sprites[self.animation_index]


class Bullet:
    def __init__(self, x, y):
        self.actor = Actor("bullet", (x, y))

    def update(self):
        self.actor.x += 10

    def draw(self):
        self.actor.draw()


class Enemy:
    def __init__(self):
        self.actor = Actor("enemy1", (random.randint(WIDTH, WIDTH + 300), 300))

    def update(self):
        self.actor.x -= 4

    def draw(self):
        self.actor.draw()


class HUD:
    def __init__(self):
        self.score = 0
        self.lives = 3

    def draw(self):
        screen.draw.text(f"Score: {self.score}", (10, 10), fontsize=30, color="white")
        screen.draw.text(f"Lives: {self.lives}", (10, 40), fontsize=30, color="white")


class Game:
    def __init__(self):
        self.character = Character()
        self.bullets = []
        self.enemies = []
        self.hud = HUD()
        self.spawn_timer = 0
        self.game_over = False

    def update(self):
        if self.game_over:
            return

        self.character.update()

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.actor.x < WIDTH]

        for enemy in self.enemies:
            enemy.update()

        self.handle_collisions()

        self.spawn_timer += 1
        if self.spawn_timer > 60:
            self.spawn_timer = 0
            self.enemies.append(Enemy())

    def draw(self):
        screen.clear()
        if self.game_over:
            screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        else:
            self.character.draw()
            for bullet in self.bullets:
                bullet.draw()
            for enemy in self.enemies:
                enemy.draw()
            self.hud.draw()

    def handle_collisions(self):
        for enemy in self.enemies:
            if self.character.actor.colliderect(enemy.actor):
                self.hud.lives -= 1
                self.enemies.remove(enemy)
                if self.hud.lives <= 0:
                    self.game_over = True
                return

            for bullet in self.bullets:
                if bullet.actor.colliderect(enemy.actor):
                    self.hud.score += 1
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    return

# --- FUNÇÕES PRINCIPAIS DO JOGO ---

game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_key_down(key):
    if key == keys.SPACE:
        game.character.jump()
    elif key == keys.F:
        game.character.shoot()

def on_mouse_down():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        sounds.powerup.play()

pgzrun.go()
