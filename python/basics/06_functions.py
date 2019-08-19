# A function
def my_function():
    print("Hello from a very simple function!")
    

# A function that takes an argument
def hello_world_printer(lines_to_print):
    for i in range(lines_to_print):
        print("Hello world")
            
                
# A function that takes two arguments and retuns an int
def compute_rectangle_area(side_a, side_b):
    area = side_a * side_b
    return area
                      

# Program starts here
if __name__ == '__main__':
    
    print("We are here!")

    my_function()

    hello_world_printer(4)

    my_rectangle_area = compute_rectangle_area(2, 6)
    print(my_rectangle_area)
