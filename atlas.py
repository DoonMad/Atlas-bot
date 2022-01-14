import asyncio
import random
import json
import discord

# all_letter_string = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# a =
# b =
# c =
# d =
# e =
# f =
# g =
# h =
# i =
# j =
# k =
# l =
# m =
# n =
# o =
# p =
# q =
# r =
# s =
# t =
# u =
# v =
# w =
# x =
# y =
# z =


class WinException(Exception):
    pass


class PlayWithBot():

    # load json data into variables
    def __init__(self, channel, client, player) -> None:
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
        self.bot_place_last = None
        # self.bot_place = None
        self.done_places = []
        self.all_letters = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l,
                            self.m, self.n, self.o, self.p, self.q, self.r, self.s, self.t, self.u, self.v, self.w, self.x, self.y, self.z]
        self.client = client
        self.player = player

    async def send(self, msg):
        await self.channel.send(msg)

    async def embed(self, title, description=False, thumbnail=False, author=False, author_icon=False, fieldT=False, fieldD=False, inline=False):
        embed = discord.Embed(title=title+'\n\n', color=0xFF5733)
        if description:
            embed.description = '\n'+description
        if fieldT:
            embed.add_field(name='\n'+fieldT, value=fieldD, inline=inline)
        if author:
            embed.set_author(name=author, icon_url=author_icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        await self.channel.send(embed=embed)

    def check(self, m):
        # return m.channel == self.channel and m.author != self.client.user
        # print(m)
        return m.channel == self.channel and m.author == self.player

    async def takeInput(self):
        try:
            msg = await self.client.wait_for('message', check=self.check, timeout=10)
            place = msg.content

        except asyncio.exceptions.TimeoutError:
            # send invalid count message and increase count
            self.invalid_count = self.invalid_count+1
            if self.invalid_count == 1:
                await self.embed(title='❌', description="You didn't enter a place within 10 seconds. ⌛")
            if self.invalid_count == 2:
                await self.embed(title='❌\t❌', description="You didn't enter a place within 10 seconds. ⌛")
            if self.invalid_count == 3:
                await self.embed(title='❌\t❌\t❌', description="You lost 😂")
                raise WinException("Game Ended")
            # else, take input
            place = await self.takeInput()

        else:
            place = place.lower()
            # check if user wants to quit
            if place == 'quit' or place == 'pass':
                await msg.add_reaction('👍')
                if self.__dict__[self.bot_place_last] != []:
                    bot_place = random.choice(
                        self.__dict__[self.bot_place_last])
                    self.done_places.append(bot_place.lower())
                    await self.embed(title='You lost 😂', description='You could have said **'+bot_place.title()+'**')
                    raise WinException("Game Ended")
                else:
                    await self.embed(title="Draw Match", description="You know what. even I do not know a place from "+self.bot_place_last+", why not call it a draw?")
                    raise WinException("Game Ended")

            # check if place is from correct letter
            while place[0] != self.bot_place_last:
                await msg.add_reaction('❌')
                self.invalid_count += 1
                if self.invalid_count == 1:
                    await self.embed(title='❌', description=f'Your place should start from {self.bot_place_last.upper()}. 😑')
                if self.invalid_count == 2:
                    await self.embed(title='❌\t❌', description=f'Your place should start from {self.bot_place_last.upper()}. 😑')
                if self.invalid_count == 3:
                    await self.embed(title='❌\t❌\t❌', description="You lost 😂")
                    raise WinException("Game Ended")
                place = await self.takeInput()

            # check if place is already done
            while place in self.done_places:
                await msg.add_reaction('🚫')
                await self.send('This place is done. Enter another place. 😶')
                place = await self.takeInput()

            while place not in self.__dict__[place[0]]:
                await msg.add_reaction('🚫')
                await self.send('This is not a place. Enter another place. 😑')
                place = await self.takeInput()

            if msg.content.lower() == place:
                await msg.add_reaction('✅')
        return place

    async def givePlace(self, last):
        if self.__dict__[last] != []:
            bot_place = random.choice(self.__dict__[last])
            self.__dict__[last].remove(bot_place)
            self.bot_place_last = bot_place[-1].lower()
            await self.embed(title=bot_place.title(), description='Enter a place from '+self.bot_place_last.upper())
            self.done_places.append(bot_place.lower())
        else:
            await self.send("You Won 🏆")
            raise WinException("Game Ended")

    async def main(self):
        await self.embed("Let's play Atlas!!", description="||\n||**Rules**\n You have to enter a place within 10 seconds. If you fail to do so, you get 1 cross (❌). If you enter a place starting with a wrong letter, it will also give you a cross (❌). If you get 3 crosses (❌\t❌\t❌), you lose.\n\n" +
                         "If you dont know a place or you want to quit, just enter \"pass\" or \" quit\" into the chat\n\n\n" +
                         "Now, I will start the game by entering a place.", author=self.client.user.name, author_icon=self.client.user.avatar_url)

        # first place
        first_letter = random.choice(self.all_letters)
        first_bot_place = random.choice(first_letter)
        self.bot_place_last = first_bot_place[-1].lower()
        await self.embed(title=first_bot_place.title(), description='Enter a place from '+self.bot_place_last.upper())
        first_letter.remove(first_bot_place)
        self.done_places.append(first_bot_place.lower())

        while True:
            # take input from user
            place = await self.takeInput()
            print(place)

            if place[0] == self.bot_place_last:
                for For in self.all_letters:
                    if place in For:
                        For.remove(place)

            # if place entered is correct and all, then run this
            last = place[-1]
            self.done_places.append(place)
            await self.givePlace(last=last)


class Play():

    # load json data into variables
    def __init__(self, channel, client, players) -> None:
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
        self.last_letter = None
        # self.bot_place = None
        self.done_places = []
        self.all_letters = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l, self.m, self.n, self.o, self.p, self.q, self.r, self.s, self.t, self.u, self.v, self.w, self.x, self.y, self.z]
        self.client = client
        self.players = dict()
        for i in range(0, len(players)):
            player = dict()
            player["user"] = players[i]
            player["invalid"] = 0
            self.players[i] = player
        self.player = None

    async def send(self, msg):
        await self.channel.send(msg)

    async def embed(self, title, description=False, thumbnail=False, author=False, author_icon=False, fieldT=False, fieldD=False, inline=False):
        embed = discord.Embed(title=title+'\n\n', color=0xFF5733)
        if description:
            embed.description = '\n'+description
        if fieldT:
            embed.add_field(name='\n'+fieldT, value=fieldD, inline=inline)
        if author:
            embed.set_author(name=author, icon_url=author_icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        await self.channel.send(embed=embed)

    def check(self, m):
        # return m.channel == self.channel and m.author != self.client.user
        # print(m)
        print(m.author.id)
        print(self.player['user'].id)
        return m.channel == self.channel and m.author.id == self.player['user'].id

    async def takeInput(self):
        # invalid = self.player["invalid"]
        # print(self.player)
        try:
            msg = await self.client.wait_for('message', check=self.check, timeout=10)
            place = msg.content

        except asyncio.exceptions.TimeoutError:
            # send invalid count message and increase count
            
            self.player["invalid"] = self.player["invalid"]+1
            if self.player["invalid"] == 1:
                await self.embed(title='❌', description="You didn't enter a place within 10 seconds. ⌛")
            if self.player["invalid"] == 2:
                await self.embed(title='❌\t❌', description="You didn't enter a place within 10 seconds. ⌛")
            if self.player["invalid"] == 3:
                await self.embed(title='❌\t❌\t❌', description="You lost 😂")
                del self.player
                return
                # raise WinException("Game Ended")
            # else, take input
            place = await self.takeInput()

        else:
            place = place.lower()
            # check if user wants to quit
            if place == 'quit' or place == 'pass':
                if self.__dict__[self.last_letter] != []:
                    bot_place = random.choice(
                        self.__dict__[self.last_letter])
                    self.done_places.append(bot_place.lower())
                    await self.embed(title='You lost 😂', description='You could have said **'+bot_place.title()+'**')
                    del self.player
                    return
                    # raise WinException("Game Ended")
                # else:
                #     await self.embed(title="Draw Match", description="You know what. even I do not know a place from "+self.last_letter+", why not call it a draw?")
                #     raise WinException("Game Ended")

            # check if place is from correct letter
            if self.last_letter:
                while place[0] != self.last_letter:
                    await msg.add_reaction('❌')
                    self.player["invalid"] += 1
                    if self.player["invalid"] == 1:
                        await self.embed(title='❌', description=f'Your place should start from {self.last_letter.upper()}. 😑')
                    if self.player["invalid"] == 2:
                        await self.embed(title='❌\t❌', description=f'Your place should start from {self.last_letter.upper()}. 😑')
                    if self.player["invalid"] == 3:
                        await self.embed(title='❌\t❌\t❌', description="You lost 😂")
                        del self.player
                        # raise WinException("Game Ended")
                        return
                    place = await self.takeInput()

            # check if place is already done
            while place in self.done_places:
                await msg.add_reaction('🚫')
                await self.send('This place is done. Enter another place. 😶')
                place = await self.takeInput()

            while place not in self.__dict__[place[0]]:
                await msg.add_reaction('🚫')
                await self.send('This is not a place. Enter another place. 😑')
                place = await self.takeInput()

            if msg.content.lower() == place:
                await msg.add_reaction('✅')
        return place

    async def givePlace(self, last):
        if self.__dict__[last] != []:
            bot_place = random.choice(self.__dict__[last])
            self.__dict__[last].remove(bot_place)
            self.last_letter = bot_place[-1].lower()
            await self.embed(title=bot_place.title(), description='Enter a place from '+self.last_letter.upper())
            self.done_places.append(bot_place.lower())
        else:
            await self.send("You Won 🏆")
            raise WinException("Game Ended")

    async def main(self):
        await self.embed("Let's play Atlas!!", description="||\n||**Rules**\n You have to enter a place within 10 seconds. If you fail to do so, your invalid count will increase. If you enter a place starting with a wrong letter, it will also increase your invalid count. If your invalid count reaches 3, you lose.\n\n" +
                         "If you dont know a place or you want to quit, just enter \"pass\" or \" quit\" into the chat\n\n" +
                         "Now, I will start the game by entering a place.", author=self.client.user.name, author_icon=self.client.user.avatar_url)

        # first place
        # first_letter = random.choice(self.all_letters)
        # first_bot_place = random.choice(first_letter)
        # self.bot_place_last = first_bot_place[-1].lower()
        # await self.embed(title=first_bot_place.title(), description='Enter a place from '+self.bot_place_last.upper())
        # first_letter.remove(first_bot_place)
        # self.done_places.append(first_bot_place.lower())

        while True:
            for player in self.players:
                self.player = self.players[player]
                if self.last_letter:
                    await self.send("Enter a place from "+self.last_letter)
                place = await self.takeInput()
                print(place)
                self.last_letter = place[-1]
                if len(self.players) == 0:
                    raise WinException("game ended")

                if self.last_letter:
                    if place[0] == self.last_letter:
                        for For in self.all_letters:
                            if place in For:
                                For.remove(place)

                # if place entered is correct and all, then run this
                # self.last_letter = place[-1]
                self.done_places.append(place)
                # await self.givePlace(last=last)


