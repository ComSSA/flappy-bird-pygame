import pygame
import pygame_menu

from objects.user_info import UserInfo


class Leaderboard:
    def __init__(self):
        self.leaderboard = []
        self.is_active = True

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

    def draw_leaderboard(self, surface, score):
        menu = pygame_menu.Menu("Leaderboard", 200, 300, theme=pygame_menu.themes.THEME_BLUE)
        user_info = UserInfo()
        menu.add.text_input("Student ID", default="", onchange=user_info.set_student_id)
        menu.add.text_input("Discord ID", default="", onchange=user_info.set_discord_id)
        menu.add.button("Exit", lambda: self._exit_menu(user_info, score))
        while self.is_active:
            menu.mainloop(surface, disable_loop=True)
            pygame.display.flip()

    def _exit_menu(self, user_info, score):
        self.write_leaderboard_to_file(user_info, score)
        self.is_active = False


