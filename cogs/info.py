import discord
from discord.ext import commands
import os
import psutil
import math
from datetime import datetime, time as datetime_time, timedelta
class info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


		
	@commands.command(aliases=['ping', 'pong', 'i', 'p'] )
	async def info(self, ctx):
		pid = os.getpid()
	
		python_process = psutil.Process(pid)

		embed=discord.Embed(title="__**Info**__", color=0x06c258)
		embed.add_field(name="Current Guilds:", value=f"Currently in {len(self.bot.guilds)} servers!", inline=False)
		embed.add_field(name="Latency:", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
		embed.add_field(name="CPU Usage:", value=f"{psutil.cpu_percent()}%", inline=False)
		embed.add_field(name="Memory Usage:", value=f"{str(round(psutil.virtual_memory().available*  0.000000001, 2))} / {str(round(psutil.virtual_memory().total *0.000000001, 2))} GB", inline=False)
		embed.add_field(name="Shards Online:", value=f"1/1", inline=False)


		embed.set_footer(text="PineBot")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(info(bot))