import asyncio
import random
import json
import string
import discord


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
        self.last_letter = None
        # self.bot_place = None
        self.done_places = []
        self.all_letters = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l,
                            self.m, self.n, self.o, self.p, self.q, self.r, self.s, self.t, self.u, self.v, self.w, self.x, self.y, self.z]
        self.client = client
        self.player = player

    async def send(self, msg):
        await self.channel.send(msg)

    async def embed(self, title, description=False, thumbnail=False, author=False, author_icon=False, fieldT=False, fieldD=False, inline=False, msg=False):
        embed = discord.Embed(title=title, color=0xFF5733)
        if description:
            embed.description = description
        if fieldT:
            embed.add_field(name=fieldT, value=fieldD, inline=inline)
        if author:
            embed.set_author(name=author, icon_url=author_icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if msg:
            await msg.reply(embed=embed)
        else:
            await self.channel.send(embed=embed)

    def check(self, msg):
        if msg.channel == self.channel and msg.author == self.player:
            place = msg.content
            place = place.lower()

            if place == 'quit':  
                asyncio.create_task(msg.add_reaction('👍'))
                if self.__dict__[self.last_letter] != []:
                    bot_place = random.choice(
                        self.__dict__[self.last_letter])
                    self.done_places.append(bot_place.lower())
                    asyncio.create_task(self.embed(title='You lost 😂', description='You could have said **'+bot_place.title()+'**'))
                    raise WinException("Game Ended")
                else:
                    asyncio.create_task(self.embed(title="Draw Match", description="You know what, even I do not know a place from "+self.last_letter+", why not call it a draw?"))
                    raise WinException("Game Ended")

            # check if place is from correct letter
            if self.last_letter:
                if place[0] != self.last_letter:
                    asyncio.create_task(msg.add_reaction('❌'))
                    asyncio.create_task(msg.reply(self.player.mention+f' Your place did not start from **{self.last_letter.upper()}** 😑'))
                    return

            # check if place is already done
            if place in self.done_places:
                asyncio.create_task(msg.add_reaction('❌'))
                asyncio.create_task(msg.reply(self.player.mention+" This place has already been entered 😶"))
                return

            if place not in self.__dict__[place[0]]:
                asyncio.create_task(msg.add_reaction('❌'))
                asyncio.create_task(msg.reply(self.player.mention+" This is not a place 😑"))
                return

            if msg.content.lower() == place:
                asyncio.create_task(msg.add_reaction('✅'))
                return True
        # return msg.channel == self.channel and msg.author == self.player

    async def addInvalid(self, desc, msg=False):
        self.invalid_count = self.invalid_count+1
        if self.invalid_count == 1:
            await self.embed(title='❌', description=desc, msg=msg)
        if self.invalid_count == 2:
            await self.embed(title='❌\t❌', description=desc, msg=msg)
        if self.invalid_count == 3:
            await self.embed(title='❌\t❌\t❌', description=desc+"\nYou lost 😂", msg=msg)
            raise WinException("Game Ended")

    async def takeInput(self):
        try:
            msg = await self.client.wait_for('message', check=self.check, timeout=10)
            place = msg.content

        except asyncio.exceptions.TimeoutError:
            await self.addInvalid("You didn't enter a place within 10 seconds. ⌛")
            place = await self.takeInput()
            
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
        await self.embed("Let's play Atlas!!", description="||\n||**Rules**\n You have to enter a place within 10 seconds. If you fail to do so, you get 1 cross (❌). If you get 3 crosses (❌\t❌\t❌), you lose.\n\n" +
        "If you dont know a place and you want to quit, enter\" quit\" into the chat\n\n\n" +
        "Now, I will start the game by entering a place.", author=self.client.user.name, author_icon=self.client.user.avatar_url)

        # first place
        first_letter = random.choice(self.all_letters)
        first_bot_place = random.choice(first_letter)
        self.last_letter = first_bot_place[-1].lower()
        await self.embed(title=first_bot_place.title(), description='Enter a place from '+self.last_letter.upper())
        first_letter.remove(first_bot_place)
        self.done_places.append(first_bot_place.lower())

        while True:
            # take input from user
            place = await self.takeInput()
            # print(place)
            if place[0] == self.last_letter:
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
        self.all_letters = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j, self.k, self.l,
                            self.m, self.n, self.o, self.p, self.q, self.r, self.s, self.t, self.u, self.v, self.w, self.x, self.y, self.z]
        self.client = client
        self.players = []
        for i in players:
            # print(i)
            player = dict()
            player["user"] = i
            player["invalid"] = 0
            self.players.append(player)
        self.player = None

    async def send(self, msg):
        await self.channel.send(msg)

    async def embed(self, title, description=False, thumbnail=False, author=False, author_icon=False, fieldT=False, fieldD=False, inline=False, msg=False):
        embed = discord.Embed(title=title, color=0xFF4040)
        if description:
            embed.description = description
        if fieldT:
            embed.add_field(name=fieldT, value=fieldD, inline=inline)
        if author:
            embed.set_author(name=author, icon_url=author_icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if msg:
            await msg.reply(embed=embed)
        else:
            await self.channel.send(embed=embed)

    async def addInvalid(self, desc, msg=False):
        self.player["invalid"] = self.player["invalid"]+1
        if self.player['invalid'] == 1:
            await self.embed(title='❌', description=desc, msg=msg)
        if self.player['invalid'] == 2:
            await self.embed(title='❌\t❌', description=desc, msg=msg)
        if self.player['invalid'] == 3:
            await self.embed(title='❌\t❌\t❌', description=desc+"\nYou lost 😂", msg=msg)
            del self.player

    def check(self, msg):
        if msg.channel == self.channel and msg.author.mention == self.player['user']:
            place = msg.content
            place = place.lower()

            # check if user wants to quit
            if place == 'quit':
                asyncio.create_task(msg.add_reaction('👍'))
                del self.player
                return True

            if place == 'pass':
                asyncio.create_task(msg.add_reaction('👍'))
                asyncio.create_task(self.addInvalid(self.player["user"]+f' You could not enter a place 😆', msg=msg))
                return True

            # check if place is from correct letter
            if self.last_letter:
                if place[0] != self.last_letter:
                    asyncio.create_task(msg.add_reaction('❌'))
                    asyncio.create_task(msg.reply(self.player["user"]+f' Your place did not start from **{self.last_letter.upper()}** 😑'))
                    return

            # check if place is already done
            if place in self.done_places:
                asyncio.create_task(msg.add_reaction('❌'))
                asyncio.create_task(msg.reply(self.player["user"]+" This place has already been entered 😶"))
                return

            if place not in self.__dict__[place[0]]:
                asyncio.create_task(msg.add_reaction('❌'))
                asyncio.create_task(msg.reply(self.player["user"]+" This is not a place 😑"))
                return

            if msg.content.lower() == place:
                asyncio.create_task(msg.add_reaction('✅'))
                return True

    async def takeInput(self):
        try:
            msg = await self.client.wait_for('message', check=self.check, timeout=10)
            place = msg.content

        except asyncio.exceptions.TimeoutError:
            await self.addInvalid(self.player["user"]+" You didn't enter a place within 10 seconds ⌛")
            return

        return place

    async def main(self):
        await self.embed("Let's play Atlas!!", description="||\n||**Rules**\n You have to enter a place within 10 seconds. If you fail to do so, you get a cross (❌). If you get 3 crosses (❌\t❌\t❌), you lose.\n\n" +
        "If you dont know a place enter \"pass\" or if you want to quit, enter \"quit\" into the chat", author=self.client.user.name, author_icon=self.client.user.avatar_url)

        self.last_letter = random.choice(string.ascii_lowercase)
        while True:
            # print("in while")
            if len(self.players) < 2:
                await self.send("🏆 "+self.players[0]["user"]+" **won the game 🏆**")
                raise WinException("game ended")

            for player in range(len(self.players)):
                if len(self.players) < 2:
                    await self.send("🏆 "+self.players[0]["user"]+" **won the game 🏆**")
                    raise WinException("game ended")
                self.player = self.players[player]
                await self.send(self.player["user"]+" Enter a place from **"+self.last_letter.upper()+"**")
                place = await self.takeInput()
                
                if "player" not in self.__dict__:
                    await self.send(self.players[player]["user"]+" **eliminated 😂**")
                    del self.players[player]
                    continue
                if place == None:
                    continue
                if place == "pass":
                    if self.player['invalid'] == 3:
                        del self.player
                    if "player" not in self.__dict__:
                        del self.players[player]
                    continue
                self.last_letter = place[-1]

                if self.last_letter:
                    if place[0] == self.last_letter:
                        for For in self.all_letters:
                            if place in For:
                                For.remove(place)
                self.done_places.append(place)
