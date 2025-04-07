class animation:
    def __init__(self, type):
        self.type_animation = type


print(animation('oi').type_animation)





















class animation:
    def __init__(self, type):
        global FRAME_DELAY, frame_counter, indice_walk, indice_idle, character_idle, on_ground
        print(on_ground)
        frame_counter += 1
        self.animation_state = type
        if self.animation_state == "walking" and on_ground:
            if frame_counter >= FRAME_DELAY:
                player.actor.image = player.walk[player.indice_walk % len(player.walk)]
                player.indice_walk += 1
                frame_counter = 0
            
        elif self.animation_state == "walking_left" and on_ground:
            if frame_counter >= FRAME_DELAY:
                player.actor.image = player.walk_left[player.indice_walk % len(player.walk_left)]
                player.indice_walk += 1
                frame_counter = 0
        elif self.animation_state == "jump":
            player.actor.image = player.jump
        elif self.animation_state == "idle":
            if frame_counter >= 20:
                player.actor.image = player.idle[player.indice_idle % len(player.idle)]
                indice_idle = (player.indice_idle + 1) % len(player.idle)
                frame_counter = 0
        pass
