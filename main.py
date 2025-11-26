import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer Game")

WIDTH, HEIGHT = 1000, 800
FPS = 144
PLAYER_VEL = 3

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self, window):
        color = tuple(min(c + 50, 255) for c in self.color) if self.hovered else self.color
        pygame.draw.rect(window, color, self.rect)
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

def show_menu(window):
    play_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 60, "JUGAR")
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60, "SALIR")

    menu_running = True
    while menu_running:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        play_button.update(mouse_pos)
        quit_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_pos):
                    return True
                if quit_button.is_clicked(mouse_pos):
                    return False

        window.fill((30, 30, 30))
        font_title = pygame.font.Font(None, 72)
        title = font_title.render("PLATFORMER GAME", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(title, title_rect)

        play_button.draw(window)
        quit_button.draw(window)
        pygame.display.update()

def show_game_over_menu(window):
    restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 60, "REINTENTAR")
    menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60, "MENÚ")

    menu_running = True
    while menu_running:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        restart_button.update(mouse_pos)
        menu_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(mouse_pos):
                    return "restart"
                if menu_button.is_clicked(mouse_pos):
                    return "menu"

        window.fill((30, 30, 30))
        font_title = pygame.font.Font(None, 72)
        title = font_title.render("GAME OVER", True, (255, 0, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(title, title_rect)

        restart_button.draw(window)
        menu_button.draw(window)
        pygame.display.update()

def show_level_complete_menu(window, level_num=1):
    continue_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 60, "SIGUIENTE")
    menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60, "MENÚ")

    menu_running = True
    while menu_running:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        continue_button.update(mouse_pos)
        menu_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.is_clicked(mouse_pos):
                    return "continue"
                if menu_button.is_clicked(mouse_pos):
                    return "menu"

        window.fill((30, 30, 30))
        font_title = pygame.font.Font(None, 72)
        title = font_title.render("NIVEL COMPLETADO", True, (0, 255, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(title, title_rect)
        
        level_text = pygame.font.Font(None, 48)
        level_display = level_text.render(f"Nivel {level_num}", True, (255, 255, 255))
        level_rect = level_display.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        window.blit(level_display, level_rect)

        continue_button.draw(window)
        menu_button.draw(window)
        pygame.display.update()


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.image = None
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.dash_active = False
        self.dash_velocity = 0
        self.dash_count = 0
        self.lives = 5
        self.wall_slide = False

    def make_dash(self):
        if not self.dash_active:
            self.dash_active = True
            self.dash_count = 0
            dash_direction = 1 if self.direction == "right" else -1
            self.dash_velocity = 128 * dash_direction

    def update_wall_slide(self, is_colliding_with_wall):
        if is_colliding_with_wall and self.y_vel > 0:
            self.wall_slide = True
            self.y_vel = min(self.y_vel, 2)
        else:
            self.wall_slide = False

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        if not self.hit:
            self.hit = True
            self.hit_count = 0
            if self.lives > 0:
                self.lives -= 1

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        
        if self.dash_active:
            self.dash_count += 1
            if self.dash_count > fps // 4:
                self.dash_active = False
                self.dash_velocity = 0
            self.move(self.dash_velocity / (fps // 6), 0)
        else:
            self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > 1:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height,):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.ask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False
        self.name = "collectible"
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        try:
            fruit_path = join("assets", "Items", "Fruits", "Strawberry.png")
            if isfile(fruit_path):
                loaded_image = pygame.image.load(fruit_path).convert_alpha()
                self.image = pygame.transform.scale(loaded_image, (width, height))
            else:
                # Si no existe, dibujar un círculo
                pygame.draw.circle(self.image, (255, 0, 0), (width // 2, height // 2), width // 2)
        except Exception as e:
            # Fallback: dibujar un círculo rojo
            pygame.draw.circle(self.image, (255, 0, 0), (width // 2, height // 2), width // 2)
        
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        if not self.collected:
            win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

def get_background_image(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_image, player, objects, offset_x, collectibles=None, current_level=1):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    # Dibujar coleccionables
    if collectibles:
        for collectible in collectibles:
            collectible.draw(window, offset_x)

    player.draw(window, offset_x)
    
    # Mostrar información del juego
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Vidas: {player.lives}", True, (255, 0, 0))
    window.blit(lives_text, (10, 10))
    
    level_text = font.render(f"Nivel: {current_level}", True, (0, 255, 0))
    window.blit(level_text, (10, 50))
    
    # Mostrar coleccionables recolectados
    collectibles_collected = sum(1 for c in collectibles if c.collected) if collectibles else 0
    collectibles_total = len(collectibles) if collectibles else 0
    collectibles_text = font.render(f"Frutas: {collectibles_collected}/{collectibles_total}", True, (255, 215, 0))
    window.blit(collectibles_text, (10, 90))

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)
    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire" and not player.hit:
            player.make_hit()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background_image("Blue.png")

    block_size = 96
    current_level = 1
    
    def setup_level(level_num):
        player = Player(100, 100, 50, 50)
        
        floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
        
        # Rediseño del nivel con más plataformas - Nivel 1
        if level_num == 1:
            platforms = [
                Block(0, HEIGHT - block_size * 2, block_size),
                Block(block_size * 3, HEIGHT - block_size * 4, block_size),
                Block(block_size * 6, HEIGHT - block_size * 3, block_size * 2),
                Block(block_size * 9, HEIGHT - block_size * 5, block_size),
                Block(block_size * 12, HEIGHT - block_size * 3, block_size * 2),
                Block(block_size * 15, HEIGHT - block_size * 6, block_size),
            ]
            
            # Fuegos posicionados sobre las plataformas
            fires = [
                Fire(block_size * 0.5, HEIGHT - block_size * 2.5, 16, 32),
                Fire(block_size * 3.5, HEIGHT - block_size * 4.5, 16, 32),
                Fire(block_size * 9.5, HEIGHT - block_size * 5.5, 16, 32),
            ]
            for fire in fires:
                fire.on()
            
            # Coleccionables
            collectibles = [
                Collectible(block_size * 1.5, HEIGHT - block_size * 3 - 40, 40, 40),
                Collectible(block_size * 5, HEIGHT - block_size * 4 - 40, 40, 40),
                Collectible(block_size * 10, HEIGHT - block_size * 6 - 40, 40, 40),
                Collectible(block_size * 14, HEIGHT - block_size * 4 - 40, 40, 40),
            ]
        
        # Nivel 2 - Más difícil
        elif level_num == 2:
            platforms = [
                Block(block_size * 1.5, HEIGHT - block_size * 3, block_size),
                Block(block_size * 4, HEIGHT - block_size * 5, block_size),
                Block(block_size * 7, HEIGHT - block_size * 4, block_size * 1.5),
                Block(block_size * 10, HEIGHT - block_size * 6, block_size),
                Block(block_size * 13, HEIGHT - block_size * 4, block_size * 1.5),
                Block(block_size * 16, HEIGHT - block_size * 7, block_size),
            ]
            
            fires = [
                Fire(block_size * 2, HEIGHT - block_size * 3.5, 16, 32),
                Fire(block_size * 4.5, HEIGHT - block_size * 5.5, 16, 32),
                Fire(block_size * 10.5, HEIGHT - block_size * 6.5, 16, 32),
                Fire(block_size * 13.5, HEIGHT - block_size * 4.5, 16, 32),
            ]
            for fire in fires:
                fire.on()
            
            collectibles = [
                Collectible(block_size * 2, HEIGHT - block_size * 3 - 40, 40, 40),
                Collectible(block_size * 5, HEIGHT - block_size * 5 - 40, 40, 40),
                Collectible(block_size * 8, HEIGHT - block_size * 4 - 40, 40, 40),
                Collectible(block_size * 11, HEIGHT - block_size * 6 - 40, 40, 40),
                Collectible(block_size * 15, HEIGHT - block_size * 4 - 40, 40, 40),
            ]
        
        # Nivel 3 - Muy difícil
        elif level_num == 3:
            platforms = [
                Block(block_size * 0.5, HEIGHT - block_size * 2, block_size * 0.8),
                Block(block_size * 2.5, HEIGHT - block_size * 4, block_size * 0.8),
                Block(block_size * 4.5, HEIGHT - block_size * 3, block_size * 0.8),
                Block(block_size * 6.5, HEIGHT - block_size * 5, block_size * 0.8),
                Block(block_size * 8.5, HEIGHT - block_size * 4, block_size),
                Block(block_size * 11, HEIGHT - block_size * 6, block_size * 0.8),
                Block(block_size * 13, HEIGHT - block_size * 3, block_size),
                Block(block_size * 15.5, HEIGHT - block_size * 7, block_size * 0.8),
            ]
            
            fires = [
                Fire(block_size * 1, HEIGHT - block_size * 2.5, 16, 32),
                Fire(block_size * 3, HEIGHT - block_size * 4.5, 16, 32),
                Fire(block_size * 5, HEIGHT - block_size * 3.5, 16, 32),
                Fire(block_size * 7, HEIGHT - block_size * 5.5, 16, 32),
                Fire(block_size * 9, HEIGHT - block_size * 4.5, 16, 32),
                Fire(block_size * 12, HEIGHT - block_size * 6.5, 16, 32),
            ]
            for fire in fires:
                fire.on()
            
            collectibles = [
                Collectible(block_size * 0.5, HEIGHT - block_size * 2 - 40, 40, 40),
                Collectible(block_size * 3, HEIGHT - block_size * 4 - 40, 40, 40),
                Collectible(block_size * 5, HEIGHT - block_size * 3 - 40, 40, 40),
                Collectible(block_size * 7, HEIGHT - block_size * 5 - 40, 40, 40),
                Collectible(block_size * 9, HEIGHT - block_size * 4 - 40, 40, 40),
                Collectible(block_size * 12, HEIGHT - block_size * 6 - 40, 40, 40),
            ]
        
        solid_objects = [*floor, *platforms, *fires]
        return player, solid_objects, collectibles
    
    player, objects, collectibles = setup_level(current_level)
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_c:
                    player.make_dash()

        # Verificar si el jugador perdió todas las vidas
        if player.lives <= 0:
            result = show_game_over_menu(window)
            if result == "restart":
                player, objects, collectibles = setup_level(current_level)
                offset_x = 0
            elif result == "menu":
                return
            else:
                run = False

        player.loop(FPS)
        
        # Loop para todos los fuegos
        for obj in objects:
            if isinstance(obj, Fire):
                obj.loop()
        
        # Detectar colisiones con coleccionables
        for collectible in collectibles:
            if not collectible.collected and pygame.sprite.collide_mask(player, collectible):
                collectible.collected = True
        
        # Verificar si se completó el nivel
        all_collected = all(c.collected for c in collectibles) if collectibles else False
        if all_collected:
            result = show_level_complete_menu(window, current_level)
            if result == "continue":
                current_level += 1
                if current_level > 3:
                    current_level = 1
                player, objects, collectibles = setup_level(current_level)
                offset_x = 0
            else:
                return
        
        # Detectar colisión con paredes para wall slide
        wall_collide_left = collide(player, objects, -5)
        wall_collide_right = collide(player, objects, 5)
        player.update_wall_slide(wall_collide_left or wall_collide_right)
        
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, collectibles, current_level)

        if(
            (player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0
            ):
            offset_x += player.x_vel

    pygame.quit()
    quit()

if __name__ == "__main__":
    if show_menu(window):
        main(window)