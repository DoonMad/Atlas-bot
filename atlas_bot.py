# imports
import random
import json
import discord
import asyncio
# from discord.ext import commands

# open json file
file = open('places.json', 'r')
data = json.loads(file.read())
file.close()

# global variables
client = discord.Client()
# client = commands.Bot(command_prefix="^", case_insensitive=True)

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

@client.event
async def on_ready():
    print("Bot logged in as {}".format(client.user))

@client.event
async def on_message(message):
    global channel, ai_place, ai_place_last, place, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, all_letter_string, all_letters

    if message.author == client.user:
        return
    if message.content.startswith('^play'):
        channel = message.channel
        await channel.send("Sure, lets play!!")

        async def send(msg):
            global channel
            await channel.send(msg)

        def check(m):
            return m.channel == channel and m.author != client.user

        async def takeInput():
            global invalid_count, place, channel
            try:
                msg = await client.wait_for('message', check=check, timeout=10)
                place = msg.content

            except asyncio.exceptions.TimeoutError:
                #send invalid count message and increase count
                if invalid_count < 1:
                    await send("You have to enter a place withing 10 seconds. If you don't, then your invalid count will increase by 1. If invalid count reaches 3, you lose.")
                invalid_count = invalid_count+1
                await send("Invalid count : {}".format(invalid_count))
                
                #check if invalid count == 3
                if invalid_count == 3:
                    # await send('You lost \U0001F602')
                    return
                
                #else, take input
                place=await takeInput()

            else:
                place = place.lower()
                #check if input is a whitespace or if it is nothing
                while place == '':
                    await send("Plese enter a place")
                    place = await takeInput()

                while place.isspace():
                    await send("Please enter a place.")
                    place = await takeInput()

                # check if user wants to quit
                if place == 'quit' or place == 'pass':
                    await send("You lost \U0001F602")
                    return
                    
                # check if place is from correct letter
                while place[0] != ai_place_last:
                    invalid_count += 1
                    await send(f'Your place should start from {ai_place_last.upper()}.')
                    await send(f'Invalid Place Count = {invalid_count}')
                    if invalid_count < 3:
                        await send(ai_place)
                    if invalid_count == 3:
                        await send("You lost \U0001F602")
                    place = await takeInput()

                #check if place is invalid
                while place[-1] not in all_letter_string:
                    await send('This is not a place. Enter another place.')
                    place = await takeInput()

                #check if place is already done
                while place in done_places:
                    await send('This place is done. Enter another place.')
                    place = await takeInput()

                # check if place exists in database
                while place not in globals()[place[0]]:
                    await send('This is not a place. Enter another place.')
                    place = await takeInput()

            return place

        #main code starts here
        # rules of the game
        await send("Let's play Atlas...")
        await send("I will start the game by entering a place.\n")
        await send("You have to enter a place in 10 seconds. If you fail to do so, your invalid count will increase. If your invalid count reaches 3, you lose.")
        await send("If you dont know place or you want to quit, just enter \"pass\" or \" quit\" into the chat")

        # first place
        first_letter = random.choice(all_letters)
        first_ai_place = random.choice(first_letter)
        ai_place_last = first_ai_place[-1].lower()
        await send('My Place : '+first_ai_place.title())
        await send('Enter a place from '+ai_place_last.upper()+'\n')
        first_letter.remove(first_ai_place)
        done_places.append(first_ai_place.lower())

        while True:
            global invalid_count
            invalid_count=0

            # take input from user
            ai_place = 'If you enter 3 invalid places you will lose'
            place = await takeInput()
            print(place)

            # invalid count checker
            if invalid_count == 3:
                await send('You lost \U0001F602')
                return

            if place[0] == ai_place_last:
                for For in all_letters:
                    if place in For:
                        For.remove(place)

            # if place entered is correct and all, then run this
            last = place[-1]
            done_places.append(place)
            place_given = False

            for cur_letter in all_letters:
                if last == ([i for i, var in globals().items() if var == cur_letter][0]) and cur_letter != []:
                    ai_place = random.choice(cur_letter)
                    cur_letter.remove(ai_place)
                    done_places.append(ai_place)
                    place_given = True
                    if ai_place == 'If you enter 3 invalid places you will lose':
                        pass

                    else:
                        await send('My Place : '+ai_place.title())
                        last_ai_place = ai_place
                        ai_place_last = last_ai_place[-1].lower()
                        await send('Enter a place from '+ai_place_last.upper()+'\n')
                        done_places.append(ai_place.lower())

            if place_given == False:
                await send("You Won")
                return
if __name__ == "__main__":

    client.run("OTI5NzI4MDg4NjUxMjI3MTQ2.YdriwQ.RZLoNH8T94bvBcoRHB5zP-PDT0w")
