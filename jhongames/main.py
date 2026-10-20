
# /// script
# dependencies = ["pytmx"]
# ///
import random
from os.path import join
from plant import Plant
from plantmony import growplant 
import pygame
import asyncio
from draw_map import load_map_tmx, load_path


pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1520, 820))
        self.clock = pygame.time.Clock()
        self.running = True

        # plant stuff
        self.seeds = 5
        self.plantnum = 1
        self.plants = {}
        self.bullets = []
        self.block_btn_img = pygame.image.load(join("assets", "BLOCK.png")).convert_alpha()
        self.green_btn_img = pygame.image.load(join("assets", "GREEN.png")).convert_alpha()
        self.yellow_btn_img = pygame.image.load(join("assets", "yellow.png")).convert_alpha()
        self.seed_btn = pygame.image.load(join("assets" , "red.png")).convert_alpha()
        self.green_img = pygame.image.load(join("assets", "GREENN.png")).convert_alpha()
        self.block_img = pygame.image.load(join("assets", "BLOCKK.png")).convert_alpha()

        # map stuff
        self.move_down = 10
        self.move_right = 10 
        self.move_Gdown = 500
        self.move_Gright = 1200 
        self.map_sprites, self.place_rects = load_map_tmx(join("assets", "test.tmx"), self.move_right, self.move_down, "Tile Layer 1", object_layer_names=("place",))        
        self.gaurd_sprite, self.gaurd_rect = load_map_tmx(join("assets", "gradina2.tmx"), self.move_Gright, self.move_Gdown, "Tile Layer 1",object_layer_names=("PLACESG",) )   
        
        # Stores the IDs of place objects that have been clicked.
        #money stuff
        self.monh = 500
        self.gaurd_plant = { obj_id: growplant(rect,self.green_img,0)
                            for obj_id , rect in self.gaurd_rect.items()}
        self.remove = False

        # Load the path for the enemy to follow and create an enemy instance 
        # enemy stuff
        self.path = load_path(join("assets", "test.tmx"), self.move_right, self.move_down)
        self.enemys = []
        self.dalay = 2
        self.spawn_time = 0
        self.emys_spw=5
        self.enemy_image = pygame.image.load(join("assets", "enemy.png")).convert_alpha()

    def taken(self,object): 
        return object in self.plants

    def spawn_enemy(self):
        random_enemy = random.randint(1,5)
        match random_enemy:
            case 1:
                e = enemy(random.choice(self.path) , self.enemy_image , False,10 ,speed=25)
            case 2:
                e = enemy(random.choice(self.path) , self.enemy_image , False,10 ,speed=40)
            case 3:
                e = enemy(random.choice(self.path) , self.enemy_image, True , 10 ,speed=30)
            case 4:
                e = enemy(random.choice(self.path) , self.enemy_image, True ,10 ,speed=20)
            case 5:
                e = enemy(random.choice(self.path) , self.enemy_image , False,10 ,speed=25)

        
        self.enemys.append(e)
        return e
    def draw_txt(self,colore,position , txt , type):
        color = colore
        pos = position
        font = pygame.font.Font(None, 36)

        text = font.render(f"{type}: {txt}",False, color)
        self.screen.blit(text, pos)

    def remove_plant(self, event):
        for object_id, rect in self.place_rects.items():
            if rect.collidepoint(event.pos) and self.taken(object_id):
                self.plants.pop(object_id)
                self.remove_mode = False      # turn the tool off after one use
                return
    
    def platype(self, screen, plant, position):
        if plant == 1:
            pimage = self.block_btn_img
            prect = pimage.get_rect(topleft=position)
            screen.blit(pimage, prect)
            return prect
        if plant == 2:
            gimage = self.green_btn_img
            grect = gimage.get_rect(topleft=position)
            screen.blit(gimage, grect)
            return grect
        if plant == 3 :
            yimage =self.yellow_btn_img
            yrect = yimage.get_rect(topleft=position)
            screen.blit(yimage, yrect)
            return yrect
        if plant == 4 :
            rimage = self.seed_btn
            rrect = rimage.get_rect(topleft=position)
            screen.blit(rimage, rrect)
            return rrect


    def load_stuff(self, event):
        for object_id, rect in self.place_rects.items():
            # Mark the clicked object's ID so it will be drawn purple.
            if rect.collidepoint(event.pos):
                if self.taken(object_id):
                    return False
                elif self.plantnum == 0 and self.monh >= 500:
                    self.plants[object_id] = Plant(rect , self.green_img,shoots=True)
                    self.monh -= 100
                elif self.plantnum == 1 and self.monh >= 100:
                    self.plants[object_id] = Plant(rect , self.green_img,shoots=True)
                    self.monh -= 100
                elif self.plantnum == 2 and self.monh >= 200:
                    self.plants[object_id] = Plant(rect , self.green_img,shoots=True)
                    self.monh -= 200
        for mone_obj , rectg in self.gaurd_rect.items():
            if rectg.collidepoint(event.pos) :
                g = self.gaurd_plant[mone_obj]
                
                if g.grown:
                    self.monh += 50
                    g.collected()
                elif not g.planted and self.seeds > 0:
                    g.plant()
                    self.seeds -= 1
        
     
    def events(self):
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.load_stuff(event)
                self.prect = self.platype(self.screen, 2, (200, 700))
                self.grect = self.platype(self.screen, 1, (100, 700))
                self.yrect = self.platype(self.screen, 3, (0, 700))
                self.rrect = self.platype(self.screen, 4, (300, 700))
                if self.yrect.collidepoint(event.pos):
                    self.remove = not self.remove
                if self.prect.collidepoint(event.pos):
                    self.plantnum=1
                    self.remove = False
                if self.grect.collidepoint(event.pos):
                    self.plantnum=2
                    self.remove = False
                    print("Clicked on the green rectangle!")
                if self.rrect.collidepoint(event.pos) and self.monh > 0:
                    self.seeds += 1
                    self.monh -= 25
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
                e.eat = 0
                e.update(dt)
            else:
                e.eat += dt
                if e.eat >= 5:
                    self.plants.pop(enem_plant, None)
                    e.eat = 0
        self.enemys = [e for e in self.enemys if not e.end]

        for plant in self.plants.values():
            plant.update(dt, self.enemys, self.bullets)

        for b in self.bullets:
            b.update(dt)
            for e in self.enemys:
                if b.rect.colliderect(e.rect):
                    e.hp -= 1
                    b.alive = False
                    break

        self.bullets = [b for b in self.bullets
                        if b.alive and self.screen.get_rect().contains(b.rect)]
        self.enemys = [e for e in self.enemys if not e.end and e.hp > 0]  

        for plant_grow in self.gaurd_plant.values():
            plant_grow.update()


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
        self.gaurd_sprite.draw(self.screen)
        self.platype(self.screen, 1 ,(100, 700))
        self.platype(self.screen, 2 ,(200, 700))
        self.platype(self.screen, 3 ,(50, 700) )
        self.platype(self.screen, 4, (300, 700))
        self.draw_txt((255,255,255),(1370,200),self.monh , "money")
        self.draw_txt((255,255,255),(1370,100),self.seeds , "seeds")
        # Draw clicked place-object rectangles in purple over the tile map.
        for plant in self.plants.values():
            plant.draw(self.screen)
        for enemy in self.enemys:
            enemy.draw(self.screen)
        for bulets in self.bullets:
            bulets.draw(self.screen)
        for g in self.gaurd_plant.values():
            g.draw(self.screen,self.block_img)

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
    def __init__(self, path,image,tag_fly,hp,speed=40):
        self.flying = tag_fly
        self.eat = 0
        self.hp = hp
        self. path = path
        self.image = image
        self.speed=speed
        self.pos = pygame.Vector2(path  [0])
        self.target_index = 1
        self.end = False
        self.rect = self.image.get_rect(center=self.pos)
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
