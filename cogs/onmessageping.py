import discord
from discord.ext import commands


class onmessageping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.user.mention):
            prefixes = await self.bot.get_prefix(message)
            if isinstance(prefixes, list):
                for pre in prefixes:
                    if not str(self.bot.user.id) in pre:
                        prefix = pre
            else:
                prefix = prefixes
            embed = discord.Embed(
                description=f"My current prefix is `{prefix}`\n\nTo change my prefix run `{prefix}changeprefix <prefix>`",
                color=0x06C258,
            )
            await message.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(onmessageping(bot))
