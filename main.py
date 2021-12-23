from monkey import Monkey

PATH = "/Users/adriansmith/Documents/Coding Files/chromedriver"

monkey = Monkey(PATH)

# MY MONKEY

# MONKEY MODE            LENGTH SETTINGS(quote length)     LENGTH SETTINGS(words)              LENGTH SETTINGS(seconds)
# 0 == time              0 == all                          0 == 10                             0 == 15
# 1 == words             1 == short                        1 == 25                             1 == 30
# 2 == quote             2 == medium                       2 == 50                             2 == 60
#                        3 == long                         3 == 100                            3 == 120
#                        4 == thick

# TEST OUT THE MONKEY

running = True
while running:
    monkey.menu_choice()
    if monkey.choice_picked == 1:  # set options
        monkey.set_mode()
        monkey.set_length()
        monkey.set_options()
    elif monkey.choice_picked == 2:  # start typing
        if monkey.mode == 0:
            monkey.type_for_time()
        elif monkey.mode == 1:
            monkey.type_n_words()
        elif monkey.mode == 2:
            monkey.type_quote()
    elif monkey.choice_picked == 3:  # another race
        monkey.do_another_test()
    elif monkey.choice_picked == 4:  # quit
        monkey.bye()
        running = False
