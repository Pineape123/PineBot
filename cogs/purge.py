import discord
from discord import channel
from discord.ext import commands

class purge(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, clean: int):
		await ctx.channel.purge(limit=clean+1)
		embed=discord.Embed(title="Successfully Purged!", description=f'{ctx.author.mention} Cleared {clean} messages!', color=0x80ff00)
		await ctx.send(embed=embed, delete_after=5.0)
	@purge.error
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			embed=discord.Embed(title="Error Purging!", description=f'You do not have required permissions to run this!', color=0xff0006)
			await ctx.send(embed=embed, delete_after=5.0)



def setup(bot):
	bot.add_cog(purge(bot))