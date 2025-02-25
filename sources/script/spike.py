from entity import Entity
import pygame
from settings import *

class Spike(Entity):
    def __init__(self, x, y, image, groupes, textures, name):
        """Spike héritant de la classe Entité, est hostile au joueur

        Args:
            x (int): pos x
            y (int): pos y
            image (pygame.image): image par défaut (utile uniquement pour la classe Entity)
            groupes (list): liste de groupes auquels appartient l'Enemy
            textures (dict): dictionnaire contenant les textures rendues pygame         
            name (str): Nom de la classe de l'ennemi
        """ 
        super().__init__(x, y, image, groupes, hitbox=pygame.Rect(x+15,y+8, 40, 40))
        self.name = name

        self.textures = textures
        self.action = "idle"

        self.basey = self.surface.top # spike apparait derrière le joueur

        self.trigger_cooldown = 0
        self.animation_counter_fps = 0

        self.damage = spike_damage
        
    def check_trigger(self, player):
        """Gestion de l'état du spike ainsi que de ses collisions et états

        Args:
            player (player object): objet du joueur pour les collisions et la gestion des dégats

        Returns:
            int: dégats infligés
        """
        global actual_sound_channel 

        if self.rect.colliderect(player.rect) and self.action == "idle" :            
            self.action = "triggered"
            self.animate()
            self.trigger_cooldown = 1

            # joue son trigger
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "spike\\trigger.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1


            return 0

        elif self.rect.colliderect(player.rect) and self.animation_counter_fps // (FPS//spike_exit_speed) == 5 and self.action == "retrieve_still": # spikes sortis complètement            
            self.animate()
            self.action = "retrieving"
            return self.damage
        
        else:
            self.animate()

    def animate(self):
        """Sous fonction de move(), s'occupe plus précisément des animations de l'ennemi
        """
        global actual_sound_channel 

        if self.action == "idle":
            self.image = self.textures[0]

        elif self.action == "triggered":
            # attend 1 secondes avant de sortir
            self.trigger_cooldown += 1
            if self.trigger_cooldown // FPS == 1:
                self.animation_counter_fps = 1
                self.action = "going_out"
                # joue son going out
                pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "spike\\going_out.mp3")))
                actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1



        elif self.action == "going_out":
            self.animation_counter_fps += 1
            self.image = self.textures[self.animation_counter_fps // (FPS//spike_exit_speed)]

            if self.animation_counter_fps // (FPS//spike_exit_speed) == 5:
                self.action = "retrieve_still"
                self.trigger_cooldown = 0

        elif self.action == "retrieve_still":
            # attend 2 seconde en l'air
            self.trigger_cooldown += 1
            if self.trigger_cooldown // FPS == 2:
                self.action = "retrieving"
                # joue son going retrieving
                pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "spike\\retrieving.mp3")))
                actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1


        elif self.action == "retrieving":
            
            self.animation_counter_fps -= 1
            self.image = self.textures[self.animation_counter_fps // (FPS//spike_exit_speed)]

            if self.animation_counter_fps <= 1:
                self.action = "idle"
                self.animation_counter_fps = 1