from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_card = {}
to_learn = {}

# TODO: Read CSV file.
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = pandas.DataFrame.to_dict(data, orient="records")

# ---------------------------- FLIP THE CARDS ------------------------------- #


def flip_card():

    canvas.itemconfig(card_background, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


# ---------------------------- DISPLAY NEXT CARD ------------------------------- #


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    stored_data = pandas.DataFrame(to_learn)
    stored_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
# TODO: Creating window.
window = Tk()
window.title("Flashy Card")
window.config(padx=60, pady=30, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# TODO: Creating canvas.
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 100, fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# TODO: Creating buttons.
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
