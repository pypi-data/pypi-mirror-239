from .NebulaCore import pygame, os, QUIT, KEYDOWN, K_RETURN, K_BACKSPACE
from ._setup import Main, configNewProject, configLoadProject, configRecentProject
ABYSS_VERSION = 'Abyss Console v0.0.1'
ABYSS_INFO = ['Nebula v0.1.1','Abyss Console v0.0.1','Developed by Setoichi Yumaden']

class Console:
    def __init__(self, width, height, theme):
        self.theme = theme
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(theme["font"], theme["font_size"])
        self.box_color = theme["box"]
        self.cursor_color = theme["cursor"]
        self.bg_color = theme["bg_color"]
        self.text_color = theme["text_color"]
        self.input_color = theme["input_color"]
        self.exec_color = theme["exec_color"]
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Abyss')
        self.input_buffer = ''
        self.output_lines = []
        self.cursor_visible = True  # Cursor visibility state
        self.last_cursor_toggle = pygame.time.get_ticks()
        self.cursor_interval = 400  # Cursor blink interval in milliseconds
        self.header()

    def header(self):
        self.custom_print('Abyss Console 0.1.0')
        self.custom_print(f'{os.getcwd()}')

    def changeTheme(self, desiredTheme:str):
        if desiredTheme in list(themes.keys()):
            theme = themes[desiredTheme]
        else:
            theme = self.theme
        self.box_color = theme["box"]
        self.bg_color = theme["bg_color"]
        self.cursor_color = theme["cursor"]
        self.text_color = theme["text_color"]
        self.exec_color = theme["exec_color"]
        self.input_color = theme["input_color"]
        self.font = pygame.font.SysFont(theme["font"], theme["font_size"])

    def custom_print(self, output):
        # Append the output to the console's output buffer
        self.output_lines.append((('~ Abyss | ', self.exec_color), (output, self.text_color)))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    self.handle_keydown(event)

            self.toggle_cursor()
            self.render()
            pygame.display.update()

    def handle_keydown(self, event):
        if event.key == K_RETURN:
            self.execute_command(self.input_buffer)
            self.input_buffer = ''
        elif event.key == K_BACKSPACE:
            self.input_buffer = self.input_buffer[:-1]
        else:
            self.input_buffer += event.unicode

    def toggle_cursor(self):
        # Toggle the cursor visibility
        if pygame.time.get_ticks() - self.last_cursor_toggle > self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = pygame.time.get_ticks()

    def request_input(self, prompt, callback, additional_prompt=None):
        self.custom_print(prompt)
        self.render()
        pygame.display.update()
        
        input_buffer = ''
        waiting_for_input = True
        
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting_for_input = False
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        waiting_for_input = False
                        if additional_prompt:
                            # If additional input is required, store the first input
                            # and start another input request for the second piece of information.
                            self.request_input(additional_prompt, lambda additional_input: callback(input_buffer, additional_input))
                        else:
                            if callback == configLoadProject:
                                callback(self, input_buffer)
                            else:
                                callback(input_buffer)
                    elif event.key == K_BACKSPACE:
                        input_buffer = input_buffer[:-1]
                    else:
                        input_buffer += event.unicode
                    self.output_lines[-1] = ((prompt, self.text_color), (input_buffer, self.input_color))
                    self.render()
                    pygame.display.update()

    def execute_command(self, command):
        # Store the "Executing" label and the command as a tuple with their colors
        self.custom_print(command)

        if command.lower() == 'recent':
            # Handle 'recent' command
            configRecentProject(self)
        elif command.lower() in {'abyss', 'Abyss'}:
            self.custom_print(ABYSS_VERSION)
        elif command.lower() in {'nebula', 'Nebula'}:
            self.custom_print(NEBULA_VERSION)
        elif command.lower() in {'--v', '--V','-v', '-V', 'version', 'Version'}:
            self.custom_print(ABYSS_VERSION)
            self.custom_print(NEBULA_VERSION)
        elif command.lower() in {'--i', '--I','-i', '-I', 'info', 'INFO'}:
            [self.custom_print(info) for info in ABYSS_INFO]
        elif command.lower() == 'theme':
            self.request_input('Enter the name of the desired theme: ', self.changeTheme)
        elif command.lower() == 'load':
            # Handle 'load' command
            self.request_input('Enter project name: ', configLoadProject)
        elif command.lower() == 'new':
            # Handle 'new' command
            self.request_input('Enter new project name: ', self.handle_new_project)
        elif command.lower() == 'exit':
            pygame.quit()
            sys.exit()
        elif command.lower() in {'cls', 'CLS'}:
            self.output_lines.clear()
            self.header()
        elif command.lower() in {'clear', 'Clear'}:
            self.output_lines.clear()
            self.header()
        elif command.lower() == 'nipps':
            self.custom_print(str(Nebula.Display.get_size()[0]))
        else:
            self.custom_print('Invalid Command!')

    def handle_new_project(self, project_name, project_path=None):
        if project_path is None:
            # If the project path is not provided, request it
            self.request_input('Enter project path: ', lambda path: self.handle_new_project(project_name, path))
        else:
            # Once both project name and path are provided, proceed with configuration
            configNewProject(self, project_name, project_path)

    def render(self):
        # Set the window background transparency
        self.window.fill(self.bg_color)
        
        # Calculate the y position for the first line
        y_pos = 10
        
        # Render the output lines
        for parts in self.output_lines:
            # Start x position for the current line
            x_pos = 10
            for text, color in parts:
                text_surface = self.font.render(text, True, color)
                self.window.blit(text_surface, (x_pos, y_pos))
                # Update the x position for the next part of the line
                x_pos += text_surface.get_width()
            # Increment y position for the next line
            y_pos += 20
        
        # Render the input buffer
        input_surface = self.font.render(self.input_buffer, True, self.input_color)
        input_rect = input_surface.get_rect(topleft=(10, self.height - 30))
        self.window.blit(input_surface, input_rect.topleft)

        # Draw the rectangle around the typing area
        typing_area_rect = pygame.Rect(5, self.height - 35, self.width - 10, 30)
        pygame.draw.rect(self.window, self.box_color, typing_area_rect, 2)

        # Render the cursor if visible
        if self.cursor_visible:
            cursor_x = input_rect.topright[0] + 3
            cursor_y = input_rect.topright[1]
            cursor_rect = pygame.Rect(cursor_x, cursor_y, 2, input_rect.height)
            pygame.draw.rect(self.window, self.cursor_color, cursor_rect)


# Terminal settings
themes ={
    "dark": {
        "font_size" : 20,
        "font" : "Consolas",
        "box" : (203, 219, 252),
        "cursor" : (255,255,255),
        "bg_color" : (20, 20, 20, 0),
        "text_color" : (63, 63, 116),
        "exec_color" : (54, 106, 143),
        "input_color" : (118, 66, 138)
    },
    "light": {
        "font_size" : 20,
        "font" : "Consolas",
        "box" : (203, 219, 252),
        "cursor" : (255,255,255),
        "bg_color" : (80, 80, 80, 0),
        "text_color" : (255, 255, 255),
        "exec_color" : (215, 123, 186),
        "input_color" : (99, 155, 255)
    }
}

# Create and run the terminal
Console(800, 600, themes['light']).run()

# Quit Pygame
pygame.quit()
sys.exit()