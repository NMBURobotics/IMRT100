




# COMMENTS

# This is a single-line comment. Comments are ignored by the iterpreter 

'''
This is a
multi-line comment
sometimes one line is not enough.
Although comments can be very useful sometimes,
it is better to write human-readable code rather than writing lots of comments everywhere
'''




# IMPORTS
# Here we import a module that we will need
# Modules are files that contain Python definitions and statements
# Think of them like different toolboxes
# Here we import a module called time.
import time




# PRINTS
print("This will be printed to the shell")




# VARIABLES
a = 10
b = 2.5
c = a + b
d = a * b
e = a / b
f = "I am a string"
g = True
h = False
print("\na:", a, " b:", b, " c:", c, " d:", d, " e:", e, " f:", f, " g:", g, " h:", h)
a = a+10 # the long way of writing
print("we changed a! a:", a)
a += 10 # slightly more compressed way of writing
print("we changed a again! a:", a)
print("g and h:", g and h) # only True if both are True
print("g or h:", g or h) # True if at least one is True




# IF STATEMENTS
print("\nNow we'll take a look at an if statement")

secret_number = 4
user_guess = int(input("Guess a number between 1-10: "))

if (user_guess == secret_number):
    print("You guessed the secret number!")
    
elif user_guess < 1 or 10 < user_guess:
    print("Your guess is outside the legal range.")
    
else:
    print("That wasn't the secret number. Better luck next time!")

    


# FOR LOOP
print("\nNow we'll take a look at a for loop") 

# This is a for loop.
# Our example will print "Hello world" followed by the value of i 10 times.
# i starts out as 0, and is incremented by 1 for each run through the loop.
for i in range(10):
    print("Hello world", i)




# WHILE LOOP
print("\nNow we'll take a look at a while loop")

# A while loop will execute as long as a condition holds true
# In this the loop will continue executing as long as the variable talking_to_user is True
# Inside the example loop, we request input from the user, then we print the input back to the shell.
# This is repeated until the user inputs "stop". If the user types "stop"
# we change the variable talking_to_user from True to False, and we will exit the loop

talking_to_user = True

while (talking_to_user):
    user_input = input('Type "stop" to stop: ')
    if user_input == "stop":
        talking_to_user = False
    else:
        print('You wrote "' + user_input + '"')




# TIME
print("Now we will wait for 6 seconds")
time.sleep(6)
print("Done waiting")
