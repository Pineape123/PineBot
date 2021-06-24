import discord
from discord.ext import commands
import math

class info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	
	@commands.command()
	async def info(self, ctx):
		await ctx.send(f"Currently in {len(self.bot.guilds)}")
		


def setup(bot):
	bot.add_cog(info(bot))
