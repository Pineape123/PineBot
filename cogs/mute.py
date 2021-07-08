import discord
import asyncio
import re
from discord.ext import commands
import sys
import traceback


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
	async def convert(self, ctx, argument):
		args = argument.lower()
		matches = re.findall(time_regex, args)
		time = 0
		for v, k in matches:
			try:
				time += time_dict[k]*float(v)
			except KeyError:
				raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
			except ValueError:
				raise commands.BadArgument("{} is not a number!".format(v))
		return time

class MuteCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def mute(self, ctx, member:discord.Member, *, time:TimeConverter = None, reason=None):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		await member.add_roles(role)
		await ctx.send((f"Muted {member} for {time}s for: {reason}" if time else "Muted {}").format(member, time))
		if time:
			await asyncio.sleep(time)
			await member.remove_roles(role)

	@mute.error
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			pass
		if isinstance(error, commands.BadArgument):
			await ctx.send(error)
		else:
			error = getattr(error, 'original', error)
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def unmute(self, ctx, member:discord.Member):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		await member.remove_roles(role)
		await ctx.send(f"{member} was unmuted")

def setup(bot):
	bot.add_cog(MuteCog(bot))