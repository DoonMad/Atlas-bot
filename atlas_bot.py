# imports
import asyncio
import discord
import atlas
import random

# global variables
client = discord.Client()
games_active = []


@client.event
async def on_ready():
    print("Bot logged in as {}".format(client.user))


@client.event
async def on_message(message):
    global games_active
    channel = message.channel

    if message.author == client.user:
        return

    # command 1
    if message.content.startswith('^playwithbot') or message.content.startswith('^pwb'):
        # react_msg = await channel.send("React with ✅ to play")
        # await react_msg.add_reaction('✅')

        # def check(reaction, user):
        #     global player
        #     if reaction.message == react_msg and str(reaction.emoji) == '✅' and not user.bot:
        #         player = user
        #         return True
        #     return False

        # try:
        #     await client.wait_for('reaction_add', timeout=10, check=check)
        # except asyncio.TimeoutError:
        #     await channel.send('Bruh, react to the message if you want to play 🤨')
        # else:
        player = message.author

        game_id = random.randint(0, 9999999)
        while game_id in games_active:
            game_id = random.randint(0, 9999999)
        locals()['p'+str(game_id)] = atlas.PlayWithBot(channel, client, player)
        games_active.append(game_id)
        
        # run the function
        try:
            print("game started \n")
            await locals()['p'+str(game_id)].main()
        except atlas.WinException as exception:
            print(exception)
            print(locals()['p'+str(game_id)].done_places)

        # destroy the instance
        del locals()['p'+str(game_id)]
        games_active.remove(game_id)


    # command 2
    if message.content.startswith('^servers'):
        await channel.send("I am in "+str(len(client.guilds))+" servers ❤️")


    #command 3
    if message.content.startswith('^play'):
        players = []
        react_msg = await channel.send("React with ✅ to play")
        await react_msg.add_reaction('✅')

        def check(reaction, user):
            # global player
            if reaction.message == react_msg and str(reaction.emoji) == '✅' and not user.bot:
                players.append(user)
                return True
            return False

        try:
            await client.wait_for('reaction_add', timeout=10, check=check)
        except asyncio.TimeoutError:
            await channel.send('Bruh, react to the message if you want to play 🤨')

        game_id = random.randint(0, 9999999)
        while game_id in games_active:
            game_id = random.randint(0, 9999999)
        locals()['p'+str(game_id)] = atlas.Play(channel, client, players)
        games_active.append(game_id)

        try:
            print("game started \n")
            await locals()['p'+str(game_id)].main()
        except atlas.WinException as exception:
            print(exception)
            print(locals()['p'+str(game_id)].done_places)

        # destroy the instance
        del locals()['p'+str(game_id)]
        games_active.remove(game_id)


if __name__ == "__main__":
    client.run("OTI5NzI4MDg4NjUxMjI3MTQ2.YdriwQ.RZLoNH8T94bvBcoRHB5zP-PDT0w")
