# imports
import asyncio
import discord
import atlas
import random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv('TOKEN')

# bot = commands.Bot(command_prefix='^', intents=intents)

# @bot.hybrid_command()
# async def test(ctx):
#     await ctx.send("This is a hybrid command!")

# bot.add_command(test)


# global variables
game_instances = {}
client = discord.Client(intents=intents)
games_active = []
tree = discord.app_commands.CommandTree(client)

@tree.command(description="Atlas bot help menu.")
async def atlashelp(interaction=discord.Interaction):
    
    await interaction.response.send_message(embed=helpEmbed)


@client.event
async def on_ready():
    await tree.sync()
    print("Bot logged in as {}".format(client.user))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='^help'))
    global helpEmbed
    helpEmbed = discord.Embed(
            description="Hello there! Here all all the commnads you can use.||\n\n||**Rules**\n"+
            "You have to enter a place from the last letter of the last entered place within 10 seconds. If you fail to do so, you get a cross (❌). If you get 3 crosses (❌\t❌\t❌), you lose. " +
        "If you dont know a place enter `pass` or if you want to quit, enter `quit` into the chat.||\n\n||", color=0x1e1e1e)
    helpEmbed.set_author(name="Atlas-bot Help Command",
                         icon_url=client.user.avatar)
    helpEmbed.add_field(name="`^pwb`",
                        value="To play atlas with me type this into the chat.", inline=True)
    helpEmbed.add_field(
            name="`^play`", value="To play atlas with your friends type this into the chat.", inline=True)


@client.event
async def on_message(message):
    global games_active
    channel = message.channel

    if message.author == client.user:
        return

    # command 1
    if message.content.startswith('^help'):
        await channel.send(embed=helpEmbed)

    # command 2
    if message.content.startswith('^pwb'):
        player = message.author

        game_id = random.randint(0, 9999999)
        while game_id in games_active:
            game_id = random.randint(0, 9999999)
        # locals()['p'+str(game_id)] = atlas.PlayWithBot(channel, client, player)
        game_instances['p'+str(game_id)] = atlas.PlayWithBot(channel, client, player)
        games_active.append(game_id)

        # Debug prints
        # print(f"game_id: {game_id}")
        # print('p'+str(game_id))
        # print(game_instances.keys())
        # print(game_instances["player"])
        # print(f"game_instances['p'+str(game_id)]: {game_instances['p'+str(game_id)]}")


        # run the function
        try:
            print("game started")
            await game_instances['p'+str(game_id)].main()
        except atlas.WinException as exception:
            print(str(exception)+'\n')
            # print(game_instances['p'+str(game_id)].done_places)
            pass

        # destroy the instance
        del game_instances['p'+str(game_id)]
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
            game_instances['p'+str(game_id)] = atlas.Play(channel, client, players)
            games_active.append(game_id)

            try:
                print("game started")
                await game_instances['p'+str(game_id)].main()
            except atlas.WinException as exception:
                print(str(exception)+"\n")
                # print(locals()['p'+str(game_id)].done_places)
                pass
            # destroy the instance
            del game_instances['p'+str(game_id)]
            games_active.remove(game_id)

    # command 4
    if message.content.startswith('^servers'):
        await channel.send("I am in "+str(len(client.guilds))+" servers ❤️")

    # command 5
    if message.content.startswith('^allservers'):
        for server in client.guilds:
            await channel.send(server.name+" ❤️")

if __name__ == "__main__":
    client.run(TOKEN)
