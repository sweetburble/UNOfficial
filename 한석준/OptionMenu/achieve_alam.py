import tkinter as tk
from tkinter import messagebox

def check_achievement():
    # 업적 달성 여부를 확인하는 로직을 작성하세요
    achievement_achieved = True

    if achievement_achieved:
        # 알림창을 표시합니다.
        messagebox.showinfo("알림", "업적이 달성되었습니다!")

# 메인 윈도우를 생성합니다.
root = tk.Tk()
root.withdraw()  # 윈도우를 숨깁니다.

# 업적을 체크하는 함수를 호출합니다.
check_achievement()

# 메인 루프를 시작합니다.
root.mainloop()
