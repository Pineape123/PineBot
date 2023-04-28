import datetime, discord, math, psutil
from discord.ext import commands
import os
from discord import app_commands
class info(commands.Cog, name = "Random"):

	def __init__(self, client: commands.Bot):
		self.client = client
		self.start_time = datetime.datetime.now()

	@commands.command(aliases = ["ping", "statistics", "info"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def stats(self, ctx):
		message = await ctx.send("Gathering stats...")
		
		cpu = psutil.cpu_percent(interval = 1)
		memory = psutil.virtual_memory()
		latency = self.client.latency

		current_time = datetime.datetime.now()
		uptime = (current_time - self.start_time).total_seconds()

		embed = discord.Embed(title = "Stats", colour= 0x06c258)

		embed.set_author(name = self.client.user.name, icon_url = self.client.user.avatar and self.client.user.avatar.url or None)
		embed.add_field(name = "Latency", inline="false", value = f"{math.floor(latency * 1000)} ms")
		embed.add_field(name = "Total Servers", inline="false", value = str(len(self.client.guilds)))
		embed.add_field(name = "CPU Usage", inline="false",  value = f"{round(cpu)}%")
		embed.add_field(name = "Memory Usage", inline="false", value = f"{round((memory.total - memory.available) / math.pow(10, 9), 2)}GB / {round(memory.total / math.pow(10, 9), 2)}GB")
		embed.add_field(name = "Uptime", inline="false", value = f"{math.floor(uptime / 86400)} days, {math.floor(uptime % 86400 / 3600)} hours, {math.floor(uptime % 3600 / 60)} minutes")

		embed.set_footer(text="PineBot")
		await message.edit(content = None, embed = embed)

		
async def setup(bot: commands.Bot):
	await bot.add_cog(info(bot))