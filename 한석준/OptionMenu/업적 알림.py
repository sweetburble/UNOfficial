import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# tkinter 윈도우 생성
root = tk.Tk()
root.withdraw()

# 메시지 박스 생성
messagebox.showinfo(title="업적 달성", message="축하합니다!\n업적을 달성했습니다.")

# 일정 시간 후에 윈도우 종료 함수
def close_window():
    root.destroy()

# 5초 후에 윈도우 종료 함수 호출
root.after(close_window)

# tkinter 메인 루프 실행
root.mainloop()
