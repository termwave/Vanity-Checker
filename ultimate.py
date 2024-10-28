import discord
from discord.ext import commands
import time
import os
import datetime
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
token = ""
@bot.command()
async def snipe(ctx):
    await ctx.send("Please enter the vanity URL you want to snipe:")
    def check_msg(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    vanity_msg = await bot.wait_for("message", check=check_msg)
    vanity_code = vanity_msg.content.strip()
    
    try:
        await ctx.send(f"Vanity URL: `{vanity_code}`, How many seconds should the bot wait between checks?")
        delay_msg = await bot.wait_for("message", check=check_msg)
        delay = int(delay_msg.content.strip())
        while True:
            response = requests.get(f"https://discord.com/api/v10/invites/{vanity_code}")
            if response.status_code == 404:
                    await ctx.send(f"Vanity URL is Available {vanity_code}!")
                    break
            else:
                await ctx.send(f"Vanity `{vanity_code}` is still in use.")
            
            time.sleep(delay)
            current_time = datetime.datetime.now().strftime("%X")

    except ValueError:
        await ctx.send("Invalid input delay as a number.")
    except KeyboardInterrupt:
        await ctx.send("Sniping process stopped.")

bot.run(token)
