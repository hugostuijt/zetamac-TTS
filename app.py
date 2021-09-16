import pyttsx3
from numpy.random import randint
import tkinter as tk

# initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 200)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def say(text):
    text = text
    engine.say(text)
    # play the speech
    engine.runAndWait()


# random addition problem
def addition():
    operator = 'plus'   # operator is spoken by the voice engine

    num1 = randint(2, 101)
    num2 = randint(2, 101)
    ans = num1 + num2

    return [num1, num2, ans, operator]


def subtraction():
    operator = 'minus'

    num1 = randint(2, 101)
    num2 = randint(2, 101)
    ans = num1 - num2

    return [num1, num2, ans, operator]


def multiplication():
    operator = 'times'

    num1 = randint(2, 13)
    num2 = randint(2, 101)
    ans = num1 * num2

    return [num1, num2, ans, operator]


def division():
    operator = 'divided by'

    num1 = randint(2, 13)
    num2 = randint(2, 101)
    ans = num1 * num2

    return [ans, num1, num2, operator]  # answer is now reversed


# Chooses randomly between a +,-,*,/ problem and calls the respective function. Returns the problem and answer.
def get_problem():
    switcher = {
        1: addition,
        2: subtraction,
        3: multiplication,
        4: division
    }

    # choose addition, subtraction, multiplication, division
    r = randint(1, 5)
    num1, num2, ans, operator = switcher.get(r)()

    text = str(num1) + ' ' + operator + ' ' + str(num2)
    return text, float(ans)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.time_over = False
        self.master.bind('<Return>', self.check_ans)    # Hit enter checks answer and moves to next problem
        self.pack()
        self.create_widgets()

    def check_ans(self, event):
        if self.time_over:
            return
        entry = self.entry_box.get()
        self.entry_box.delete(0, 'end')
        try:
            entry = float(entry)
        except:
            pass # if entry is not a number, answer will be incorrect.
        if self.ans == entry:
            self.score += 1
            self.score_label['text'] = self.score
            self.new_problem()

        else:
            text = 'wrong, ' + self.text
            say(text)

    def countdown(self, count):
        self.time_label['text'] = 'Time: ' + str(count)
        if count > 0:
            self.master.after(1000, self.countdown, count-1)
        else:
            self.time_over = True
            say('Time over, your score is ' + str(self.score))
    
    def start(self):
        self.score = 0
        self.time_over = False
        self.score_label['text'] = self.score
        self.countdown(180)
        self.start_button['text'] = 'Restart'
        self.new_problem()

    def new_problem(self):
        text, ans = get_problem()

        self.text = text
        self.ans = ans

        say(text)

    def create_widgets(self):
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start"
        self.start_button["command"] = self.start
        self.start_button.pack(side="top")

        self.entry_box = tk.Entry(self)
        self.entry_box.pack(side='top')

        self.time_label = tk.Label(self)
        self.time_label['text'] = 'Time: '
        self.time_label.pack(side='bottom')

        self.score_label = tk.Label(self)
        self.score_label['text'] = ''
        self.score_label.pack(side='bottom')


root = tk.Tk()
# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen
# calculate x and y coordinates for the Tk root window
w = 250
h = 250
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

app = Application(master=root)
app.master.title('Zetamac')
app.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


app.mainloop()
