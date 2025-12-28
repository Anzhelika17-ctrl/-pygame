import pygame
import random
import sys
import os

pygame.init()

# ---------- Параметры ----------
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гном в пещере")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Georgia", 30)
FONT_BIG = pygame.font.SysFont("Georgia", 40, bold=True)

# ---------- Цвета для кнопки ----------
COLOR_BUTTON_NORMAL = (100, 200, 100)      # Зеленый
COLOR_BUTTON_TEXT = (255, 255, 255)        # Белый
# ---------- Функция загрузки картинок ----------
def load_image(path, size=None):
    if not os.path.exists(path):
        print(f"[ОШИБКА] Нет картинки: {path}")
        w, h = size if size else (50, 50)
        e = pygame.Surface((w, h))
        e.fill((255, 0, 0))
        return e
    img = pygame.image.load(path)
    if size:
        img = pygame.transform.scale(img, size)
    print(f"[OK] Загружено: {path}")
    return img

# ---------- Загрузка всех изображений ----------
bg_img      = load_image("cave.jpg",        (WIDTH, HEIGHT))
gnome_run   = load_image("gnome_run.png",   (130, 130))
gnome_jump  = load_image("gnome_jump.png",  (110, 160))
rock_img    = load_image("rock.png",        (90, 100))
title_img   = load_image("title_screen.png",(WIDTH, HEIGHT))
vin         = load_image("koncovka.jpg",    (WIDTH, HEIGHT))
lose        = load_image("zaval.png",        (WIDTH, HEIGHT))
# ---------- Переменные ----------
gnome_x, gnome_y = 80, 220
velocity_y = 0
gravity = 1
jump_power = -15
stones = []
score = 0
game_over = False
game_started = False
title_screen = True
min_distance = 250 

# ---------- Текст ----------
def draw_text(text, x, y, font=FONT, color=(255, 255, 255)):
    scr = font.render(text, True, color)
    screen.blit(scr, (x, y))
# ---------- Класс кнопки ----------
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = COLOR_BUTTON_NORMAL
        self.hovered = False
        self.clicked = False
    
    def draw(self, surface):
        # Рисуем кнопку
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        # Текст кнопки
        text_surf = FONT.render(self.text, True, COLOR_BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos, mouse_click):
        # Проверяем, наведена ли мышь на кнопку
        self.hovered = self.rect.collidepoint(mouse_pos)
          
        # Проверяем клик
        if mouse_click and self.hovered:
            self.clicked = True
            return True
        else:
            self.clicked = False
            return False

# ---------- ЗАСТАВКА ----------
def show_title_screen():
    global title_screen
    while title_screen:
        # Рисуем фоновую картинку заставки
        if title_img:
            screen.blit(title_img, (0, 0))
        else:
            # Если нет картинки, делаем простой фон
            screen.fill((50, 30, 10))  # Коричневый цвет пещеры
            pygame.draw.rect(screen, (80, 50, 20), (100, 80, WIDTH-200, HEIGHT-160))
        
        # Текст на заставке
        draw_text("ГНОМ В ПЕЩЕРЕ", 250, 100, FONT_BIG, (255, 215, 0))  # Желтый 
        draw_text("Гном Том добыл самый большой самородок ", 120, 160, FONT, (200, 200, 200))
        draw_text("в своей жизни но от его радостного крика ", 130, 190, FONT, (200, 200, 200))
        draw_text("треснул потолок шахты !Теперь ему нужно  ", 120, 220, FONT, (200, 200, 200))
        draw_text("бежать к выходу , преодолевая препятствия ", 120, 250, FONT, (200, 200, 200))
        draw_text("пока , потолок не рухнул.", 250, 280, FONT, (200, 200, 200))
        # Инструкция для перехода
        draw_text("Нажмите M для продолжения", 230, 320, FONT, (255, 215, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Нажатие M
                    title_screen = False  # Выход из заставки
                    return
                if event.key == pygame.K_ESCAPE:  # ESC для выхода
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        clock.tick(60)

# ---------- Меню ----------
def menu():
    global game_started
    
    # Создаем кнопку "Начать игру"
    button_start = Button(270, 300, 300, 60, "НАЧАТЬ ИГРУ")
    
    while not game_started:
        # Используем игровой фон для меню
        screen.blit(bg_img, (0, 0))
        
        # Текст меню
        draw_text("ГНОМ В ПЕЩЕРЕ", 260, 80, FONT_BIG, (255, 215, 0))
        draw_text("Управление:", 340, 140)
        draw_text("SPACE - прыжок", 310, 180)
        draw_text("Цель игры:", 340, 220)
        draw_text("Избегайте камней и наберите 300 очков!", 150, 260)
        
        # Рисуем кнопку
        button_start.draw(screen)
        
        # Получаем состояние мыши
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_click = True
        
        # Обновляем кнопку и проверяем нажатие
        if button_start.update(mouse_pos, mouse_click):
            game_started = True
        
        pygame.display.update()
        clock.tick(60)

# ---------- Конец игры ----------
def end_screen(win=False):
    while True:
        screen.blit(vin, (0, 0))
        if win:
            screen.blit(vin,(0,0))
        else:
            screen.blit(lose,(0,0))
        # Затемнение
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if win:
            draw_text("ПОБЕДА!", 320, 120, FONT_BIG, (0, 255, 0))
            draw_text("Гном выбрался из пещеры с сокровищами!", 150, 170)
        else:
            draw_text("ПОРАЖЕНИЕ", 310, 120, FONT_BIG, (255, 50, 50))
            draw_text("Гном ударился о камень", 270, 170)
        
        draw_text(f"Счёт: {score}", 360, 220)
        draw_text("Нажмите ESC чтобы выйти", 230, 280)
        draw_text("Нажмите ЛЕВЫЙ SHIFT для повторной игры", 150, 320)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LSHIFT:
                    # Возвращаемся в начало
                    reset_game()
                    return

        pygame.display.update()
        clock.tick(60)
# ---------- Сброс игры ----------
def reset_game():
    global gnome_x, gnome_y, velocity_y, stones, score, game_over, game_started, title_screen
    gnome_x, gnome_y = 80, 280
    velocity_y = 0
    stones = []
    score = 0
    game_over = False
    game_started = False
    title_screen = True
# ==================== ЗАПУСК ИГРЫ ====================
# Показываем заставку
show_title_screen()
# Показываем меню
menu()
# Основной игровой цикл
while True:
    if game_over:
        end_screen(win=False)
        continue

    if score >= 300:
        end_screen(win=True)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gnome_y >= 280:
                velocity_y = jump_power
            if event.key == pygame.K_ESCAPE:
                # Возврат в меню
                reset_game()
                show_title_screen()
                menu()
    # ---------- Прыжок ----------
    gnome_y += velocity_y
    velocity_y += gravity
    if gnome_y > 280:
        gnome_y = 280
    # ---------- Гном меняет картинку ----------
    if gnome_y < 280:
        current_gnome = gnome_jump
    else:
        current_gnome = gnome_run
    # ---------- Спавн камней ----------
    if random.randint(1, 40) == 1:
        if len(stones) == 0:
            stones.append([WIDTH, 320])
        else:
            last_stone = stones[-1]
            if last_stone[0] < WIDTH - min_distance:
                stones.append([WIDTH, 320])
    # ---------- Движение камней ----------
    for st in stones:
        st[0] -= 8
        if st[0] < -40:
            stones.remove(st)
            score += 10
    # ---------- Столкновение ----------
    for st in stones:
        g_rect = pygame.Rect(gnome_x, gnome_y, 60, 60)
        s_rect = pygame.Rect(st[0], st[1], 40, 60)
        if g_rect.colliderect(s_rect):
            game_over = True 
    # ---------- ОТРИСОВКА ----------
    screen.blit(bg_img, (0, 0))
    screen.blit(current_gnome, (gnome_x, gnome_y))
    for st in stones:
        screen.blit(rock_img, (st[0], st[1]))
    draw_text(f"Счёт: {score}", 20, 20)
    # Подсказка во время игры
    draw_text("ESC - меню", WIDTH-180, 20, color=(200, 200, 0))

    pygame.display.update()
    clock.tick(60)