import tkinter as tk
import random
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent
import threading
from gtts import gTTS
import os


# Lists of options
#("", ""),
options = [
    ("have more time", "have more money"),
    ("talk to animals", "speak all languages"),
    ("win the lottery", "live twice as long"),
    ("be without internet", "be without phone"),
    ("lose vision", "lose hearing"),
]
current_option_index = 0

client: TikTokLiveClient = TikTokLiveClient(unique_id="@Your TikTok ID")

# Creating the main application
class WouldYouRatherGame(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Would You Rather Game")
        self.geometry("600x300")
        self.configure(bg="gray15")
        self.red_votes = 0
        self.blue_votes = 0
        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        self.question_label = tk.Label(self, text="Would you rather:", font=("Helvetica", 42))
        self.question_label.pack(pady=20)

        self.red_frame = tk.Frame(self, bg="red")
        self.red_frame.pack(pady=20)

        self.option1_label = tk.Label(self.red_frame, text="Option Red", bg="red", fg="white", font=("Helvetica", 32))
        self.option1_label.pack()

        self.option1_votes_label = tk.Label(self.red_frame, text=" comment 'red' - Votes: 0", bg="red", fg="white", font=("Helvetica", 22))
        self.option1_votes_label.pack()

        self.or_label = tk.Label(self, text="or", font=("Helvetica", 30))
        self.or_label.pack()

        self.blue_frame = tk.Frame(self, bg="blue")
        self.blue_frame.pack(pady=20)

        self.option2_label = tk.Label(self.blue_frame, text="Option Blue", bg="blue", fg="white", font=("Helvetica", 32))
        self.option2_label.pack()

        self.option2_votes_label = tk.Label(self.blue_frame, text=" comment 'blue' - Votes: 0", bg="blue", fg="white", font=("Helvetica", 22))
        self.option2_votes_label.pack()

        self.timer_label = tk.Label(self, text="", font=("Helvetica", 25))
        self.timer_label.pack()

    def start_game(self):
        self.remaining_time = 35
        self.update_options()
        self.update_timer()

    def update_options(self):
        global current_option_index
        if current_option_index == len(options):
            current_option_index = 0
        red_option, blue_option = options[current_option_index]
        current_option_index += 1

        self.option1_label.config(text=red_option)
        self.option2_label.config(text=blue_option)

        #Speak the options using gTTS
        speak_text = f"Would you rather {red_option} or {blue_option}"
        tts = gTTS(text=speak_text, lang='en', slow=False)
        tts.save("question.mp3")
        os.system("start question.mp3")

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Time left: {self.remaining_time} seconds")
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.show_result()
            self.after(5000, self.restart_game)

    def vote_red(self):
        self.red_votes += 1
        self.option1_votes_label.config(text=f" comment 'red' - Votes: {self.red_votes}")

    def vote_blue(self):
        self.blue_votes += 1
        self.option2_votes_label.config(text=f" comment 'blue' - Votes: {self.blue_votes}")

    def show_result(self):
        self.option1_label.config(state=tk.DISABLED)
        self.option2_label.config(state=tk.DISABLED)

        if self.red_votes > self.blue_votes:
            result = "Red option wins!"
        elif self.red_votes < self.blue_votes:
            result = "Blue option wins!"
        else:
            result = "It's a tie!"

        self.question_label.config(text=result)

        self.timer_label.config(text=f"Red votes: {self.red_votes}\nBlue votes: {self.blue_votes}")

        #Speak the result using gTTS
        speak_text = result
        tts = gTTS(text=speak_text, lang='en', slow=False)
        tts.save("result.mp3")
        os.system("start result.mp3")

    def restart_game(self):
        self.red_votes = 0
        self.blue_votes = 0
        self.option1_label.config(state=tk.NORMAL)
        self.option2_label.config(state=tk.NORMAL)
        self.option1_votes_label.config(text="comment 'red' - Votes: 0")
        self.option2_votes_label.config(text=" comment 'blue' - Votes: 0")
        self.question_label.config(text="Would you rather:")
        self.timer_label.config(text="")
        self.start_game()


# Run the game and TikTokLive
@client.on('comment')
def on_comment(event: CommentEvent):
    text = f'{event.comment}'
    if text.lower() == "red":
        app.vote_red()
    if text.lower() == "blue":
        app.vote_blue()
    print(text)

def run_tiktok_client():
    client.run()

app = WouldYouRatherGame()

# Start the TikTokLive client in a separate thread
client_thread = threading.Thread(target=run_tiktok_client)
client_thread.daemon = True
client_thread.start()

#start the game
app.mainloop()
