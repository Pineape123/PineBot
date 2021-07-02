import discord
from discord.ext import commands

class bane(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def bane(self, ctx, user=None):
		if not user:
			user = ctx.author.mention
		embed=discord.Embed(description=f"{user} was bannned!")
		await ctx.send(embed=embed)
#Custom bane command, mentions whoever was mentioned in the bane msg and outputs: "was bannned."

def setup(bot):
	bot.add_cog(bane(bot))
#Adds this as a cog to the bot.
