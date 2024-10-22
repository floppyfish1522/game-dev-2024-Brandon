import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = 10
HOOK_DISTANCE = 200

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player Class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - 100, 50, 50)
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        if not self.on_ground:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.on_ground = True
            self.velocity_y = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

# Grappling Hook Class
class GrapplingHook:
    def __init__(self):
        self.active = False
        self.position = None

    def activate(self, player_pos):
        self.active = True
        self.position = player_pos

    def update(self, player):
        if self.active:
            dx = self.position[0] - player.rect.centerx
            dy = self.position[1] - player.rect.centery
            distance = math.hypot(dx, dy)

            if distance > 0:
                player.rect.x += dx / distance * 5
                player.rect.y += dy / distance * 5

            if distance < 10:
                self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.line(screen, GREEN, (player.rect.centerx, player.rect.centery), self.position, 2)

# Main Game Loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    hook = GrapplingHook()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_g:
                    hook.activate((player.rect.centerx + HOOK_DISTANCE, player.rect.centery))

        player.update()
        hook.update(player)

        player.draw(screen)
        hook.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
