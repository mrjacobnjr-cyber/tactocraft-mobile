import math
import random
import sys

try:
    import pygame
except Exception as exc:
    print("Pygame is required:", exc)
    raise

APP_TITLE = "Tactocraft Mobile"
WIDTH, HEIGHT = 1280, 720
FPS = 60

BG = (10, 14, 24)
PANEL = (22, 30, 50)
TEXT = (235, 242, 255)
MUTED = (140, 155, 180)
ACCENT = (80, 170, 255)
GOOD = (80, 220, 150)
WARN = (255, 196, 80)
DANGER = (255, 90, 90)


class Button:
    def __init__(self, rect, label):
        self.rect = pygame.Rect(rect)
        self.label = label

    def draw(self, screen, font, hover=False):
        color = (40, 70, 110) if hover else (32, 48, 78)
        pygame.draw.rect(screen, color, self.rect, border_radius=18)
        pygame.draw.rect(screen, ACCENT, self.rect, 2, border_radius=18)
        text = font.render(self.label, True, TEXT)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def hit(self, pos):
        return self.rect.collidepoint(pos)


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.r = 22
        self.speed = 5.5
        self.hp = 100
        self.score = 0

    def move(self, keys):
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
        self.x = max(self.r, min(WIDTH - self.r, self.x + dx * self.speed))
        self.y = max(self.r, min(HEIGHT - self.r, self.y + dy * self.speed))

    def draw(self, screen):
        pygame.draw.circle(screen, ACCENT, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(screen, (180, 230, 255), (int(self.x - 7), int(self.y - 7)), 6)


class Enemy:
    def __init__(self):
        side = random.choice([0, 1, 2, 3])
        if side == 0:
            self.x, self.y = -30, random.randint(0, HEIGHT)
        elif side == 1:
            self.x, self.y = WIDTH + 30, random.randint(0, HEIGHT)
        elif side == 2:
            self.x, self.y = random.randint(0, WIDTH), -30
        else:
            self.x, self.y = random.randint(0, WIDTH), HEIGHT + 30
        self.r = random.randint(14, 24)
        self.speed = random.uniform(1.2, 2.8)

    def update(self, player):
        dx, dy = player.x - self.x, player.y - self.y
        dist = max(1, math.hypot(dx, dy))
        self.x += dx / dist * self.speed
        self.y += dy / dist * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, DANGER, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(screen, (80, 10, 20), (int(self.x), int(self.y)), self.r, 2)


class Bullet:
    def __init__(self, x, y, tx, ty):
        self.x, self.y = x, y
        dx, dy = tx - x, ty - y
        dist = max(1, math.hypot(dx, dy))
        self.vx, self.vy = dx / dist * 11, dy / dist * 11
        self.r = 6

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def dead(self):
        return self.x < -40 or self.x > WIDTH + 40 or self.y < -40 or self.y > HEIGHT + 40

    def draw(self, screen):
        pygame.draw.circle(screen, WARN, (int(self.x), int(self.y)), self.r)


def draw_background(screen, tick):
    screen.fill(BG)
    for i in range(36):
        x = (i * 97 + tick * 0.25) % WIDTH
        y = (i * 53 + math.sin(tick * 0.02 + i) * 20) % HEIGHT
        pygame.draw.circle(screen, (18, 26, 44), (int(x), int(y)), 2)
    pygame.draw.rect(screen, (13, 20, 36), (0, HEIGHT - 110, WIDTH, 110))


def draw_hud(screen, font, small, player, wave):
    pygame.draw.rect(screen, PANEL, (24, 22, 420, 86), border_radius=18)
    screen.blit(font.render(APP_TITLE, True, TEXT), (44, 34))
    screen.blit(small.render(f"Score: {player.score}   HP: {player.hp}   Wave: {wave}", True, MUTED), (44, 72))
    pygame.draw.rect(screen, (50, 20, 25), (WIDTH - 324, 36, 280, 22), border_radius=8)
    pygame.draw.rect(screen, GOOD, (WIDTH - 324, 36, int(280 * player.hp / 100), 22), border_radius=8)
    screen.blit(small.render("Drag/tap to shoot. WASD/arrow keys to move.", True, MUTED), (WIDTH - 540, HEIGHT - 42))


def menu(screen, clock, fonts):
    title, font, small = fonts
    play = Button((WIDTH // 2 - 170, 390, 340, 72), "Start Game")
    quitb = Button((WIDTH // 2 - 170, 480, 340, 64), "Quit")
    tick = 0
    while True:
        tick += 1
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.hit(pos):
                    return True
                if quitb.hit(pos):
                    return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return True
        draw_background(screen, tick)
        screen.blit(title.render("TACTOCRAFT", True, TEXT), title.render("TACTOCRAFT", True, TEXT).get_rect(center=(WIDTH // 2, 230)))
        screen.blit(font.render("Mobile Alpha 8.8.8", True, ACCENT), font.render("Mobile Alpha 8.8.8", True, ACCENT).get_rect(center=(WIDTH // 2, 305)))
        play.draw(screen, font, play.hit(pos))
        quitb.draw(screen, font, quitb.hit(pos))
        pygame.display.flip()
        clock.tick(FPS)


def game_loop(screen, clock, fonts):
    title, font, small = fonts
    player = Player()
    enemies = []
    bullets = []
    spawn_timer = 0
    wave = 1
    tick = 0

    while True:
        tick += 1
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Bullet(player.x, player.y, mouse[0], mouse[1]))

        keys = pygame.key.get_pressed()
        player.move(keys)

        spawn_timer += 1
        limit = max(16, 50 - wave * 3)
        if spawn_timer >= limit:
            spawn_timer = 0
            enemies.append(Enemy())

        if player.score > wave * 120:
            wave += 1

        for e in enemies:
            e.update(player)
            if math.hypot(e.x - player.x, e.y - player.y) < e.r + player.r:
                player.hp -= 1

        for b in bullets:
            b.update()

        for e in enemies[:]:
            for b in bullets[:]:
                if math.hypot(e.x - b.x, e.y - b.y) < e.r + b.r:
                    enemies.remove(e)
                    bullets.remove(b)
                    player.score += 10
                    break

        bullets = [b for b in bullets if not b.dead()]
        enemies = [e for e in enemies if -80 < e.x < WIDTH + 80 and -80 < e.y < HEIGHT + 80]

        draw_background(screen, tick)
        for b in bullets:
            b.draw(screen)
        for e in enemies:
            e.draw(screen)
        player.draw(screen)
        draw_hud(screen, font, small, player, wave)

        if player.hp <= 0:
            over = title.render("GAME OVER", True, DANGER)
            info = font.render("Tap to return to menu", True, TEXT)
            screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                        waiting = False
                clock.tick(FPS)
            return True

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.set_caption(APP_TITLE)
    flags = pygame.SCALED
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    except Exception:
        screen = pygame.display.set_mode((960, 540))
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 72, bold=True)
    font = pygame.font.SysFont("arial", 30, bold=True)
    small = pygame.font.SysFont("arial", 22)
    fonts = (title, font, small)

    running = True
    while running:
        if not menu(screen, clock, fonts):
            break
        running = game_loop(screen, clock, fonts)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
