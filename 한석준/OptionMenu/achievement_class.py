class Achievement:
    def __init__(self, name):
        self.name = name
        self.achieved = False
        self.achieved_time = None

    def set_achieved(self):
        self.achieved = True
        self.achieved_time = datetime.datetime.now()

class AchievementSystem:
    def __init__(self):
        self.achievements = []

    def add_achievement(self, achievement):
        self.achievements.append(achievement)

    def check_achievements(self):
        for achievement in self.achievements:
            if not achievement.achieved:
                # 여기에서 업적 달성을 확인할 조건을 추가하세요
                if 조건:
                    achievement.set_achieved()

achievement_1 = Achievement('Singleplay_win')
achievement_2 = Achievement('storymod_1_win')
achievement_3 = Achievement('storymod_2_win')
achievement_4 = Achievement('storymod_3_win')
achievement_5 = Achievement('storymod_4_win')
achievement_6 = Achievement('fast_win')
achievement_7 = Achievement('handicap')
achievement_8 = Achievement('win_afterUNO')
achievement_9 = Achievement('apply_color_weakness')
achievement_10 = Achievement('open_setting')
achievement_11 = Achievement('open_storymod')

achievement_system = AchievementSystem()
achievement_system.add_achievement(achievement_1)
achievement_system.add_achievement(achievement_2)
achievement_system.add_achievement(achievement_3)
achievement_system.add_achievement(achievement_4)
achievement_system.add_achievement(achievement_5)
achievement_system.add_achievement(achievement_6)
achievement_system.add_achievement(achievement_7)
achievement_system.add_achievement(achievement_8)
achievement_system.add_achievement(achievement_9)
achievement_system.add_achievement(achievement_10)
achievement_system.add_achievement(achievement_11)