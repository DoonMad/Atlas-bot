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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='^help'))


@client.event
async def on_message(message):
    global games_active
    channel = message.channel

    if message.author == client.user:
        return

    # command 1
    if message.content.startswith('^help'):
        embed = discord.Embed(
            description="Hello there! Here all all the commnads you can use. New commands will be added soon!", color=0x1e1e1e)
        embed.set_author(name="Atlas-bot Help Command",
                         icon_url=client.user.avatar_url)
        # embed = discord.Embed(title="Hello there! Here all all the commnads you can use.", description="", color=0x1e1e1e)
        embed.add_field(name="`^playwithbot`, `^pwb`",
                        value="To play atlas with me type this into the chat.", inline=True)
        embed.add_field(
            name="`^play`", value="To play atlas with your friends type this into the chat.", inline=True)
        await channel.send(embed=embed)

    # command 2
    if message.content.startswith('^playwithbot') or message.content.startswith('^pwb'):
        player = message.author

        game_id = random.randint(0, 9999999)
        while game_id in games_active:
            game_id = random.randint(0, 9999999)
        locals()['p'+str(game_id)] = atlas.PlayWithBot(channel, client, player)
        games_active.append(game_id)

        # run the function
        try:
            print("game started")
            await locals()['p'+str(game_id)].main()
        except atlas.WinException as exception:
            print(str(exception)+'\n')
            # print(locals()['p'+str(game_id)].done_places)
            pass

        # destroy the instance
        del locals()['p'+str(game_id)]
        games_active.remove(game_id)

    # command 3
    if message.content.startswith('^play'):
        players = []
        embed = discord.Embed(
            title="React to play!", description="React to this message with ✅ to play.", color=0x00d26a)
        react_msg = await channel.send(embed=embed)
        await react_msg.add_reaction('✅')
        await asyncio.sleep(10)
        cache_msg = await react_msg.channel.fetch_message(react_msg.id)
        reactions = cache_msg.reactions
        for reaction in reactions:
            if str(reaction) == '✅' and reaction.message.id == react_msg.id:
                players = [user async for user in reaction.users() if user != client.user]
                for i in range(len(players)):
                    players[i] = players[i].mention
        if len(players) == 1:
            await channel.send('Aww, no one is there to play with '+players[0]+', but don\'t you worry, you can still play with me. To play with me enter ^playwithbot or ^pwb into the chat. 🙃')
        elif len(players) < 1:
            await channel.send("Bruh, react if you want to play. Don\'t waste my time 😠")
        else:
            game_id = random.randint(0, 9999999)
            while game_id in games_active:
                game_id = random.randint(0, 9999999)
            locals()['p'+str(game_id)] = atlas.Play(channel, client, players)
            games_active.append(game_id)

            try:
                print("game started")
                await locals()['p'+str(game_id)].main()
            except atlas.WinException as exception:
                print(str(exception)+"\n")
                # print(locals()['p'+str(game_id)].done_places)
                pass
            # destroy the instance
            del locals()['p'+str(game_id)]
            games_active.remove(game_id)

    # command 4
    if message.content.startswith('^servers'):
        await channel.send("I am in "+str(len(client.guilds))+" servers ❤️")

    # command 5
    if message.content.startswith('^allservers'):
        for server in client.guilds:
            await channel.send(server.name+" ❤️")

if __name__ == "__main__":
    client.run("OTI5NzI4MDg4NjUxMjI3MTQ2.YdriwQ.RZLoNH8T94bvBcoRHB5zP-PDT0w")
