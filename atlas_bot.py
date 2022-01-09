# imports
from inputimeout import inputimeout, TimeoutOccurred
import random
import json
import sys

# open json file
file = open('places.json', 'r')
data = json.loads(file.read())

# global variables

# load json data into variables
a = data["a"]
b = data["b"]
c = data["c"]
d = data["d"]
e = data["e"]
f = data["f"]
g = data["g"]
h = data["h"]
i = data["i"]
j = data["j"]
k = data["k"]
l = data["l"]
m = data["m"]
n = data["n"]
o = data["o"]
p = data["p"]
q = data["q"]
r = data["r"]
s = data["s"]
t = data["t"]
u = data["u"]
v = data["v"]
w = data["w"]
x = data["x"]
y = data["y"]
z = data["z"]

# miscellaneous
all_letters = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
all_letter_string = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
done_places = []
invalid_count = 0

def takeInput():
    # place=None
    try:
        place = inputimeout(prompt='Your place : ', timeout=10)

    except TimeoutOccurred:
        global invalid_count

        #send invalid count message and increase count
        if invalid_count < 1:
            print("You have to enter a place withing 10 seconds. If you don't, then your invalid count will increase by 1. If invalid count reaches 3, you lose.")
        invalid_count = invalid_count+1
        print("Invalid count : {}".format(invalid_count))
        
        #check if invalid count == 3
        if invalid_count == 3:
            print('You lost')
            sys.exit()
        
        #else, take input
        place=takeInput()

    else:
        place = place.lower()

        #check if input is a whitespace or if it is nothing
        while place == '':
            print("Plese enter a place")
            place = takeInput()
        while place.isspace():
            print("Please enter a place.")
            place = takeInput()

        # check if user wants to quit
        if place == 'quit' or place == 'pass':
            print("You lost")
            sys.exit()

        #check if place is invalid
        while place[-1] not in all_letter_string:
            print('This is not a place. Enter another place.')
            place = takeInput()

        #check if place is already done
        while place in done_places:
            print('This place is done. Enter another place.')
            place = takeInput()

        # check if place exists in database
        while place not in globals()[place[0]]:
            print('This is not a place. Enter another place.')
            place = takeInput()

        if place[0] == ai_place_last:
            for For in all_letters:
                if place in For:
                    For.remove(place)

    return place

def takeInput():
    global invalid_count

    try:
        place = inputimeout(prompt='Your place : ', timeout=10)

    except TimeoutOccurred:
        #send invalid count message and increase count
        if invalid_count < 1:
            print("You have to enter a place withing 10 seconds. If you don't, then your invalid count will increase by 1. If invalid count reaches 3, you lose.")
        invalid_count = invalid_count+1
        print("Invalid count : {}".format(invalid_count))
        
        #check if invalid count == 3
        if invalid_count == 3:
            print('You lost')
            sys.exit()
        
        #else, take input
        place=takeInput()

    else:
        place = place.lower()

        #check if input is a whitespace or if it is nothing
        while place == '':
            print("Plese enter a place")
            place = takeInput()
        while place.isspace():
            print("Please enter a place.")
            place = takeInput()

        # check if user wants to quit
        if place == 'quit' or place == 'pass':
            print("You lost")
            sys.exit()

        # check if place is from correct letter
        if place[0] != ai_place_last:
            invalid_count += 1
            print(f'Your place should start from {ai_place_last.upper()}.')
            print(f'Invalid Place Count = {invalid_count}')
            print(ai_place)

        #check if place is invalid
        while place[-1] not in all_letter_string:
            print('This is not a place. Enter another place.')
            place = takeInput()

        #check if place is already done
        while place in done_places:
            print('This place is done. Enter another place.')
            place = takeInput()

        # check if place exists in database
        while place not in globals()[place[0]]:
            print('This is not a place. Enter another place.')
            place = takeInput()

    return place

# main code starts here
if __name__ == "__main__":

    # global invalid_count
    invalid_count = 0

    # greetings
    print("Let's play Atlas...")
    print("I will start the game by entering a place.\n")

    # first place
    first_letter = random.choice(all_letters)
    first_ai_place = random.choice(first_letter)
    ai_place_last = first_ai_place[-1].lower()
    print('A.I. Place - ', end='')
    print(first_ai_place.title())
    print('Your place should start from',ai_place_last.upper()+'\n')
    first_letter.remove(first_ai_place)

    done_places.append(first_ai_place.lower())

    while True:

        # invalid count checker
        if invalid_count == 3:
            print('You lose')
            sys.exit()

        # take input from user
        ai_place = 'If you enter 3 invalid places you will lose'
        place = takeInput()
<<<<<<< HEAD
        
        # check if place entered starts from the right letter or not
        if place[0] != ai_place_last:
            invalid_count += 1
            print(f'Your place should start from {ai_place_last.upper()}.')
            print(f'Invalid Place Count = {invalid_count}')
            print(ai_place)

        # if place entered is correct and all, then run this
        else:
            last = place[-1]
            done_places.append(place)
            place_given = False

            for cur_letter in all_letters:
                if last == ([i for i, var in locals().items() if var == cur_letter][0]) and cur_letter != []:
                    ai_place = random.choice(cur_letter)
                    cur_letter.remove(ai_place)
                    done_places.append(ai_place)
                    place_given = True

                    if ai_place == 'If you enter 3 invalid places you will lose':
                        pass
                    else:
                        print('\nBot\'s Place : '+ai_place.title())
                        # print(ai_place.title())
                        last_ai_place = ai_place
                        ai_place_last = last_ai_place[-1].lower()
                        print('Your place should start from '+ai_place_last.upper()+'\n')
                        done_places.append(ai_place.lower())

            if place_given == False:
                print("You Won")
                sys.exit()

    # print('Done places -',done_places)
=======

        if place[0] == ai_place_last:
            for For in all_letters:
                if place in For:
                    For.remove(place)

        # if place entered is correct and all, then run this
        last = place[-1]
        done_places.append(place)
        place_given = False
        for cur_letter in all_letters:
            if last == ([i for i, var in locals().items() if var == cur_letter][0]) and cur_letter != []:
                ai_place = random.choice(cur_letter)
                cur_letter.remove(ai_place)
                done_places.append(ai_place)
                place_given = True
                if ai_place == 'If you enter 3 invalid places you will lose':
                    pass
                else:
                    print('\nBot\'s Place : '+ai_place.title())
                    last_ai_place = ai_place
                    ai_place_last = last_ai_place[-1].lower()
                    print('Your place should start from '+ai_place_last.upper()+'\n')
                    done_places.append(ai_place.lower())
        if place_given == False:
            print("You Won")
            sys.exit()
>>>>>>> master
