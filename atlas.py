import asyncio
import random
import json

all_letter_string = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class WinException(Exception):
    pass

class PlayWithBot():

    # load json data into variables
    def __init__(self, channel, client) -> None:
        file = open('places.json', 'r')
        data = json.loads(file.read())
        file.close()
        self.a = data["a"]
        self.b = data["b"]
        self.c = data["c"]
        self.d = data["d"]
        self.e = data["e"]
        self.f = data["f"]
        self.g = data["g"]
        self.h = data["h"]
        self.i = data["i"]
        self.j = data["j"]
        self.k = data["k"]
        self.l = data["l"]
        self.m = data["m"]
        self.n = data["n"]
        self.o = data["o"]
        self.p = data["p"]
        self.q = data["q"]
        self.r = data["r"]
        self.s = data["s"]
        self.t = data["t"]
        self.u = data["u"]
        self.v = data["v"]
        self.w = data["w"]
        self.x = data["x"]
        self.y = data["y"]
        self.z = data["z"]
        self.channel = channel
        self.invalid_count = 0
        self.ai_place_last = None
        self.ai_place = None
        self.done_places = []
        self.invalid_msg = 'If you enter 3 invalid places you will lose'
        self.all_letters = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l, self.m, self.n, self.o, self.p, self.q, self.r, self.s, self.t, self.u, self.v, self.w, self.x, self.y, self.z]
        self.client = client

    async def send(self, msg):
        await self.channel.send(msg)

    def check(self, m):
        return m.channel == self.channel and m.author != self.client.user

    async def takeInput(self):
        try:
            msg = await self.client.wait_for('message', check=self.check, timeout=10)
            place = msg.content

        except asyncio.exceptions.TimeoutError:
            #send invalid count message and increase count
            if self.invalid_count < 1:
                await self.send("You have to enter a place withing 10 seconds. If you don't, then your invalid count will increase by 1. If invalid count reaches 3, you lose.")
            self.invalid_count = self.invalid_count+1
            await self.send("Invalid Count : {}".format(self.invalid_count))
            
            #check if invalid count == 3
            if self.invalid_count == 3:
                await self.send('You lost \U0001F602')
                raise WinException("Game Ended")
            
            #else, take input
            place=await self.takeInput()

        else:
            place = place.lower()
            #check if input is a whitespace or if it is nothing
            while place == '':
                await self.send("Plese enter a place")
                place = await self.takeInput()

            while place.isspace():
                await self.send("Please enter a place.")
                place = await self.takeInput()

            # check if user wants to quit
            if place == 'quit' or place == 'pass':
                await self.send("You lost \U0001F602")
                raise WinException("Game Ended")
                    
            # check if place is from correct letter
            while place[0] != self.ai_place_last:
                self.invalid_count += 1
                await self.send(f'Your place should start from {self.ai_place_last.upper()}.')
                await self.send(f'Invalid Count = {self.invalid_count}')
                if self.invalid_count < 3:
                    await self.send(self.invalid_msg)
                if self.invalid_count == 3:
                    await self.send("You lost \U0001F602")
                    raise WinException("Game Ended")
                place = await self.takeInput()

            #check if place is invalid
            while place[-1] not in all_letter_string:
                await self.send('This is not a place. Enter another place.')
                place = await self.takeInput()

            #check if place is already done
            while place in self.done_places:
                await self.send('This place is done. Enter another place.')
                place = await self.takeInput()

            while place not in self.__dict__[place[0]]:
                await self.send('This is not a place. Enter another place.')
                place = await self.takeInput()

        return place

    async def main(self):
        # await self.send("Let's play Atlas...")
        await self.send("Sure, lets play!!")
        await self.send("I will start the game by entering a place.\n")
        await self.send("You have to enter a place in 10 seconds. If you fail to do so, your invalid count will increase. If your invalid count reaches 3, you lose.")
        await self.send("If you dont know place or you want to quit, just enter \"pass\" or \" quit\" into the chat")

        # first place
        first_letter = random.choice(self.all_letters)
        first_ai_place = random.choice(first_letter)
        self.ai_place_last = first_ai_place[-1].lower()
        await self.send('My Place : '+first_ai_place.title())
        await self.send('Enter a place from '+self.ai_place_last.upper()+'\n')
        first_letter.remove(first_ai_place)
        self.done_places.append(first_ai_place.lower())

        while True:
            # self.invalid_count=0

            # take input from user
            ai_place = ''
            place = await self.takeInput()
            print(place)

            # invalid count checker
            if self.invalid_count == 3:
                await self.send('You lost \U0001F602')
                raise WinException("Game Ended")

            if place[0] == self.ai_place_last:
                for For in self.all_letters:
                    if place in For:
                        For.remove(place)

            # if place entered is correct and all, then run this
            last = place[-1]
            self.done_places.append(place)
            place_given = False

            for cur_letter in all_letter_string:
                if last == cur_letter:
                    ai_place = random.choice(self.__dict__[cur_letter])
                    self.__dict__[cur_letter].remove(ai_place)
                    # self.done_places.append(ai_place)
                    place_given = True
                    if ai_place == '':
                        pass

                    else:
                        await self.send('My Place : '+ai_place.title())
                        last_ai_place = ai_place
                        self.ai_place_last = last_ai_place[-1].lower()
                        await self.send('Enter a place from '+self.ai_place_last.upper()+'\n')
                        self.done_places.append(ai_place.lower())

            if place_given == False:
                await self.send("You Won")
                raise WinException("Game Ended")