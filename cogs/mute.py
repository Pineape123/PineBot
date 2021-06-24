import discord
from discord.ext import commands

class mute(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	
	@commands.command()
	async def mute(self, ctx, user:discord.Member, *, reason=None, duration=None):
		role = discord.utils.get(ctx.guild.roles, name="Muted")

		await user.add_roles(role)

def setup(bot):
	bot.add_cog(mute(bot))
