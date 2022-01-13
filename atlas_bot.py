# imports
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

    if message.author == client.user:
        return
    if message.content.startswith('^play'):
        channel = message.channel
        game_id = random.randint(0, 9999999)
        while game_id in games_active:
            game_id = random.randint(0, 9999999)

        locals()['p'+str(game_id)]=atlas.PlayWithBot(channel, client)
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


if __name__ == "__main__":
    client.run("OTI5NzI4MDg4NjUxMjI3MTQ2.YdriwQ.RZLoNH8T94bvBcoRHB5zP-PDT0w")
