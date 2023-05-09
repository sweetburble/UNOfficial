import tkinter as tk
from datetime import datetime
from tkinter import messagebox


# tkinter 윈도우 생성
root = tk.Tk()
root.withdraw()

# 메시지 박스 생성
messagebox.showinfo(title="업적 달성", message="축하합니다!\n업적을 달성했습니다.")

# tkinter 윈도우 종료
root.destroy()
