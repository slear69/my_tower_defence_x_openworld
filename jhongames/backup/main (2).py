
# /// script
# dependencies = ["pytmx"]
# ///
import random
import time
import pygame
from pathlib import Path
import asyncio
from draw_map import load_map_tmx, load_path


pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1520, 820))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.plantnum = 1
        
        self.move_down = 10
        self.move_right = 10 
        self.map_sprites, self.place_rects = load_map_tmx("test.tmx", self.move_right, self.move_down, "Tile Layer 1", object_layer_names=("place",))
        self.paths = load_path("test.tmx", self.move_right, self.move_down)
        # Stores the IDs of place objects that have been clicked.
        self.first_obj = set()
        self.second_obj = set()
        self.therd_obj = set()
        self.monh = 500


        self.remove = False

        # Load the path for the enemy to follow and create an enemy instance
        self.path = load_path("test.tmx", self.move_right, self.move_down)
        self.enemys = []
        self.dalay = 2
        self.spawn_time = 0
        self.emys_spw=5
        self.enemy_image = pygame.image.load("enemy.png").convert_alpha()

    def taken(self,object): 
        if object in self.first_obj or object in self.second_obj or object in self.therd_obj:
            return True
        else:
            return False

    def spawn_enemy(self):
        random_enemy = random.randint(1,5)
        match random_enemy:
            case 1:
                e = enemy(random.choice(self.path) , self.enemy_image , False ,speed=25)
            case 2:
                e = enemy(random.choice(self.path) , self.enemy_image , False ,speed=40)
            case 3:
                e = enemy(random.choice(self.path) , self.enemy_image, True , speed=40)
            case 4:
                e = enemy(random.choice(self.path) , self.enemy_image, True , speed=20)
            case 5:
                e = enemy(random.choice(self.path) , self.enemy_image , False ,speed=25)

        
        self.enemys.append(e)
        return e
    def moneh(self):
        color = (255, 255, 255)
        pos = (1360,10)
        font = pygame.font.Font(None, 36)

        text = font.render(f"Money: {self.monh}", True, color)
        self.screen.blit(text, pos)

    def remove_plant(self, event):
        for object_id, rect in self.place_rects.items():
            if rect.collidepoint(event.pos) and self.taken(object_id):
                self.first_obj.discard(object_id)
                self.second_obj.discard(object_id)
                self.therd_obj.discard(object_id)
                self.remove_mode = False      # turn the tool off after one use
                return
    
    def platype(self, screen, plant, position):
        if plant == 1:
            pimage = pygame.image.load("BLOCK.png").convert_alpha()
            prect = pimage.get_rect(topleft=position)
            screen.blit(pimage, prect)
            return prect
        if plant == 2:
            gimage = pygame.image.load("GREEN.png").convert_alpha()
            grect = gimage.get_rect(topleft=position)
            screen.blit(gimage, grect)
            return grect
        if plant == 3 :
            yimage = pygame.image.load("yellow.png").convert_alpha()
            yrect = yimage.get_rect(topleft=position)
            screen.blit(yimage, yrect)
            return yrect


    def load_stuff(self, event):
        for object_id, rect in self.place_rects.items():
            # Mark the clicked object's ID so it will be drawn purple.
            if rect.collidepoint(event.pos):
                if self.taken(object_id):
                    return False
                elif self.plantnum == 0 and self.monh >= 500:
                    self.first_obj.add(object_id)
                    self.monh -= 100
                elif self.plantnum == 1 and self.monh >= 100:
                    self.second_obj.add(object_id)
                    self.monh -= 100
                elif self.plantnum == 2 and self.monh >= 200:
                    self.therd_obj.add(object_id)
                    self.monh -= 200
                else:
                    pass
     
    def events(self):
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.load_stuff(event)
                self.prect = self.platype(self.screen, 2, (200, 700))
                self.grect = self.platype(self.screen, 1, (100, 700))
                self.yrect = self.platype(self.screen, 3, (50, 700))
                if self.yrect.collidepoint(event.pos):
                    self.remove = not self.remove
                if self.prect.collidepoint(event.pos):
                    self.plantnum=1
                    self.remove = False
                if self.grect.collidepoint(event.pos):
                    self.plantnum=2
                    self.remove = False
                    print("Clicked on the green rectangle!")
                elif self.remove:
                    self.remove_plant(event) 

                    
    def update(self, dt):
        if self.emys_spw > 0:
            self.spawn_time += dt
            if self.spawn_time >= self.dalay:
                self.spawn_time -= self.dalay
                self.spawn_enemy()
                self.emys_spw -= 1
        for e in self.enemys:
            enem_plant = self.enemy_onplant(e)
            if enem_plant is None:
                e.stoped = False
                e.eat = 0
                e.update(dt)
            else :
                e.stoped = True
                e.eat += dt
                if e.eat >= 5:
                    self.first_obj.discard(enem_plant)
                    self.second_obj.discard(enem_plant)
                    self.therd_obj.discard(enem_plant)
                    e.eat=0
    
    def enemy_onplant(self, e):
        if e.flying:
            return None
        for plant,rect in self.place_rects.items():
            if e.rect.colliderect(rect) and self.taken(plant):
                return plant
        return None
    # remove ones that finished

    def render(self):
        self.screen.fill("blue")
        self.map_sprites.draw(self.screen)
        self.platype(self.screen, 1 ,(100, 700))
        self.platype(self.screen, 2 ,(200, 700))
        self.platype(self.screen, 3 ,(50, 700) )
        self.moneh()
        # Draw clicked place-object rectangles in purple over the tile map.
        for object_id in self.therd_obj:
            rect = self.place_rects[object_id]
            self.screen.blit(pygame.image.load("BLOCKK.png").convert_alpha(),(rect.x,rect.y))
        for object_id in self.second_obj:
            rect = self.place_rects[object_id]
            self.screen.blit(pygame.image.load("GREENN.png").convert_alpha(),(rect.x,rect.y))
        for object_id in self.first_obj:
            rect = self.place_rects[object_id]
            self.screen.blit(pygame.image.load("pea.png").convert_alpha(), (rect.x, rect.y))
        for e in self.enemys:
            e.draw(self.screen)
        pygame.display.flip()
        

    async def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.events()
            self.update(dt)
            self.render()
            await asyncio.sleep(0)   # lets the browser breathe; required
        pygame.quit()

class enemy:
    def __init__(self, path,image,tag_fly,speed=40):
        self.flying = tag_fly
        self.eat = 0
        self. path = path
        self.image = image
        self.speed=speed
        self.pos = pygame.Vector2(path  [0])
        self.target_index = 1
        self.end = False
        self.rect = self.image.get_rect(center=self.pos)
        self.stoped = False
    # updates the position of the enemy along the path based on the speed and time delta
    def update(self,dt):
        if self.target_index >= len(self.path):
            self.end = True
            return
        goal = pygame.Vector2(self.path[self.target_index])
        goal_distance = goal - self.pos
        step = self.speed * dt
        if goal_distance.length()< step:
            self.pos = goal
            self.target_index += 1
        else:
            self.pos += goal_distance.normalize() * step
        self.rect.center = round(self.pos.x), round(self.pos.y)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

async def main():
    game = Game()
    await game.run()

asyncio.run(main())
