import tkinter as tk
import random

choices = ["Rock", "Paper", "Scissors"]

user_score = 0
comp_score = 0
round_no = 0
max_rounds = 7
player_name = ""

def start_game():
    global player_name, user_score, comp_score, round_no
    player_name = entry_name.get().strip()
    if player_name == "":
        player_name = "Player"
    
    user_score = 0
    comp_score = 0
    round_no = 0
    
    entry_name.pack_forget()
    btn_start.pack_forget()
    
    label_title.config(text=f"Welcome {player_name}! Best of 7 🎮")
    btn_rock.pack(pady=5)
    btn_paper.pack(pady=5)
    btn_scissors.pack(pady=5)
    label_result.pack(pady=15)
    label_score.pack(pady=10)
    btn_play_again.pack_forget()
    
    label_score.config(text=f"Score -> {player_name}: 0  |  Computer: 0")
    label_result.config(text="")

def play(user_choice):
    global user_score, comp_score, round_no
    
    if round_no >= max_rounds or user_score >= 4 or comp_score >= 4:
        return 
    
    round_no += 1
    computer_choice = random.choice(choices)
    
    if user_choice == computer_choice:
        result = "🤝 It's a Tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = f"🎉 {player_name} Wins!"
        user_score += 1
    else:
        result = "💻 Computer Wins!"
        comp_score += 1
    
    label_result.config(
        text=f"Round {round_no} of {max_rounds}\n"
             f"{player_name}'s choice: {user_choice}\n"
             f"Computer's choice: {computer_choice}\n\n{result}"
    )
    label_score.config(text=f"🏆 Score -> {player_name}: {user_score}  |  Computer: {comp_score}")
    
    if round_no == max_rounds or user_score == 4 or comp_score == 4:
        if user_score > comp_score:
            final = f"🥳 {player_name} WINS the Match!"
        elif comp_score > user_score:
            final = "💻 Computer WINS the Match!"
        else:
            final = "🤝 It's a DRAW!"
        
        label_result.config(text=label_result.cget("text") + f"\n\nFinal Result: {final}")
        disable_buttons()
        btn_play_again.pack(pady=10)

def disable_buttons():
    btn_rock.config(state="disabled")
    btn_paper.config(state="disabled")
    btn_scissors.config(state="disabled")

def reset_game():

    btn_rock.config(state="normal")
    btn_paper.config(state="normal")
    btn_scissors.config(state="normal")
    
    label_result.config(text="")
    label_score.config(text="")
    
    label_title.config(text="Enter your name to start the game:")
    entry_name.pack(pady=5)
    btn_start.pack(pady=5)
    btn_play_again.pack_forget()
    
root = tk.Tk()
root.title("Rock Paper Scissors - Best of 7")
root.geometry("420x460")
root.config(bg="#f0f5f5")

label_title = tk.Label(root, text="Enter your name to start the game:", font=("Arial", 12, "bold"), bg="#f0f5f5")
label_title.pack(pady=10)

entry_name = tk.Entry(root, font=("Arial", 12), justify="center")
entry_name.pack(pady=5)

btn_start = tk.Button(root, text="▶ Start Game", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=start_game)
btn_start.pack(pady=5)

btn_rock = tk.Button(root, text="🪨 Rock", font=("Arial", 11, "bold"), width=15, bg="#d9ead3", command=lambda: play("Rock"))
btn_paper = tk.Button(root, text="📄 Paper", font=("Arial", 11, "bold"), width=15, bg="#cfe2f3", command=lambda: play("Paper"))
btn_scissors = tk.Button(root, text="✂️ Scissors", font=("Arial", 11, "bold"), width=15, bg="#f4cccc", command=lambda: play("Scissors"))

label_result = tk.Label(root, text="", font=("Arial", 11), bg="#f0f5f5")
label_score = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f5f5")

btn_play_again = tk.Button(root, text="🔄 Play Again", font=("Arial", 12, "bold"), bg="#ff9800", fg="white", command=reset_game)

root.mainloop()