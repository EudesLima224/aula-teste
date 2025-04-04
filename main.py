import pgzrun
import pygame
# Definir tamanho da tela
WIDTH = 1200
HEIGHT = 900

#variavel de controle
running = False

button_start = Rect((WIDTH // 2 - 150), 220, 300, 80)
speed = 0
indice_frame = 0


# Criar um Actor para a nuvem
cloud1 = Actor("cloud1", (200, 100))  # Posição inicial (X=200, Y=100)
cloud2 = Actor("cloud2", (650, 150))  # Posição inicial (X=200, Y=100)
#cloud3 = Actor("cloud3", )
clouds = [cloud1, cloud2]

#criação chão
floor_height = HEIGHT - 20
grassy_ground = Actor("grassy_ground", (0, floor_height))
grassy_grounds = [Actor("grassy_ground", (x, floor_height)) for x in range(0, WIDTH + 64 + 64, 64)]  


#criação do personagem
character = Actor("character_idle1", (100, HEIGHT - 147))
#animação do personagem
walking_frames = ["character_walk0"]
for n in range(1, 7):
    walking_frames.append(Actor(f"character_walk{n}"))

def draw():
    screen.clear()
    screen.fill((135,206,250))  # Cor de fundo azul(ceu)
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
    if running:
        for floor in grassy_grounds:
            floor.draw()  # Desenha cada pedaço do chão
        character.draw()


def update():
    global indice frame
    global grassy_grounds
    #move o chão para a esquerda
    for floor in grassy_grounds:
        floor.x -= speed
    #se um pedaço sair da tela, remove ele e adiciona um novo
    if grassy_grounds[0].x < -64:
        grassy_grounds.pop(0) #remove o primeiro chao
        new_grassy_ground = Actor("grassy_ground", (grassy_grounds[-1].x + 64, floor_height))
        grassy_grounds.append(new_grassy_ground)#Adiciona o novo chao
    
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
