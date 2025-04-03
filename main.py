import pgzrun
import pygame
# Definir tamanho da tela
WIDTH = 800
HEIGHT = 600

#variavel para controlar o estado jogo
running = False

button_start = Rect((WIDTH // 2 - 150), 220, 300, 80)


# Criar um Actor para a nuvem
cloud1 = Actor("cloud1", (200, 100))  # Posição inicial (X=200, Y=100)
cloud2 = Actor("cloud2", (650, 100))  # Posição inicial (X=200, Y=100)
clouds = [cloud1, cloud2]


def draw():
    screen.clear()
    screen.fill((135,206,250))  # Cor de fundo azul(ceu)
    for cloud in clouds:
        cloud.draw()
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
        
def on_mouse_down(pos):
    global running
    if not running:
        if button_start.collidepoint(pos):  # Verifica se clicou no botão
            running = True

# Iniciar o jogo
pgzrun.go()
