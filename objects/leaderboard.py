import time
import pygame
import pygame_menu

from objects.constants import COMSSA_COLOR
from objects.user_info import UserInfo


class Leaderboard:
    def __init__(self):
        self.leaderboard = []
        self.is_active = False

    def get_leaderboard(self):
        return self.leaderboard

    def write_leaderboard_to_file(self, user_info, score):
        leaderboard = self.read_leaderboard_from_file()
        leaderboard.append((user_info, int(score)))
        self.leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
        with open("leaderboard.txt", "w") as f:
            for user_info, score in self.leaderboard:
                f.write(f"{user_info.student_id.strip()},{user_info.discord_id.strip()},{score}\n")

    def read_leaderboard_from_file(self):
        try:
            with open("leaderboard.txt", "r") as f:
                leaderboard = []
                for line in f:
                    student_id, discord_id, score = line.split(",")
                    user_info = UserInfo(student_id, discord_id)
                    leaderboard.append((user_info, int(score)))
                return leaderboard
        except FileNotFoundError:
            return []

    def fill_leaderboard(self, surface, score):
        self.is_active = True
        screen_width, screen_height = pygame.display.get_surface().get_size()

        menu = pygame_menu.Menu("Leaderboard", screen_width * 0.7, screen_height * 0.5, theme=pygame_menu.themes.THEME_BLUE)
        user_info = UserInfo()
        menu.add.label("Enter your Student/Staff ID")
        menu.add.text_input("", onchange=user_info.set_student_id, input_underline_len=20, maxchar=20)
        
        menu.add.label("Enter your Discord ID/Tag")
        menu.add.text_input("", onchange=user_info.set_discord_id, input_underline_len=20, maxchar=20)

        menu.add.vertical_margin(20)

        menu.add.button("Exit", lambda: self._exit_menu(user_info, score))
        
        while self.is_active:
            # Add ComSSA color background with surface.fill
            menu.mainloop(surface, disable_loop=True, bgfun=lambda: surface.fill(COMSSA_COLOR))
            pygame.display.flip()

    def _exit_menu(self, user_info=None, score=None):
        if user_info is not None and score is not None and len(user_info.student_id) > 0 and len(user_info.discord_id) > 0 and score > 0:
            self.write_leaderboard_to_file(user_info, score)
        self.is_active = False

    def draw_leaderboard(self, surface):
        self.is_active = True
        screen_width, screen_height = pygame.display.get_surface().get_size()

        menu = pygame_menu.Menu("Top 10 Leaderboard", screen_width * 0.8, screen_height * 0.8, theme=pygame_menu.themes.THEME_BLUE)

        table = menu.add.table(table_id='my_table', font_size=25)
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(['Student ID', 'Discord ID', 'Score'],
                    cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
        leaderboard = self.read_leaderboard_from_file()
        if len(leaderboard) > 10:
            leaderboard = leaderboard[:10]
        for user_info, score in leaderboard:
            table.add_row([user_info.student_id, user_info.discord_id, score], cell_align=pygame_menu.locals.ALIGN_CENTER)
        
        menu.add.vertical_margin(20)
        menu.add.button("Exit", lambda: self._exit_menu())
        while self.is_active:
            # Add ComSSA color background with surface.fill
            menu.mainloop(surface, disable_loop=True, bgfun=lambda: surface.fill(COMSSA_COLOR))
            pygame.display.flip()
