
# /// script
# dependencies = ["pytmx"]
# ///

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
        self.map = Path(__file__).resolve().parent / "test.tmx"
        self.map_sprites, self.place_rects = load_map_tmx(str(self.map),self.move_right,self.move_down,"Tile Layer 1",object_layer_names=("place",),)
        # Stores the IDs of place objects that have been clicked.
        self.first_obj = set()
        self.second_obj = set()
        self.therd_obj = set()
        self.monh = 500

        self.path = load_path(str(self.map), self.move_right, self.move_down)



    def taken(self,object):
        if object in self.first_obj or object in self.second_obj or object in self.therd_obj:
            return True
        else:
            return False

    def moneh(self):
        color = (255, 255, 255)
        pos = (1360,10)
        font = pygame.font.Font(None, 36)

        text = font.render(f"Money: {self.monh}", True, color)
        self.screen.blit(text, pos)
    
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
                if self.prect.collidepoint(event.pos):
                    self.plantnum=1
                if self.grect.collidepoint(event.pos):
                    self.plantnum=2
                    print("Clicked on the green rectangle!")
                    
    def update(self, dt):
        pass

    # move

    # remove ones that finished

    def render(self):
        self.screen.fill("blue")
        self.map_sprites.draw(self.screen)
        self.platype(self.screen, 1 ,(100, 700))
        self.platype(self.screen, 2 ,(200, 700))
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
    def __init__(self, path,image, speed=40):
        self. path = path
        self.image = image
        self.speed=speed
        self.pos = pygame.Vector2(path[0])
        self.target_index = 1
        self.end = False

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
