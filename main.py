from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

score = 0
current_card = {}
to_learn = []
countdown = 3
countdown_timer = None


#  LOAD DATA #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv("data/arabic_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


#  FUNCTIONS  #

def next_card():
    global current_card, flip_timer, countdown, countdown_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
        flip_timer = None

    if countdown_timer is not None:
        window.after_cancel(countdown_timer)
        countdown_timer = None

    # Check if all cards are finished
    if len(to_learn) == 0:
        canvas.itemconfig(card_background, image=card_back_imag)
        canvas.itemconfig(card_title, text="Finished!", fill="white")
        canvas.itemconfig(card_word, text=f"Final Score: {score}", fill="white")
        return

    current_card = random.choice(to_learn)

    # Show Arabic side
    canvas.itemconfig(card_background, image=card_front_imag)
    canvas.itemconfig(card_title, text="Arabic", fill="black")
    canvas.itemconfig(card_word, text=current_card["Arabic"], fill="black")

    # Start countdown
    countdown = 3
    canvas.itemconfig(timer_text, text="Timer: 3")
    countdown_timer = window.after(0, update_countdown)

    # Flip after 3 seconds
    flip_timer = window.after(3000, flip_card)

def update_countdown():
    global countdown, countdown_timer

    if countdown > 0:
        canvas.itemconfig(timer_text, text=f"Timer: {countdown}")

        countdown -= 1
        countdown_timer = window.after(1000, update_countdown)

    else:
        canvas.itemconfig(timer_text, text="Timer: 0")

def flip_card():
    canvas.itemconfig(card_background, image=card_back_imag)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(timer_text, text="Timer: 0")


def is_known():
    global score, flip_timer, countdown_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)

    if countdown_timer is not None:
        window.after_cancel(countdown_timer)

    score += 1
    canvas.itemconfig(score_text, text=f"Score: {score}")

    canvas.itemconfig(card_background, image=card_back_imag)
    canvas.itemconfig(card_title, text="Correct!", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


    to_learn.remove(current_card)

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    window.after(1500, next_card)


def dont_know():
    global flip_timer, countdown_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
        flip_timer = None

    if countdown_timer is not None:
        window.after_cancel(countdown_timer)
        countdown_timer = None

    canvas.itemconfig(card_background, image=card_back_imag)
    canvas.itemconfig(card_title, text="Incorrect!", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


    window.after(1500, next_card)


# UI SETUP #

window = Tk()
window.title("Flashy")
window.config(padx=20, pady=10, bg=BACKGROUND_COLOR)


#  CANVAS  #

canvas = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)

canvas.grid(column=0, row=0, columnspan=2)


# Card images
card_front_imag = PhotoImage(file="images/card_front.png")
card_back_imag = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(
    400,
    263,
    image=card_front_imag
)


# Card title
card_title = canvas.create_text(
    400,
    150,
    text="Arabic",
    font=("Arial", 40, "bold"),
    fill="black"
)


# Card word
card_word = canvas.create_text(
    400,
    263,
    text="word",
    font=("Arial", 60, "bold"),
    fill="black"
)
# Timer
timer_text = canvas.create_text(
    700,
    50,
    text="Timer: 3",
    font=("Arial", 20, "bold"),
    fill="black"
)


# Score
score_text = canvas.create_text(
    100,
    50,
    text="Score: 0",
    font=("Arial", 20, "bold"),
    fill="black"
)



# BUTTON IMAGES #

right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")


#  BUTTONS #

right_button = Button(
    image=right_img,
    highlightthickness=0,
    command=is_known
)

right_button.grid(column=1, row=1)


wrong_button = Button(
    image=wrong_img,
    highlightthickness=0,
    command=dont_know
)

wrong_button.grid(column=0, row=1)



flip_timer = None
next_card()

window.mainloop()