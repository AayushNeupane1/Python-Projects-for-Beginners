def get_user_input(valid_choices):

    while True:
        user_choice=input("Enter rock, paper, scissors:").lower()

        if user_choice in valid_choices:
            break
        
        print("Oops! That's not a valid move. Please enter rock, paper, or scissors.")

    return user_choice

