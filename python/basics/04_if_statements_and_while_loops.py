

program_is_running=True


while program_is_running:


    # Get user name and age
    user_name = input("Please enter your name: ")
    user_age = int(input("Please enter your age: "))



    # Evaluate input, and output answer to user
    if user_age < 18:
        print("You are too young to drive a car, " + user_name)
    elif user_age > 99:
        print("You are too old to drive a car, " + user_name)
    else:
        print("You are old enough to drive a car, " + user_name)



    # Ask user if it's time to exit the program
    user_command = input("Type exit to terminate program: ")

    if user_command == "exit":
        program_is_running = False




print("Goodbye")


