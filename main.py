import json
import os
import pygame
import sys

import colors
from logic import *
from database import get_best, insert_result


GAMERS_DB = get_best()

def draw_top_gamers():
    """ Displays a list of the top three players in the upper right corner of the playing field """
    font_top = pygame.font.SysFont('simsun', 30)
    font_gamer = pygame.font.SysFont('simsun', 20)
    text_head = font_top.render("Best tries: ", True, colors.RAISIN_BLACK)
    screen.blit(text_head, (300, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index + 1}. {name} - {score}'
        text_gamer = font_gamer.render(s, True, colors.RAISIN_BLACK)
        screen.blit(text_gamer, (300, 38 + 22 * index))


def draw_interface(score, delta=0):
    """ Draws the playing field and header with score and top gamers """
    pygame.draw.rect(screen, colors.SEASHELL, TITLE_RECT)
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('simsun', 48)
    font_delta = pygame.font.SysFont('simsun', 22)
    text_score = font_score.render("Score: ", True, colors.RAISIN_BLACK)
    text_score_value = font_score.render(f"{score}", True, colors.RAISIN_BLACK)
    screen.blit(text_score, (20, 25))
    screen.blit(text_score_value, (170, 25))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, colors.RAISIN_BLACK)
        screen.blit(text_delta, (185, 75))
    draw_top_gamers()
    for row in range(BLOCKS_NUMBER):
        for col in range(BLOCKS_NUMBER):
            value = mas[row][col]
            text = font.render(f'{value}', True, colors.BLACK)
            x = col * SIZE_BLOCK + (col + 1) * GAP
            y = row * SIZE_BLOCK + (row + 1) * GAP + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (x, y, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_width, font_height = text.get_size()
                text_x = x + (SIZE_BLOCK - font_width) / 2
                text_y = y + (SIZE_BLOCK - font_height) / 2
                screen.blit(text, (text_x, text_y))


def init_const():
    """ Creates an initial layout of numbers with zeroes and two numbers (2 or 4) in random places """
    global mas, score
    score = 0
    mas = [[0] * 4 for i in range(4)]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)




COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 204, 204),
    8: (255, 153, 153),
    16: (255, 102, 102),
    32: (255, 51, 51),
    64: (255, 0, 0),
    128: (204, 0, 0),
    256: (153, 0, 0),
    512: (102, 0, 0),
    1024: (51, 0, 0),
    2048: (21, 0, 0),
    4096: (153, 153, 255),
    8192: (153, 153, 255),
    16384: (102, 102, 255),
    32768: (51, 51, 255),
}

BLOCKS_NUMBER = 4
SIZE_BLOCK = 110
GAP = 10
WIDTH = BLOCKS_NUMBER * SIZE_BLOCK + (BLOCKS_NUMBER + 1) * GAP
HEIGHT = WIDTH + 110
TITLE_RECT = pygame.Rect(0, 0, WIDTH, SIZE_BLOCK)
biggest_number = 0

mas = None
score = None
USERNAME = None
project_path = os.getcwd()
if 'last_game_data.txt' in os.listdir(project_path):
    with open('last_game_data.txt') as file:
        data = json.load(file)
        mas = data['mas']
        score = data['score']
        USERNAME = data['user']
    abs_path = os.path.join(project_path, 'last_game_data.txt')
    os.remove(abs_path)
else:
    init_const()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')


def draw_intro():
    img2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('stxingkai', 70)
    text_welcome = font.render("Welcome", True, colors.SEASHELL)
    name = 'Your name'
    is_find_name = False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Your name':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break
        screen.fill(colors.BLACK)
        text_name = font.render(name, True, colors.SEASHELL)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, (200, 200)), (10, 10))
        screen.blit(text_welcome, (245, 90))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(colors.BLACK)


def draw_game_over():
    """ Shows the game over screen with the final score of a player
    and information about best score or information that players result broke the record.
    With pressing Space player can start game again.
    With pressing Enter player can be changed.
    """
    global USERNAME, mas, score, GAMERS_DB, biggest_number
    img2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('stxingkai', 65)
    font_info = pygame.font.SysFont('stxingkai', 55)
    text_game_over = font.render("Game over", True, colors.SEASHELL)
    text_score = font_info.render(f'You got {score} points', True, colors.SEASHELL)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = 'You broke the record!'
    elif biggest_number >= 32768:
        text = 'You reach the limit!'
    else:
        text = f"Record is {best_score} points"
    text_record = font_info.render(text, True, colors.SEASHELL)
    insert_result(USERNAME, score)
    GAMERS_DB = get_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game with same gamer name
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    # go back to intro screen
                    USERNAME = None
                    make_decision = True
                    init_const()
        screen.fill(colors.BLACK)
        screen.blit(text_game_over, (235, 90))
        screen.blit(text_score, (35, 280))
        screen.blit(text_record, (35, 350))
        screen.blit(pygame.transform.scale(img2048, (200, 200)), (10, 10))
        pygame.display.update()
    screen.fill(colors.BLACK)


def save_game():
    data = {
        'user': USERNAME,
        'score': score,
        'mas': mas
    }
    with open('last_game_data.txt', 'w') as outfile:
        json.dump(data, outfile)


def game_loop():
    global score, mas, biggest_number
    draw_interface(score)
    pygame.display.update()
    is_mas_moved = False
    finish_game = False
    while (is_zero_in_mas(mas) or can_move(mas)) and biggest_number < 32768 and not finish_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, biggest_number, is_mas_moved = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, biggest_number, is_mas_moved = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, biggest_number, is_mas_moved = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, biggest_number, is_mas_moved = move_down(mas)
                elif event.key == pygame.K_BACKSPACE:
                    # end the game
                    finish_game = True
                score += delta
                if is_zero_in_mas(mas) and is_mas_moved:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    is_mas_moved = False
                draw_interface(score, delta)
                pygame.display.update()


while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
