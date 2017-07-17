import asyncio
from discord.ext import commands


class Help:
    """Commands that return helpful information."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def regions(self, ctx):
        """Lists valid regions"""
        msg = "BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR"
        await ctx.send("```fix\n" + msg + "\n```")

    @commands.command(no_pm=True)
    async def invite(self, ctx):
        """Add Blitzcrank to your server with this link!"""
        link = "https://discordapp.com/oauth2/authorize?client_id=282765243862614016&scope=bot&permissions=19456"
        await ctx.send("Invite me to your server with this link!\n" + link)

    @commands.command(no_pm=True)
    async def support(self, ctx):
        """Join the support server to ask for help!"""
        link = "https://discord.gg/J78uAgZ"
        await ctx.send("Join my support server if you need help with commands!\n " + link)


def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Help(bot))

# Base finished
