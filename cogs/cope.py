import discord
from discord.ext import commands
import random


class cope(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cope(self, ctx: commands.Context):
        copewords = [
            "Cope Bitch",
            "Its alright you were just born a loser",
            "Your future is bright",
            ":ghost:",
        ]
        x = random.choice(copewords)
        embed = discord.Embed(description=f"{x}", color=0x06C258)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(cope(bot))
