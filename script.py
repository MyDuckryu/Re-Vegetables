import pygame
import sys
import os
import random
import math

# 1. Initialization
pygame.init()

# 2. Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Re:Vegetables")

# 3. Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 150, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 80, 0)
LIGHT_GRAY = (192, 192, 192)

# 4. Font Loading (Using default font)
title_font = pygame.font.Font(None, 80)
story_font = pygame.font.Font(None, 30)
button_font = pygame.font.Font(None, 40)

# 5. Load Background Image
try:
    current_dir = os.path.dirname(__file__)
    background_path = os.path.join(current_dir, "assets", "images", "background.png")
    background_image = pygame.image.load(background_path).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_image = None


# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


# Function to draw a button with RPG style
def draw_button(surface, rect, color, text, font, text_color):
    # Darker shade for the button's border
    darker_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))
    # Lighter shade for the button's highlight
    lighter_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))

    # Draw the main button body
    pygame.draw.rect(surface, darker_color, rect, border_radius=12)

    # Draw a slightly smaller rect for the main face of the button, creating a border effect
    inner_rect = rect.inflate(-6, -6)
    pygame.draw.rect(surface, color, inner_rect, border_radius=9)

    # Check for hover state
    if rect.collidepoint(pygame.mouse.get_pos()):
        hover_rect = inner_rect.inflate(2, 2)
        pygame.draw.rect(surface, lighter_color, hover_rect, border_radius=9)

    draw_text(text, font, text_color, surface, rect.centerx, rect.centery)


# Function to draw wrapped text
def draw_wrapped_text(text, font, color, surface, x, y, max_width):
    words = text.split(' ')
    wrapped_lines = []
    current_line = ''
    for word in words:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            if current_line:
                current_line += ' ' + word
            else:
                current_line = word
        else:
            wrapped_lines.append(current_line)
            current_line = word
    wrapped_lines.append(current_line)
    line_y = y
    line_height = font.get_linesize()
    for line in wrapped_lines:
        text_obj = font.render(line, True, color)
        text_rect = text_obj.get_rect(center=(x, line_y))
        surface.blit(text_obj, text_rect)
        line_y += line_height


# Fade effect function
def fade_out_in(fade_speed=5):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fade out
    for alpha in range(0, 256, fade_speed):
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

    # Fade in
    for alpha in range(255, -1, -fade_speed):
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)


# Function to draw a lightning bolt
def draw_lightning(surface, color, start_pos, end_pos, segments=5):
    points = [start_pos]

    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]

    for i in range(1, segments):
        x = start_pos[0] + (dx * i / segments) + random.randint(-20, 20)
        y = start_pos[1] + (dy * i / segments) + random.randint(-20, 20)
        points.append((x, y))

    points.append(end_pos)

    pygame.draw.lines(surface, color, False, points, 5)


# ** ฟังก์ชันใหม่: วาดเอฟเฟกต์การโจมตี **
def draw_attack_effect(surface, effect_type, start_pos, end_pos, elapsed_time, duration):
    # ปรับปรุงค่า alpha และขนาดของเอฟเฟกต์ตามเวลา
    alpha = int(255 * (1 - (elapsed_time / duration)))

    # สร้างพื้นผิวโปร่งใสสำหรับเอฟเฟกต์
    effect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    if effect_type == "light":
        # Light Attack: เส้นสั้น
        length = int(50 * (elapsed_time / duration))
        width = int(5 * (elapsed_time / duration))
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        x2 = start_pos[0] + length * math.cos(angle)
        y2 = start_pos[1] + length * math.sin(angle)
        pygame.draw.line(effect_surface, (255, 255, 255, alpha), start_pos, (x2, y2), width)

    elif effect_type == "heavy":
        # Heavy Attack: เส้นยาว
        length = int(150 * (elapsed_time / duration))
        width = int(10 * (elapsed_time / duration))
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        x2 = start_pos[0] + length * math.cos(angle)
        y2 = start_pos[1] + length * math.sin(angle)
        pygame.draw.line(effect_surface, (255, 255, 255, alpha), start_pos, (x2, y2), width)

    # วาดพื้นผิวเอฟเฟกต์ลงบนหน้าจอหลัก
    surface.blit(effect_surface, (0, 0))


# Shop screen function
def shop_screen(player):
    message = ""
    message_time = 0
    message_duration = 2000

    item_width = 300
    item_height = 60
    gap = 50
    start_x = (SCREEN_WIDTH - (item_width * 2 + gap)) / 2
    start_y = SCREEN_HEIGHT / 2 - 100

    items = [
        {"name": "Sword", "price": 100, "effect": "dmg",
         "rect": pygame.Rect(start_x, start_y, item_width, item_height)},
        {"name": "Potion", "price": 50, "effect": "hp",
         "rect": pygame.Rect(start_x + item_width + gap, start_y, item_width, item_height)},
        {"name": "Leather Armor", "price": 56, "effect": "dr_5",
         "rect": pygame.Rect(start_x, start_y + item_height + gap, item_width, item_height)},
        {"name": "Steel Armor", "price": 1500, "effect": "dr_20",
         "rect": pygame.Rect(start_x + item_width + gap, start_y + item_height + gap, item_width, item_height)},
    ]

    back_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT * 0.9 - 30, 200, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return

                for item in items:
                    if item["rect"].collidepoint(event.pos):
                        if player.money >= item["price"]:
                            player.money -= item["price"]
                            if item["effect"] == "dmg":
                                player.base_damage += 30
                                message = "Sword purchased! Damage +30"
                            elif item["effect"] == "hp":
                                player.potions += 1
                                message = "Potion purchased! Potions +1"
                            elif item["effect"] == "dr_5":
                                player.damage_reduction = 0.05
                                message = "Leather Armor purchased! Damage reduction: 5%"
                            elif item["effect"] == "dr_20":
                                player.damage_reduction = 0.20
                                message = "Steel Armor purchased! Damage reduction: 20%"

                            message_time = pygame.time.get_ticks()
                        else:
                            message = "Not enough money!"
                            message_time = pygame.time.get_ticks()

        screen.fill(BLACK)
        draw_text("Shop", title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

        money_text = button_font.render(f"Money: {player.money}", True, YELLOW)
        money_rect = money_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(money_text, money_rect)

        for item in items:
            draw_button(screen, item["rect"], GRAY, f"{item['name']} ({item['price']})", story_font, WHITE)

        draw_button(screen, back_button_rect, GRAY, "Back", button_font, WHITE)

        if message and pygame.time.get_ticks() - message_time < message_duration:
            draw_text(message, story_font, GOLD, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8)

        pygame.display.flip()


class Firefly:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = SCREEN_HEIGHT + random.randint(0, 50)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2.0)
        self.color = ORANGE
        self.alpha = random.randint(100, 200)

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (self.color[0], self.color[1], self.color[2], self.alpha), (self.size, self.size),
                           self.size)
        surface.blit(s, (self.x, self.y))


def start_screen():
    text = "Re:Vegetables"
    text_width, text_height = title_font.size(text)
    base_x = (SCREEN_WIDTH - text_width) / 2
    base_y = SCREEN_HEIGHT / 4

    fireflies = []

    while True:
        start_button_text = button_font.render("Start Game", True, BLACK)
        start_button_rect = start_button_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return

        # Add new fireflies
        if random.random() < 0.2:
            fireflies.append(Firefly())

        # Update and draw fireflies
        screen.fill(DARK_GREEN)
        for firefly in fireflies:
            firefly.update()
            firefly.draw(screen)

        # Remove fireflies that are off-screen
        fireflies = [f for f in fireflies if f.y > -10]

        current_x = base_x
        for i, char in enumerate(text):
            char_surface = title_font.render(char, True, WHITE)
            char_width, char_height = title_font.size(char)

            wave_speed = 0.005
            wave_amplitude = 8
            offset = wave_amplitude * math.sin(wave_speed * pygame.time.get_ticks() + i * 0.5)

            char_y = base_y + offset
            char_rect = char_surface.get_rect(center=(current_x + char_width / 2, char_y))
            screen.blit(char_surface, char_rect)
            current_x += char_width

        draw_button(screen, start_button_rect, WHITE, "Start Game", button_font, BLACK)

        pygame.display.flip()


def story_screen():
    story_lines = [
        "When your eyes open again...",
        "You find yourself no longer in the same world.",
        "And most importantly... you are no longer human.",
        "You are a small seed that has just broken free from its shell.",
        "In a new world full of danger,",
        "You must grow, evolve, and survive,",
        "Against hungry humans... and a brutal chef!"
    ]

    current_line_index = 0
    state = "FADE_IN"
    alpha = 0
    fade_speed = 1

    while True:
        skip_button_text = button_font.render("Skip >>", True, WHITE)
        skip_button_rect = skip_button_text.get_rect(center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skip_button_rect.collidepoint(event.pos):
                    return

        # Draw black background
        screen.fill(BLACK)

        # Draw a smooth, pulsing light effect
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        pulse = (math.sin(pygame.time.get_ticks() * 0.002) + 1) / 2

        for i in range(10, 0, -1):
            base_radius = i * 20
            # Adjust radius and alpha using the pulse value
            radius = int(base_radius + pulse * 10)
            light_alpha = int(max(0, 50 - i * 5) * (1 + pulse * 0.5))

            # Create a semi-transparent surface
            light_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

            # Draw a solid white circle on this surface
            pygame.draw.circle(light_surface, WHITE, (radius, radius), radius)

            # Set the alpha (transparency) of the entire surface
            light_surface.set_alpha(light_alpha)

            screen.blit(light_surface, (center_x - radius, center_y - radius))

        if current_line_index < len(story_lines):

            if state == "FADE_IN":
                alpha += fade_speed
                if alpha >= 255:
                    alpha = 255
                    state = "WAIT"
                    start_time = pygame.time.get_ticks()

            elif state == "WAIT":
                if pygame.time.get_ticks() - start_time > 3000:
                    state = "FADE_OUT"

            elif state == "FADE_OUT":
                alpha -= fade_speed
                if alpha <= 0:
                    alpha = 0
                    current_line_index += 1
                    state = "FADE_IN"

            # Draw the text
            if current_line_index < len(story_lines):
                text_surface = story_font.render(story_lines[current_line_index], True, WHITE)
                text_surface.set_alpha(alpha)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                screen.blit(text_surface, text_rect)
            else:
                return
        else:
            return

        screen.blit(skip_button_text, skip_button_rect)
        pygame.display.flip()


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, size, max_hp, base_damage, money, potions, damage_reduction, exp_data,
                 critical_chance=0.1, image_path=None):
        super().__init__()

        if image_path:
            try:
                # Load the image and resize it to the specified size
                original_image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(original_image, size)
            except pygame.error as e:
                print(f"Error loading image: {image_path}. Using a placeholder. Error: {e}")
                self.image = pygame.Surface(size)
                self.image.fill(ORANGE)  # Fallback to a solid color if the image fails to load
        else:
            self.image = pygame.Surface(size)
            self.image.fill(ORANGE)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.money = money
        self.potions = potions
        self.base_damage = base_damage
        self.damage_reduction = damage_reduction

        self.level = exp_data['level']
        self.current_exp = exp_data['current_exp']
        self.max_exp = exp_data['max_exp']
        self.skill_points = 0
        self.critical_chance = critical_chance
        self.lightning_bolt_dmg = 0
        self.enemy_miss_chance = 0.0
        self.accuracy_boost = 0.0
        self.win_streak = 0

    def draw_hp_bar(self, surface, x, y):
        bar_width = 150
        bar_height = 20
        hp_percentage = self.current_hp / self.max_hp
        current_bar_width = int(bar_width * hp_percentage)
        pygame.draw.rect(surface, GRAY, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, RED, (x, y, current_bar_width, bar_height))
        pygame.draw.rect(surface, BLACK, (x, y, bar_width, bar_height), 2)
        draw_text(f"HP: {self.current_hp}/{self.max_hp}", story_font, BLACK, surface, x + bar_width / 2,
                  y + bar_height / 2)

    def draw_exp_bar(self, surface, x, y):
        bar_width = 300
        bar_height = 20
        exp_percentage = self.current_exp / self.max_exp
        current_bar_width = int(bar_width * exp_percentage)
        pygame.draw.rect(surface, GRAY, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, LIGHT_BLUE, (x, y, current_bar_width, bar_height))
        pygame.draw.rect(surface, BLACK, (x, y, bar_width, bar_height), 2)
        draw_text(f"Level: {self.level} EXP: {self.current_exp}/{self.max_exp}", story_font, BLACK, surface,
                  x + bar_width / 2, y + bar_height / 2)


# Level up screen function
def level_up_screen(player):
    upgrades = ["evasion", "critical", "lightning", "accuracy"]
    chosen_upgrade = random.choice(upgrades)

    if chosen_upgrade == "evasion":
        player.enemy_miss_chance += 0.05
        message = "You gained Evasion! Enemy miss chance increased by 5%!"
    elif chosen_upgrade == "critical":
        player.critical_chance += 0.05
        message = "You gained Critical Strike! Critical chance increased by 5%!"
    elif chosen_upgrade == "lightning":
        if player.lightning_bolt_dmg == 0:
            player.lightning_bolt_dmg = 50
            message = "You unlocked Lightning Bolt! You can now use a powerful attack!"
        else:
            player.lightning_bolt_dmg += 10
            message = "Lightning Bolt improved! Damage increased by 10!"
    elif chosen_upgrade == "accuracy":
        player.accuracy_boost += 0.05
        message = "You gained Accuracy! Your accuracy is increased by 5%!"

    screen.fill(BLACK)
    draw_text("Level Up!", title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_wrapped_text(message, story_font, GOLD, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 700)
    pygame.display.flip()
    pygame.time.delay(3000)


def game_over_screen():
    restart_button_text = button_font.render("New Game", True, BLACK)
    restart_button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        return True
        screen.fill(BLACK)
        draw_text("You Lose!", title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

        draw_button(screen, restart_button_rect, WHITE, "New Game", button_font, BLACK)

        pygame.display.flip()


def game_loop(player):
    is_boss_fight = False
    if player.win_streak >= 10 and random.random() < 0.5:
        is_boss_fight = True
        player.win_streak = 0

    enemy_color = random.choice([RED, BLUE, BLACK])

    if is_boss_fight:
        enemy_hp = random.randint(150, 250)
        enemy_damage = random.randint(25, 45)
        enemy_crit_chance = 0.3
        enemy_size = (150, 180)
        enemy_name = "Boss"
        enemy_image_path = os.path.join(current_dir, "assets", "images", "boss.png")

    else:
        enemy_hp = random.randint(80, 150)
        enemy_damage = random.randint(10, 25)
        enemy_crit_chance = 0.1
        enemy_size = (120, 150)
        enemy_name = "Enemy"
        enemy_image_path = None  # No specific image for regular enemies, use color fallback

    enemy = Character(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT / 2, enemy_size, enemy_hp, 0, 0, 0, 0,
                      {'level': 0, 'current_exp': 0, 'max_exp': 0}, enemy_crit_chance, image_path=enemy_image_path)
    if not enemy_image_path:
        enemy.image.fill(enemy_color)

    player_turn = True
    game_state = "start_battle"  # เริ่มด้วยสถานะ start_battle
    battle_start_time = pygame.time.get_ticks()
    start_effect_duration = 1500
    white_effect_radius = 0
    bottom_bar_y = SCREEN_HEIGHT

    enemy_critical_text = None
    enemy_miss_text = None
    player_critical_text = None
    effect_start_time = 0
    effect_duration = 1000
    lightning_effect_time = 0

    # ** ตัวแปรสำหรับเอฟเฟกต์การโจมตี **
    attack_effect_time = 0
    attack_effect_type = None

    last_action_text = ""

    button_width = 150
    button_height = 60
    button_padding = 20
    menu_start_y = SCREEN_HEIGHT - 80

    main_button_rect = pygame.Rect(button_padding, menu_start_y, button_width, button_height)

    sub_menu_buttons = [
        {"name": "Attack", "rect": pygame.Rect(20, menu_start_y, 150, 60), "color": GREEN, "action": "attack_menu"},
        {"name": "Potion", "rect": pygame.Rect(190, menu_start_y, 150, 60), "color": GREEN, "action": "potion_menu"},
        {"name": "Run", "rect": pygame.Rect(360, menu_start_y, 150, 60), "color": GREEN, "action": "run_menu"},
    ]

    attack_menu_buttons = [
        {"name": "Light Attack", "base_dmg": 10, "rect": pygame.Rect(20, menu_start_y, 170, 60), "color": GREEN,
         "action": "player_attack"},
        {"name": "Heavy Attack", "base_dmg": 40, "rect": pygame.Rect(200, menu_start_y, 170, 60), "color": BROWN,
         "action": "player_attack"},
        {"name": "Lightning Bolt", "base_dmg": player.lightning_bolt_dmg,
         "rect": pygame.Rect(380, menu_start_y, 170, 60), "color": YELLOW, "action": "player_attack"},
        {"name": "Back", "rect": pygame.Rect(650, menu_start_y, 100, 60), "color": GRAY, "action": "main"},
    ]

    potion_menu_buttons = [
        {"name": "Use Potion", "rect": pygame.Rect(20, menu_start_y, 200, 60), "color": GREEN, "action": "use_potion"},
        {"name": "Back", "rect": pygame.Rect(650, menu_start_y, 100, 60), "color": GRAY, "action": "main"},
    ]

    run_menu_buttons = [
        {"name": "Confirm Run", "rect": pygame.Rect(20, menu_start_y, 250, 60), "color": GREEN,
         "action": "confirm_run"},
        {"name": "Back", "rect": pygame.Rect(650, menu_start_y, 100, 60), "color": GRAY, "action": "main"},
    ]

    shop_button_rect = pygame.Rect(SCREEN_WIDTH - 150 - 20, 20, 150, 60)

    running_battle = True
    while running_battle:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state != "start_battle":
                    if shop_button_rect.collidepoint(event.pos):
                        shop_screen(player)

                    if player_turn:
                        if game_state == "main" and main_button_rect.collidepoint(event.pos):
                            game_state = "sub_menu"
                        elif game_state == "sub_menu":
                            for button in sub_menu_buttons:
                                if button["rect"].collidepoint(event.pos):
                                    game_state = button["action"]
                                    last_action_text = f"Last Action: {button['name']}"
                        elif game_state == "attack_menu":
                            for button in attack_menu_buttons:
                                if button["rect"].collidepoint(event.pos):
                                    action = button.get("action")
                                    if action == "main":
                                        game_state = "main"
                                    elif action == "player_attack":
                                        damage_done = player.base_damage + button["base_dmg"]

                                        miss_chance_base = player.enemy_miss_chance
                                        if is_boss_fight:
                                            boss_miss_multiplier = random.choice([1.5, 2.0, 2.5, 3.0])
                                            miss_chance_base *= boss_miss_multiplier

                                        effective_miss_chance = miss_chance_base - player.accuracy_boost
                                        if effective_miss_chance < 0:
                                            effective_miss_chance = 0

                                        if random.random() < effective_miss_chance:
                                            damage_done = 0
                                            enemy_miss_text = "MISS"
                                            enemy_critical_text = None
                                            effect_start_time = pygame.time.get_ticks()
                                        else:
                                            enemy_miss_text = None
                                            if random.random() <= player.critical_chance:
                                                damage_done *= 2
                                                enemy_critical_text = "CRITICAL HIT!"
                                                effect_start_time = pygame.time.get_ticks()
                                            else:
                                                enemy_critical_text = None

                                        if button["name"] == "Lightning Bolt":
                                            lightning_effect_time = pygame.time.get_ticks()

                                        # ** กำหนดประเภทและเวลาของเอฟเฟกต์การโจมตี **
                                        if button["name"] == "Light Attack":
                                            attack_effect_time = pygame.time.get_ticks()
                                            attack_effect_type = "light"
                                        elif button["name"] == "Heavy Attack":
                                            attack_effect_time = pygame.time.get_ticks()
                                            attack_effect_type = "heavy"

                                        enemy.current_hp -= damage_done
                                        if enemy.current_hp < 0: enemy.current_hp = 0

                                        player_turn = False
                                        game_state = "main"
                                        last_action_text = f"Last Action: {button['name']}"
                        elif game_state == "potion_menu":
                            for button in potion_menu_buttons:
                                if button["rect"].collidepoint(event.pos):
                                    action = button.get("action")
                                    if action == "main":
                                        game_state = "main"
                                    elif action == "use_potion":
                                        if player.potions > 0:
                                            player.potions -= 1
                                            player.current_hp += 40
                                            if player.current_hp > player.max_hp:
                                                player.current_hp = player.max_hp
                                            player_turn = False
                                            game_state = "main"
                                            last_action_text = "Last Action: Potion"
                                        else:
                                            message = "No potions left!"
                                            message_time = pygame.time.get_ticks()
                                            draw_text(message, story_font, GOLD, screen, SCREEN_WIDTH / 2, 400)
                                            pygame.display.flip()
                                            pygame.time.delay(1000)
                        elif game_state == "run_menu":
                            for button in run_menu_buttons:
                                if button["rect"].collidepoint(event.pos):
                                    action = button.get("action")
                                    if action == "main":
                                        game_state = "main"
                                    elif action == "confirm_run":
                                        print("Tried to run away!")
                                        player_turn = False
                                        game_state = "main"
                                        last_action_text = "Last Action: Run"

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(GREEN)

        screen.blit(player.image, player.rect)
        screen.blit(enemy.image, enemy.rect)

        player.draw_hp_bar(screen, player.rect.left, player.rect.bottom + 10)
        enemy.draw_hp_bar(screen, enemy.rect.left, enemy.rect.bottom + 10)
        if is_boss_fight:
            draw_text("BOSS", story_font, RED, screen, enemy.rect.left + 75, enemy.rect.bottom + 45)

        player.draw_exp_bar(screen, SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 120)

        # เอฟเฟกต์เริ่มฉาก
        if game_state == "start_battle":
            elapsed_time = pygame.time.get_ticks() - battle_start_time
            if elapsed_time < start_effect_duration:
                alpha = int(255 * (1 - (elapsed_time / start_effect_duration)))
                radius = int(100 * (elapsed_time / start_effect_duration))

                white_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(white_surface, (255, 255, 255, alpha), (radius, radius), radius)
                screen.blit(white_surface, (player.rect.centerx - radius, player.rect.centery - radius))
                screen.blit(white_surface, (enemy.rect.centerx - radius, enemy.rect.centery - radius))

                bottom_bar_speed = 3  # ความเร็วในการเลื่อนขึ้น
                if bottom_bar_y > SCREEN_HEIGHT - 100:
                    bottom_bar_y -= bottom_bar_speed
            else:
                game_state = "main"
                bottom_bar_y = SCREEN_HEIGHT - 100

            pygame.draw.rect(screen, BLACK, (0, bottom_bar_y, SCREEN_WIDTH, 100))

        else:
            pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            if lightning_effect_time > 0 and (pygame.time.get_ticks() - lightning_effect_time) < 500:
                draw_lightning(screen, YELLOW, player.rect.center, enemy.rect.center)
            else:
                lightning_effect_time = 0

            # ** แสดงเอฟเฟกต์การโจมตี **
            if attack_effect_time > 0 and (pygame.time.get_ticks() - attack_effect_time) < 500:
                draw_attack_effect(screen, attack_effect_type, player.rect.center, enemy.rect.center,
                                   pygame.time.get_ticks() - attack_effect_time, 500)
            else:
                attack_effect_time = 0
                attack_effect_type = None

            if game_state != "win" and game_state != "lose":
                draw_button(screen, shop_button_rect, GRAY, "Shop", button_font, WHITE)

            if game_state == "main":
                draw_button(screen, main_button_rect, GRAY, "Main", button_font, WHITE)

                if last_action_text:
                    draw_text(last_action_text, story_font, WHITE, screen, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80)

            elif game_state == "sub_menu":
                for button in sub_menu_buttons:
                    draw_button(screen, button["rect"], button["color"], button["name"], button_font, WHITE)
            elif game_state == "attack_menu":
                for button in attack_menu_buttons:
                    if button["name"] == "Lightning Bolt" and player.lightning_bolt_dmg == 0:
                        continue
                    draw_button(screen, button["rect"], button["color"], button["name"], button_font, WHITE)
            elif game_state == "potion_menu":
                for button in potion_menu_buttons:
                    draw_button(screen, button["rect"], button["color"], button["name"], button_font, WHITE)
                draw_text(f"Potions: {player.potions}", story_font, WHITE, screen, SCREEN_WIDTH / 2,
                          SCREEN_HEIGHT * 0.75)
            elif game_state == "run_menu":
                for button in run_menu_buttons:
                    draw_button(screen, button["rect"], button["color"], button["name"], button_font, WHITE)

            if enemy_critical_text and (pygame.time.get_ticks() - effect_start_time) < effect_duration:
                draw_text(enemy_critical_text, button_font, RED, screen, enemy.rect.centerx, enemy.rect.y - 30)
            elif enemy_miss_text and (pygame.time.get_ticks() - effect_start_time) < effect_duration:
                draw_text(enemy_miss_text, button_font, WHITE, screen, enemy.rect.centerx, enemy.rect.y - 30)

            if player_critical_text and (pygame.time.get_ticks() - effect_start_time) < effect_duration:
                draw_text(player_critical_text, button_font, RED, screen, player.rect.centerx, player.rect.y - 30)
            else:
                enemy_critical_text = None
                enemy_miss_text = None
                player_critical_text = None

            if not player_turn and game_state not in ["win", "lose"]:
                pygame.time.delay(500)
                final_damage = enemy_damage * (1 - player.damage_reduction)

                if random.random() < enemy.critical_chance:
                    final_damage *= 2
                    player_critical_text = "CRITICAL HIT!"
                    effect_start_time = pygame.time.get_ticks()
                else:
                    player_critical_text = None

                player.current_hp -= final_damage
                if player.current_hp < 0:
                    player.current_hp = 0
                player_turn = True

        if player.current_hp <= 0:
            game_state = "lose"
        elif enemy.current_hp <= 0:
            game_state = "win"

        if game_state == "win":
            exp_gain = random.randint(15, 30)
            if is_boss_fight:
                exp_gain *= 5

            player.current_exp += exp_gain
            player.money += 500
            player.win_streak += 1

            draw_text("You Win!", title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            draw_text(f"You earned {exp_gain} EXP and 500 coins!", story_font, YELLOW, screen, SCREEN_WIDTH / 2,
                      SCREEN_HEIGHT / 2 + 50)
            pygame.display.flip()
            pygame.time.delay(3000)

            if player.current_exp >= player.max_exp:
                player.level += 1
                player.current_exp = 0
                player.max_exp += 50
                level_up_screen(player)

            return True
        elif game_state == "lose":
            player.current_exp //= 2
            draw_text("You Lose!", title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            draw_text("Your EXP has been reduced by half!", story_font, RED, screen, SCREEN_WIDTH / 2,
                      SCREEN_HEIGHT / 2 + 50)
            pygame.display.flip()
            pygame.time.delay(3000)
            return False

        pygame.display.flip()


# 5. Game flow
if __name__ == "__main__":
    start_screen()
    fade_out_in()
    story_screen()
    fade_out_in()

    player_data = {
        'max_hp': 100,
        'base_damage': 0,
        'money': 0,
        'potions': 0,
        'damage_reduction': 0,
        'exp_data': {
            'level': 1,
            'current_exp': 0,
            'max_exp': 100
        }
    }

    # Pathing change
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "assets", "images", "Character.png")

    player = Character(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT / 2, (120, 150),
                       player_data['max_hp'], player_data['base_damage'], player_data['money'],
                       player_data['potions'], player_data['damage_reduction'], player_data['exp_data'],
                       image_path=image_path)

    while True:
        if game_loop(player):
            fade_out_in()
        else:
            if not game_over_screen():
                break
            else:
                fade_out_in()
                player.current_hp = player.max_hp
                player.base_damage = player_data['base_damage']
                player.potions = player_data['potions']
                player.damage_reduction = player_data['damage_reduction']
                player.level = player_data['exp_data']['level']
                player.current_exp = player.current_exp
                player.max_exp = player_data['exp_data']['max_exp']

    pygame.quit()
    sys.exit()