def determine_winner(user_choice, computer_choice):

    if user_choice == computer_choice:
        result = "Draw!"
    elif user_choice == "rock" and computer_choice == "scissors":
        result = "You win!"
    elif user_choice == "scissors" and computer_choice == "paper":
        result = "You win!"
    elif user_choice == "paper" and computer_choice == "rock":
        result = "You win!"
    else:
        result = "You lose!"

    return(result)

