from tkinter import *
import random
import pandas as pd

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
TOP_TEXT = ("Ariel", 40, "italic")
BOTTOM_TEXT = ("Ariel", 60, "bold")
PINYIN_TEXT = ("Ariel", 40, "italic")
current_card = {}
to_learn = {}
# ---------------------------- Functions ------------------------------- #

try:
    data = pd.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_date = pd.read_csv("./data/CN_noun_list.csv")
    to_learn = original_date.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(old_img, image=card_front)
    canvas.itemconfig(card_top, text="Chinese", fill="black")
    canvas.itemconfig(card_word, fill="black", text=current_card["Simplified"])
    canvas.itemconfig(card_bottom, fill="black", text=current_card["Pinyin"])
    flip_timer = window.after(3000, flip_card)


def remove_from_dict():
    to_learn.remove(current_card)
    df = pd.DataFrame(to_learn)
    df.to_csv('words_to_learn.csv', encoding='utf-8-sig', mode="w", index=False, header=True)
    next_card()


def flip_card():
    # English card side
    canvas.itemconfig(old_img, image=card_back)
    canvas.itemconfig(card_top, text="English", fill="white")
    canvas.itemconfig(card_word, fill="white", text=current_card["English Translation"])
    canvas.itemconfig(card_bottom, fill="white", text="")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)
#Canvas
#Chinese card side
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
old_img = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
card_top = canvas.create_text(400, 150, text="Chinese", font=TOP_TEXT)
card_word = canvas.create_text(400, 263, text="", font=BOTTOM_TEXT)
card_bottom = canvas.create_text(400, 376, text="", font=PINYIN_TEXT)

#English card side
card_back = PhotoImage(file="./images/card_back.png")

#Buttons
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, bg=BACKGROUND_COLOR, command=remove_from_dict)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
