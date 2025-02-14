class UserInfo:
    def __init__(self, student_id="", discord_id=""):
        self.student_id = student_id
        self.discord_id = discord_id

    def get_user_info(self):
        return self.student_id, self.discord_id
    
    def set_student_id(self, student_id):
        self.student_id = student_id
    
    def set_discord_id(self, discord_id):
        self.discord_id = discord_id
