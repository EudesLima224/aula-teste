import pgzrun
import pygame
# Definir tamanho da tela
WIDTH = 800
HEIGHT = 600




cloud1 = Actor("cloud1", (200, 100))  # Posição inicial (X=200, Y=100)
cloud2 = Actor("cloud2", (650, 100))  # Posição inicial (X=200, Y=100)
clouds = [cloud1, cloud2]
def draw():
    screen.clear()
    screen.fill((135,206,250))  # Cor de fundo azul(ceu)

    for cloud in clouds:
        cloud.draw()









# Iniciar o jogo
pgzrun.go()