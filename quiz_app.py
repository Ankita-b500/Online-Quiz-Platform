import customtkinter as ctk
import json
from PIL import Image

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    quiz_data = json.load(f)


class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pinnacle Quiz Platform")
        self.geometry("450x650")
        ctk.set_appearance_mode("dark")

        # Background Image
        try:
            self.bg_img = ctk.CTkImage(
                light_image=Image.open("bg-image.jpg"),
                dark_image=Image.open("bg-image.jpg"),
                size=(450, 650)
            )

            self.bg_label = ctk.CTkLabel(
                self,
                image=self.bg_img,
                text=""
            )
            self.bg_label.place(x=0, y=0)
        except Exception as e:
            print(f"Background image load error: {e}")

        # Variables
        self.score = 0
        self.index = 0
        self.time_left = 10
        self.timer_running = False

        # Timer Label
        self.lbl_timer = ctk.CTkLabel(
            self,
            text="10 secs",
            font=("Arial", 28, "bold"),
            text_color="#FFD700"
        )
        self.lbl_timer.pack(pady=(40, 20))

        # Question Number
        self.lbl_q_no = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 14)
        )
        self.lbl_q_no.pack(pady=5)

        # Question
        self.lbl_q = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 20),
            wraplength=350,
            fg_color="transparent"
        )
        self.lbl_q.pack(pady=20)

        # Option Buttons
        self.btns = []

        for i in range(3):
            btn = ctk.CTkButton(
                self,
                text="",
                fg_color="#33334d",
                hover_color="#444466",
                border_width=2,
                border_color="#33334d",
                height=50,
                font=("Arial", 16),
                command=lambda i=i: self.check_ans(i)
            )

            btn.pack(
                pady=8,
                padx=40,
                fill="x"
            )

            self.btns.append(btn)

        self.load_q()

    def update_timer(self):
        if not self.timer_running:
            return

        self.lbl_timer.configure(
            text=f"{self.time_left} secs"
        )

        if self.time_left > 0:
            self.time_left -= 1
            self.after(1000, self.update_timer)
        else:
            self.check_ans(-1)

    def load_q(self):

        if self.index < len(quiz_data):

            self.time_left = 10
            self.timer_running = True

            data = quiz_data[self.index]

            self.lbl_q_no.configure(
                text=f"Question {self.index + 1} of {len(quiz_data)}"
            )

            self.lbl_q.configure(
                text=data["q"]
            )

            self.lbl_timer.configure(
                text="10 secs"
            )

            for i in range(3):
                self.btns[i].configure(
                    text=data["o"][i],
                    state="normal",
                    fg_color="#33334d",
                    border_color="#33334d"
                )

            self.update_timer()

        else:
            self.show_results()

    def check_ans(self, idx):

        self.timer_running = False

        correct_ans = quiz_data[self.index]["a"]

        # Score Update
        if idx != -1:
            selected_option = quiz_data[self.index]["o"][idx]

            if selected_option == correct_ans:
                self.score += 1

        # Disable Buttons
        for btn in self.btns:
            btn.configure(state="disabled")

        # Answer Feedback
        for i in range(3):

            option = quiz_data[self.index]["o"][i]

            if option == correct_ans:
                self.btns[i].configure(
                    fg_color="green",
                    border_color="green"
                )

            elif i == idx:
                self.btns[i].configure(
                    fg_color="red",
                    border_color="red"
                )

        self.after(1500, self.next_q)

    def next_q(self):
        self.index += 1
        self.load_q()

    def show_results(self):

        self.timer_running = False

        total_questions = len(quiz_data)
        percentage = (self.score / total_questions) * 100

        # Hide quiz widgets
        self.lbl_timer.pack_forget()
        self.lbl_q_no.pack_forget()
        self.lbl_q.pack_forget()

        for btn in self.btns:
            btn.pack_forget()

        # Results Title
        result_title = ctk.CTkLabel(
            self,
            text="🎉 Quiz Completed!",
            font=("Arial", 28, "bold")
        )
        result_title.pack(pady=(60, 20))

        # Score
        score_label = ctk.CTkLabel(
            self,
            text=f"Score: {self.score}/{total_questions}",
            font=("Arial", 24)
        )
        score_label.pack(pady=10)

        # Percentage
        percent_label = ctk.CTkLabel(
            self,
            text=f"{percentage:.0f}% Correct",
            font=("Arial", 20)
        )
        percent_label.pack(pady=10)

        # Performance Message
        if percentage >= 80:
            msg = "🌟 Excellent Work!"
        elif percentage >= 50:
            msg = "👍 Good Job!"
        else:
            msg = "📚 Keep Practicing!"

        performance_label = ctk.CTkLabel(
            self,
            text=msg,
            font=("Arial", 18)
        )
        performance_label.pack(pady=15)

        # Play Again Button
        replay_btn = ctk.CTkButton(
            self,
            text="🔄 Play Again",
            command=self.restart_quiz
        )
        replay_btn.pack(pady=10)

        # Exit Button
        exit_btn = ctk.CTkButton(
            self,
            text="❌ Exit",
            fg_color="red",
            hover_color="#aa0000",
            command=self.destroy
        )
        exit_btn.pack(pady=10)

    def restart_quiz(self):

        self.destroy()

        app = QuizApp()
        app.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()