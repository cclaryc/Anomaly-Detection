import os
import random
import pygame
import math
import sys
from os import listdir
from os.path import isfile, join
from pygame.locals import *
import time
import random

pygame.init()

pygame.display.set_caption("Observation Duty")

TRANSPARENT = (0, 0, 0, 63)  # Semi-transparent black
TRANSPARENTT = (0, 0, 0, 0)
BG_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
OFFSET = 40
info = pygame.display.Info()
resolution = (info.current_w, info.current_h)
screen_width, screen_height = info.current_w, info.current_h
semi_resolution = (1920, 1080)

frame_dir = r"FramesBedroom"
frames = []

FPS = 10

window = pygame.display.set_mode(semi_resolution)

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))

def change_background():
    random_time = random.randint(25000, 45000)  # milliseconds
    return random_time

def real_to_game_time(real_time):
    return (real_time % 300) / 5  # 5 real minutes = 1 in-game hour

class Button:
    def __init__(self, color, x, y, width, height, text='', action=None, visited=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.visited = visited
        self.last_pressed_time = 0
        self.cooldown_duration = 0.5  

    def draw(self, screen, outline=None):
        button_surface = pygame.Surface((self.x, self.y), pygame.SRCALPHA)
        button_surface.fill(TRANSPARENT)
        if self.text != '':
            font = pygame.font.SysFont("Cambria Math", 20)  
            text = font.render(self.text, True, (211, 211, 211))  
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))  

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:  
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
    def press(self):
        if time.time() - self.last_pressed_time >= self.cooldown_duration:
            self.last_pressed_time = time.time()
            return True
        else:
            return False
    
class menu:
    def draw_semi_transparent_window(screen, width, height):
        window_surface = pygame.Surface((width, height), pygame.SRCALPHA)  
        window_surface.fill(TRANSPARENT)  
        screen.blit(window_surface, (screen_width - width, screen_height - height))  
        return window_surface  

def Draw_text(screen, text, x, y, L, l, color):
    font = pygame.font.SysFont("Cambria Math", 20)  
    text = font.render(text, True, (211, 211, 211))  
    screen.blit(text, (x + (L / 2 - text.get_width() / 2), y + (l / 2 - text.get_height() / 2)))  

class StartButton:
    def __init__(self, color, x, y, width, height, text='', action=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if outline:
            pygame.draw.rect(screen, outline, (self.x, self.y, self.width, self.height), 2)
        if self.text != '':
            font = pygame.font.SysFont("Cambria Math", 20)
            text = font.render(self.text, True, BLACK)  
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

def draw_centered_text(screen, text, y, color=GRAY):
    font = pygame.font.SysFont("Cambria Math", 36)  
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(semi_resolution[0] / 2, y))
    screen.blit(rendered_text, text_rect)

def start_screen(window):
   
    background_image = pygame.image.load("start_screen.png")
    background_image = pygame.transform.scale(background_image, semi_resolution)

    start_button_y = semi_resolution[1] // 2 + 100
    exit_button_y = semi_resolution[1] // 2 + 165

    start_button = StartButton(GRAY, semi_resolution[0] // 2 - 50, start_button_y, 100, 50, "Start")
    exit_button = StartButton(GRAY, semi_resolution[0] // 2 - 50, exit_button_y, 100, 50, "Exit")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.is_over(pos):
                    return  
                elif exit_button.is_over(pos):
                    pygame.quit()
                    sys.exit()

        window.blit(background_image, (0, 0))  
        
        start_button.draw(window, outline=BLACK)  
        exit_button.draw(window, outline=BLACK)  
        
        pygame.display.update() 
   

class PauseButton:
    def __init__(self, color, x, y, width, height, text='', action=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if outline:
            pygame.draw.rect(screen, outline, (self.x, self.y, self.width, self.height), 2)
        if self.text != '':
            font = pygame.font.SysFont("Cambria Math", 20)
            text = font.render(self.text, True, BLACK) 
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

def draw_centered_text(screen, text, y, color=GRAY):
    font = pygame.font.SysFont("Cambria Math", 36)  
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(semi_resolution[0] / 2, y))
    screen.blit(rendered_text, text_rect)

def pause_screen(window):
    continue_button = PauseButton(GRAY, semi_resolution[0] // 2 - 50, semi_resolution[1] // 2 - 25, 100, 50, "Continue")
    exit_button = PauseButton(GRAY, semi_resolution[0] // 2 - 50, semi_resolution[1] // 2 + 40, 100, 50, "Exit")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if continue_button.is_over(pos):
                    return  # Resume the game
                elif exit_button.is_over(pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  

        window.fill(BG_COLOR)  
        
        draw_centered_text(window, "Ready to give up?", semi_resolution[1] // 3)  
        continue_button.draw(window, outline=BLACK)  
        exit_button.draw(window, outline=BLACK)  
        
        pygame.display.update()  

def win_screen(window):
    win_font = pygame.font.SysFont("Cambria Math", 72)
    win_text = win_font.render("Congratulations! You've won!", True, WHITE)
    text_rect = win_text.get_rect(center=(semi_resolution[0] / 2, semi_resolution[1] / 2))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  

        window.fill(BLACK)
        window.blit(win_text, text_rect)
        pygame.display.update()

def game_over_screen(window, message, background_image_path):
    game_over_font = pygame.font.SysFont("Cambria Math", 72)
    restart_font = pygame.font.SysFont("Cambria Math", 36)
    
    game_over_text = game_over_font.render(message, True, RED)
    restart_text = restart_font.render("Press Enter to Restart or ESC to Exit", True, RED)
    
    game_over_rect = game_over_text.get_rect(center=(semi_resolution[0] // 2, semi_resolution[1] // 2 - 50))
    restart_rect = restart_text.get_rect(center=(semi_resolution[0] // 2, semi_resolution[1] // 2 + 50))
    
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (semi_resolution[0], semi_resolution[1]))
    
    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Blit background image
        window.blit(background_image, (0, 0))
        
        # Blit texts
        window.blit(game_over_text, game_over_rect)
        window.blit(restart_text, restart_rect)
        
        # Update display
        pygame.display.update()

    return False

def draw_mistakes(screen, mistakes):
    for i in range(mistakes):
        x_pos = 20 + (i * 30)
        y_pos = screen_height - 40
        pygame.draw.line(screen, RED, (x_pos, y_pos), (x_pos + 20, y_pos + 20), 5)
        pygame.draw.line(screen, RED, (x_pos + 20, y_pos), (x_pos, y_pos + 20), 5)

def main(window):
    frame_directories = ([r"FramesBedroom", r"FramesBack", r"FramesKitchen", r"FramesBathroom"], [r"", r"", r"", r""])
    frame_directories_copy = [r"FramesBedroom", r"FramesBack", r"FramesKitchen", r"FramesBathroom"]
    frame_directories_names = ["Bedroom", "Frontdoor", "Kitchen", "Bathroom"]
    anomalies_bed = (["dystorsion", r"Anomalies\Beddystorsion1"], ["camera_malf", r"Anomalies\Bedcamera_malf"], ["movement", r"Anomalies\Bedmovement"], ["picture", r"Anomalies\Bedpicturee"])
    anomalies_back = (["movement", r"Anomalies\Backmovement"], ["missing", r"Anomalies\Backmissing"], ["extr", r"Anomalies\Backextr"], ["intruder", r"Anomalies\Backintruder2"])
    anomalies_kitchen = (["extr", r"Anomalies\Kitchenextr"], ["abyss", r"Anomalies\Kitchenabyss"])
    anomalies_bathroom = (["camera_malf", r"Anomalies\Bathcamera_malf"], ["picture", r"Anomalies\Bathpicture"], ["intruder", r"Anomalies\Bathintruder1"], ["movement", r"Anomalies\Bathmovement"])
    frame_dir = r"FramesBedroom"
    
    mistake_count = 0
    max_mistakes = 3

    clock = pygame.time.Clock()
    
    selected_room = None
    selected_anomaly_type = None

    frame_index = 0
    frames = []
    window_visible = False

    visited = False
    fullscreen = False
    real_current_time = time.time()
    game_start_time = time.time()
    game_current_time1 = int(real_current_time - game_start_time) // 60
    
    last_background_change_time = pygame.time.get_ticks()
    next_background_change_time = change_background()
    
    frame_files = sorted(os.listdir(frame_dir))  
    for frame_file in frame_files:
        frame_path = os.path.join(frame_dir, frame_file)
        frame = pygame.image.load(frame_path).convert() 
        frame = pygame.transform.scale(frame, semi_resolution)  
        frames.append(frame)  
    
    menu_surf = menu()
    screen = pygame.display.set_mode(semi_resolution)
    button = Button((0, 255, 0), screen_width - OFFSET - 80 - 10, screen_height - OFFSET, 100, 40, 'Report', 'show_window')  # color, x, y, width, height, text, action
    button2 = Button((0, 255, 0), screen_width - 800 + OFFSET, screen_height - OFFSET, 80, 20, 'Cancel', 'close_window')
    button3 = Button((0, 0, 0), screen_width - OFFSET - 80, screen_height - OFFSET, 80, 40, 'Submit', 'submit')
    
    button4 = Button((0, 255, 0), screen_width + 3 * OFFSET - 800, screen_height - 300 + OFFSET + 10, 100, 40, '[ ] Kitchen', 'Kitchen')
    button5 = Button((0, 255, 0), screen_width + 6 * OFFSET - 800 + 40, screen_height - 300 + OFFSET + 10, 100, 40, '[ ] Bathroom', 'Bathroom')
    button6 = Button((0, 255, 0), screen_width + 9 * OFFSET - 800 + 80, screen_height - 300 + OFFSET + 10, 100, 40, '[ ] Front', 'Frontdoor')
    button7 = Button((0, 255, 0), screen_width + 12 * OFFSET - 800 + 120, screen_height - 300 + OFFSET + 10, 100, 40, '[ ] Bedroom', 'Bedroom')
    
    left_arrow = Button((0, 255, 0), 20, screen_height // 2, 80, 40, '\u2989', 'prev_room')
    right_arrow = Button((0, 255, 0), screen_width - 100, screen_height // 2, 80, 40, '⦊', 'next_room')
    
    buttons = [button4, button5, button6, button7]

    picture = Button((0, 255, 0), screen_width + 3 * OFFSET - 800, screen_height - 300 + OFFSET + 10 + 90, 100, 40, '[ ] Picture Anomaly', 'picture')
    dystorsion = Button((0, 255, 0), screen_width + 6 * OFFSET - 800 + 40, screen_height - 300 + OFFSET + 10 + 90, 100, 40, '[ ] Dystorsion', 'dystorsion')
    extr = Button((0, 255, 0), screen_width + 9 * OFFSET - 800 + 80, screen_height - 300 + OFFSET + 10 + 90, 100, 40, '[ ] Extra object', 'extr')
    missing = Button((0, 255, 0), screen_width + 12 * OFFSET - 800 + 120, screen_height - 300 + OFFSET + 10 + 90, 100, 40, '[ ] Missing object', 'missing')
    
    intruder = Button((0, 255, 0), screen_width + 3 * OFFSET - 800, screen_height - 300 + OFFSET + 10 + 130, 100, 40, '[ ] Intruder', 'intruder')
    movement = Button((0, 255, 0), screen_width + 6 * OFFSET - 800 + 40, screen_height - 300 + OFFSET + 10 + 130, 100, 40, '[ ]  Movement', 'movement')
    abyss = Button((0, 255, 0), screen_width + 9 * OFFSET - 800 + 80, screen_height - 300 + OFFSET + 10 + 130, 100, 40, '[ ] Abyss', 'abyss')
    camera_malf = Button((0, 255, 0), screen_width + 12 * OFFSET - 800 + 120, screen_height - 300 + OFFSET + 10 + 130, 100, 40, '[ ] Camera malfunction', 'camera_malf')

    anomaly_buttons = [abyss, dystorsion, extr, missing, intruder, movement, picture, camera_malf]
    
    dir_poz = 0  
    no_dir = len(frame_directories[0])  
    Draw_text(screen, frame_directories_names[dir_poz], 100, 100, 20, 20, ((0, 255, 0)))  
    Draw_text(screen, str(clock.get_rawtime()), 100, 500, 20, 20, ((0, 255, 0)))  
    run = True
    number_of_anomalies = 0
    start_time=0
    while run:
        real_current_time = time.time()
        game_current_time1 = int(real_current_time - game_start_time) // 60

        if real_current_time-start_time>60 and start_time!=0:
            if game_over_screen(window,"The anomalies have taken over! You weren't fast enough!",r"creepy_face.png"):
                start_screen(window)
                main(window)
            else:
                return

        if game_current_time1 >= 30:  
            win_screen(window)

        clock.tick(FPS)
        screen.fill(BG_COLOR) 
        game_current_time = int(real_current_time - game_start_time)
        current_time = pygame.time.get_ticks()
        if frame_index < len(frames):
            screen.blit(frames[frame_index], (0, 0))  
            frame_index = (frame_index + 1) % len(frames)
        for event in pygame.event.get():  # Getting events
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_LCTRL):
                run = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_screen(window)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button.is_over(pos) and window_visible == False:
                    print("Button clicked")
                    window_visible = not window_visible
                elif button2.is_over(pos) and window_visible:
                    window_visible = False
                elif button3.is_over(pos) and window_visible == True:
                    print("Submit button clicked")
                    for b in buttons:
                        if b.visited:
                            selected_room = b.action  
                            break  
                    for b in anomaly_buttons:
                        if b.visited:
                            selected_anomaly_type = b.action  
                            break
                    index = 0
                    for i in range(len(frame_directories_names)):
                        if selected_room == frame_directories_names[i]:
                            index = i
                            break
                    print(selected_anomaly_type)
                    print(frame_directories[0][index])
                    if selected_anomaly_type in frame_directories[0][index]:
                        print("Correct report")
                        number_of_anomalies-=1
                        start_time=0
                        if frame_dir == frame_directories[0][index]:
                            print("Resetting current frame")
                            frame_directories[0][index] = frame_directories[1][index]
                            frame_directories[1][index] = ""
                            frame_dir = frame_directories[0][index]
                            frame_files = sorted(os.listdir(frame_dir))
                            frames.clear()  
                            for frame_file in frame_files:
                                frame_path = os.path.join(frame_dir, frame_file)
                                frame = pygame.image.load(frame_path).convert()  
                                frame = pygame.transform.scale(frame, semi_resolution)  
                                frames.append(frame)  
                        else:
                            frame_directories[0][index] = frame_directories[1][index]
                            frame_directories[1][index] = ""
                    else:
                        print("Incorrect report")
                        mistake_count += 1
                        if mistake_count >= max_mistakes:
                            if game_over_screen(window,"The anomalies have taken over! You weren't accurate enough!",r"creepy_face.png"):
                                start_screen(window)
                                main(window)
                            else:
                                return  
                    window_visible = False
                elif left_arrow.is_over(pos) and left_arrow.press():
                    if dir_poz == 0:
                        dir_poz = no_dir - 1
                    else:
                        dir_poz = dir_poz - 1
                    frame_dir = frame_directories[0][dir_poz]
                    frame_files = sorted(os.listdir(frame_dir))
                    frames.clear()  
                    for frame_file in frame_files:
                        frame_path = os.path.join(frame_dir, frame_file)
                        frame = pygame.image.load(frame_path).convert() 
                        frame = pygame.transform.scale(frame, semi_resolution)  
                        frames.append(frame)  
                elif right_arrow.is_over(pos) and right_arrow.press():
                    dir_poz = (dir_poz + 1) % no_dir
                    frame_dir = frame_directories[0][dir_poz]
                    frame_files = sorted(os.listdir(frame_dir))
                    frames.clear()  
                    for frame_file in frame_files:
                        frame_path = os.path.join(frame_dir, frame_file)
                        frame = pygame.image.load(frame_path).convert()  
                        frame = pygame.transform.scale(frame, semi_resolution) 
                        frames.append(frame) 
                for b in buttons:
                    if b.is_over(pos) and b.press() == True:
                        for c in buttons: 
                            if c != b:
                                c.visited = False
                                c.text = '[ ]' + c.text[3:]
                        b.visited = not b.visited
                        if b.visited == True:
                            b.text = '[X]' + b.text[3:]
                        else:
                            b.text = '[ ]' + b.text[3:]
                for b in anomaly_buttons:
                    if b.is_over(pos) and b.press() == True:
                        for c in anomaly_buttons: 
                            if c != b:
                                c.visited = False
                                c.text = '[ ]' + c.text[3:]
                        b.visited = not b.visited
                        if b.visited == True:
                            b.text = '[X]' + b.text[3:]
                        else:
                            b.text = '[ ]' + b.text[3:]
            if event.type == KEYDOWN:
                if event.key == K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(resolution, FULLSCREEN)
                        print(resolution)
                    else:
                        screen = pygame.display.set_mode(semi_resolution)
        if current_time - last_background_change_time > next_background_change_time:
            last_background_change_time = current_time
            next_background_change_time = change_background()
            print("Background changed")
            random_number = random.randint(0, 3)
            print(random_number)
            print(frame_directories[0][random_number])
            print(frame_directories_copy[random_number])
            if frame_directories[0][random_number] in frame_directories_copy[random_number]: 
                print("Anomaly added")
                if number_of_anomalies==0:
                    start_time=real_current_time
                number_of_anomalies+=1
                if random_number == 0:
                    random_number2 = random.randint(0, 3)
                    frame_directories[1][random_number] = frame_directories[0][random_number]
                    frame_directories[0][random_number] = anomalies_bed[random_number2][1]
                    print(anomalies_bed[random_number2][1])
                elif random_number == 1:
                    random_number2 = random.randint(0, 3)
                    frame_directories[1][random_number] = frame_directories[0][random_number]
                    frame_directories[0][random_number] = anomalies_back[random_number2][1]
                    print(anomalies_back[random_number2][1])
                elif random_number == 2:
                    random_number2 = random.randint(0, 1)
                    frame_directories[1][random_number] = frame_directories[0][random_number]
                    frame_directories[0][random_number] = anomalies_kitchen[random_number2][1]
                    print(anomalies_kitchen[1])
                elif random_number == 3:
                    random_number2 = random.randint(0, 3)
                    frame_directories[1][random_number] = frame_directories[0][random_number]
                    frame_directories[0][random_number] = anomalies_bathroom[random_number2][1]
                    print(anomalies_bathroom[random_number2][1])
                print("Anomaly swap complete")
                print(random_number)
                print(random_number2)
                print(frame_directories[0][random_number])
                print(frame_directories[1][random_number])    
        if window_visible:
            menu.draw_semi_transparent_window(screen, 800, 300)
            Draw_text(screen, 'ANOMALY SPOTTED IN:', screen_width + 9 * OFFSET - 800 + 80, screen_height - 300 + 20, 20, 20, ((0, 255, 0)))
            button2.draw(screen, (0, 0, 0, 0))
            button3.draw(screen, (0, 0, 0, 0))
            for b in buttons:
                b.draw(screen, (0, 0, 0, 0))
            Draw_text(screen, 'ANOMALY TYPE:', screen_width + 9 * OFFSET - 800 + 80, screen_height - 300 + 100, 20, 20, ((0, 255, 0)))
            for b in anomaly_buttons:
                b.draw(screen, (0, 0, 0, 0))
        else:
            button.draw(screen, (0, 0, 0, 0))
            for c in anomaly_buttons: 
                c.visited = False
                c.text = '[ ]' + c.text[3:]
            for c in buttons: 
                c.visited = False
                c.text = '[ ]' + c.text[3:]
        left_arrow.draw(screen, (0, 0, 0, 0))
        right_arrow.draw(screen, (0, 0, 0, 0))
        Draw_text(screen, frame_directories_names[dir_poz], 50, 30, 20, 20, ((0, 255, 255)))
        Draw_text(screen, str((game_current_time1 + 12) % 13 + (game_current_time1 + 12) // 13) + " AM", screen_width - OFFSET - 19, 30, 20, 20, ((0, 255, 0)))

        draw_mistakes(screen, mistake_count)

        pygame.display.update()
        pygame.display.flip()
    pygame.quit()
    quit()

if __name__ == "__main__":
    start_screen(window)
    main(window)
