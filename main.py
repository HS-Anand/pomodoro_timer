from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
DARK_BG = "#343131"
DARK_FG = "#c7c7c7"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
dark_mode = False

button_style = {
    "font": (FONT_NAME, 14, "bold"),
    "fg": GREEN,
    "bg": GREEN,
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "activebackground": PINK,
    "cursor": "hand2",
    "width": 10,
    "height": 1
}


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps, timer
    if timer:
        window.after_cancel(timer)

    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    window.lift()
    window.wm_attributes("-topmost", 1)

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

    window.after(1000, window.lift)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = "".join("✔" for _ in range(math.floor(reps / 2)))
        check_marks.config(text=marks)


# ---------------------------- DARK/LIGHT MODE TOGGLE ------------------------------- #

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        window.config(bg=DARK_BG)
        title_label.config(bg=DARK_BG, fg=DARK_FG)
        canvas.config(bg=DARK_BG)
        check_marks.config(bg=DARK_BG, fg=DARK_FG)
        start_button.config(bg=DARK_FG, fg="green")
        toggle_button.config(bg=GREEN, fg="green")
        reset_button.config(bg=DARK_FG, fg="green")
    else:
        window.config(bg=YELLOW)
        title_label.config(bg=YELLOW, fg=GREEN)
        canvas.config(bg=YELLOW)
        check_marks.config(bg=YELLOW, fg=GREEN)
        start_button.config(bg=GREEN, fg=GREEN)
        toggle_button.config(bg=GREEN, fg=GREEN)
        reset_button.config(bg=GREEN, fg=GREEN)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", **button_style, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", **button_style, command=reset_timer)
reset_button.grid(column=2, row=2)

toggle_button = Button(text="Toggle Mode", **button_style, command=toggle_mode)
toggle_button.grid(column=1, row=4)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
