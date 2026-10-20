import pygame
 
 
class Bullet:
    def __init__(self, pos, target):
        self.pos = pygame.Vector2(pos)
        self.vel = (pygame.Vector2(target) - self.pos).normalize() * 300
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.center = pos
        self.alive = True
 
    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)
 
    def draw(self, screen):
        pygame.draw.circle(screen, (120, 255, 120), self.rect.center, 5)
 
 
class Plant:
    def __init__(self, rect, image, shoots=False):
        self.rect = rect
        self.image = image
        self.shoots = shoots
        self.timer = 0
 
    def update(self, dt, enemys, bullets):
        if not self.shoots or not enemys:
            return
        self.timer += dt
        if self.timer >= 1:      # shoots once per second
            self.timer = 0
            nearest = min(enemys, key=lambda e: pygame.Vector2(e.rect.center).distance_to(self.rect.center))
            bullets.append(Bullet(self.rect.center, nearest.rect.center))
 
    def draw(self, screen):
        screen.blit(self.image, self.rect)
 