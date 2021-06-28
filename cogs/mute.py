import re
import datetime
from copy import deepcopy
import asyncio
import discord
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta


class mute(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.mute_task = self.check_current_mutes.start()

	@tasks.loop(minutes=5)
	async def check_current_mutes(self):
		currentTime = datetime.datetime.now()
		mutes = deepcopy(self.bot.muted_users)
		for key, value in mutes.items():
			if value['muteDuration'] is None:
				continue

			unmuteTime = value['mutedAt'] + relativedelta(seconds=value['muteDuration'])

			if currentTime >= unmuteTime:
				guild = self.bot.get_guild(value['guildId'])
				member = guild.get_member(value['_id'])

				role = discord.utils.get(guild.roles, name="Muted")
				if role in member.roles:
					await member.remove_roles(role)
					print(f"Unmuted: {member.display_name}")

				await self.bot.mutes.delete(member.id)
				try:
					self.bot.muted_users.pop(member.id)
				except KeyError:
					pass

	@check_current_mutes.before_loop
	async def before_check_current_mutes(self):
		await self.bot.wait_until_ready()

	@commands.command(
		name='mute',
		description="Mutes a given user for x time!",
		ussage='<user> [time]'
	)
	@commands.has_permissions(manage_roles=True)
	async def mute(self, ctx, member: discord.Member, *, time: TimeConverter=None):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if not role:
			await ctx.send("No muted role was found! Please create one called `Muted`")
			return

		try:
			if self.bot.muted_users[member.id]:
				await ctx.send("This user is already muted")
				return
		except KeyError:
			pass

		data = {
			'_id': member.id,
			'mutedAt': datetime.datetime.now(),
			'muteDuration': time or None,
			'mutedBy': ctx.author.id,
			'guildId': ctx.guild.id,
		}
		await self.bot.mutes.upsert(data)
		self.bot.muted_users[member.id] = data

		await member.add_roles(role)

		if not time:
			await ctx.send(f"Muted {member.display_name}")
		else:
			minutes, seconds = divmod(time, 60)
			hours, minutes = divmod(minutes, 60)
			if int(hours):
				await ctx.send(
					f"Muted {member.display_name} for {hours} hours, {minutes} minutes and {seconds} seconds"
				)
			elif int(minutes):
				await ctx.send(
					f"Muted {member.display_name} for {minutes} minutes and {seconds} seconds"
				)
			elif int(seconds):
				await ctx.send(f"Muted {member.display_name} for {seconds} seconds")

		if time and time < 300:
			await asyncio.sleep(time)

			if role in member.roles:
				await member.remove_roles(role)
				await ctx.send(f"Unmuted `{member.display_name}`")

			await self.bot.mutes.delete(member.id)
			try:
				self.bot.muted_users.pop(member.id)
			except KeyError:
				pass
def setup(bot):
	bot.add_cog(mute(bot))