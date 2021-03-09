import os # for importing env vars for the bot to use
from twitchio.ext import commands
'''
bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)
'''

botnick = "captainpovey"
channel = ""
bot = commands.Bot(
    irc_token="oauth:qwynekuzj717pqvs6oimwj9p3i1l8u",
    client_id="captainpovey",
    nick=botnick,
    prefix="!",
    initial_channels=channel
)
@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{botnick} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(channel, f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == botnick.lower():
        return

    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)

    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Hi, @{ctx.author.name}!")


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')


if __name__ == "__main__":
    bot.run()