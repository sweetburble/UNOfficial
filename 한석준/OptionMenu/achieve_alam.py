import achievement
import tkinter as tk
from tkinter import messagebox

def check_achievement():
    # 업적 달성 여부를 확인하는 로직을 작성하세요
    achievement_achieved = True

    if achievement_achieved:
        # 업적 아이콘 경로 가져오기
        achievement_icon_path = achievement.icon

        # 알림창을 표시합니다.
        root = tk.Tk()
        root.withdraw()  # 윈도우를 숨깁니다.
        messagebox.showinfo("알림", f"업적이 달성되었습니다!\n달성한 업적: {achievement.name}", icon=achievement_icon_path)
        root.destroy()

# 메인 윈도우를 생성합니다.
root = tk.Tk()
root.withdraw()  # 윈도우를 숨깁니다.

# 아이콘 파일 경로를 설정합니다.
icon_path = "img\\achieve.ico"

# 아이콘을 설정합니다.
root.iconbitmap(icon_path)

# 업적을 체크하는 함수를 호출합니다.
check_achievement()

# 메인 루프를 시작합니다.
root.mainloop()
