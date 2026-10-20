import pytmx.util_pygame  
import pygame



def load_map_tmx(filename, pos, posy, *tile_layer_names, object_layer_names=()):
    spritegroup = AllSprites()
    tmx_map = pytmx.load_pygame(filename)
    object_rects = {}
    for layer_name in tile_layer_names:
        for x, y, image in tmx_map.get_layer_by_name(layer_name).tiles():
            Sprite((x * tmx_map.tilewidth + pos, y * tmx_map.tileheight + posy),image,spritegroup,)

    for layer_name in object_layer_names:
        for obj in tmx_map.get_layer_by_name(layer_name):
            if obj.width > 0 and obj.height > 0:
                object_rects[obj.id] = pygame.Rect(obj.x + pos,obj.y + posy,obj.width,obj.height,)

    return spritegroup, object_rects

def load_path(filename, offsetx, offsety, prefix="path"):
    tmx_map = pytmx.load_pygame(filename)
    path = []
    for layer in tmx_map.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.startswith(prefix):
            points=sorted(layer , key=lambda o: o.id)
            if len (points) >= 2:
                path.append([(o.x + offsetx , o.y + offsety) for o in points])
    return path
    

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_sprite = pygame.display.get_surface()
