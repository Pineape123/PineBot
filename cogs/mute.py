import asyncio
from discord.ext import commands
import discord

class mute(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command
	async def mute(self, ctx, user : discord.Member, duration = 0,*, unit = None):
		roleobject = discord.utils.get(ctx.message.guild.roles, id="Muted")
		await ctx.send(f":white_check_mark: Muted {user} for {duration}{unit}")
		await user.add_roles(roleobject)
		if unit == "s":
			wait = 1 * duration
			await asyncio.sleep(wait)
		elif unit == "m":
			wait = 60 * duration
			await asyncio.sleep(wait)
		await user.remove_roles(roleobject)
		await ctx.send(f":white_check_mark: {user} was unmuted")

def setup(bot):
	bot.add_cog(mute(bot))