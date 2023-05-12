import discord
import datetime
import asyncio
import re
from discord.ext import commands
import sys
import traceback


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k)
                )
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(
        self,
        ctx: commands.Context,
        member: discord.Member,
        time: int = None,
        *,
        reason=None,
    ):
        timeout_td = datetime.timedelta(seconds=time if time else 900)
        await member.timeout(
            timeout_td,
            reason=f"From {ctx.author.display_name}: {reason}."
            if reason
            else f"{ctx.author.display_name} provided no reason.",
        )
        embed = discord.Embed(
            description=f"{member} Muted for: {time or 900}s reason: {reason}",
            color=0x06C258,
        )
        embed.set_author(
            name=member.name + "#" + member.discriminator, icon_url=member.avatar.url
        )
        await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        else:
            error = getattr(error, "original", error)
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(
            None, reason=f"From {ctx.author.display_name}: removed timeout."
        )
        embed = discord.Embed(description=f"{member} was unmuted", color=0x06C258)
        embed.set_author(
            name=member.name + "#" + member.discriminator, icon_url=member.avatar.url
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(mute(bot))
