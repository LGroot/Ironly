"""A bot to list all members of a server."""
import csv, os, tempfile, time
from dotenv import load_dotenv
 
from discord.ext import commands
from discord.ext.commands import Bot
from discord import File, Intents
 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
 
intents = Intents.default()
intents.members = True
bot = Bot(intents=intents)
 
 
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
 
 
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        print(error)
 
 
@bot.slash_command()
async def stat(ctx):
    """Returns a CSV file of all users on the server."""

    await ctx.respond("Check your DMs", ephemeral=True)
    before = time.time()
    nicknames = [m.display_name for m in ctx.guild.members]
    roles = [m.roles for m in ctx.guild.members]
    
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        for v,role in zip(nicknames, roles):
            writer.writerow([v, ",".join([r.name for r in role])])
        f.seek(0)

        after = time.time()

        dm = await bot.create_dm(ctx.author)
        await dm.send(file=File(f, filename='stats.csv'),
                      content="Here you go! Generated in {:.4}ms.".format((after - before)*1000))
 
 
if __name__ == '__main__':
    bot.run(TOKEN)
