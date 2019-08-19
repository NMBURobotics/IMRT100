shopping = ["banana", "potato", "candy", "pizza"]
print(shopping)
print("length of shopping list:", len(shopping))
print(shopping[0])
print(shopping[1])
print(shopping[-1])

my_list = ["banana", 4, True, [2,4,1], -9.99]
print(my_list)


# prints 2x newlines to make some space in the output
print(2*"\n") 


things_to_watch = ["Cops", "Sinnasnekker'n", "MacGyver"]
print(things_to_watch)

things_to_watch[2] = "Batman"
print(things_to_watch)

things_to_watch.append("Home and away")
print(things_to_watch)

suggested_shows = ["Beat for Beat", "QuizDan"]
things_to_watch.extend(suggested_shows)
print(things_to_watch)

watch_on_monday = things_to_watch[0:2]
print(watch_on_monday)

for i in range(len(things_to_watch)):
    print(things_to_watch[i])

for show in things_to_watch:
    print(show)
