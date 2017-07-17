from discord.ext import commands

import config


class Reload:
    """Blitzcrank's reloading module,"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def reload(self, ctx, *, module: str):
        """Reloads the specified module."""
        if ctx.message.author.id == config.OWNER_ID:
            try:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
            except Exception as e:
                await ctx.send("There was an error reloading module {}:".format(module))
                await ctx.send("```fix\n{}: {}\n```".format(type(e).__name__, e))
            else:
                await ctx.send("{} successfully reloaded.".format(module))
        else:
            await ctx.send("Sorry, you don't have permission to use that command!")


def setup(bot):
    bot.add_cog(Reload(bot))
