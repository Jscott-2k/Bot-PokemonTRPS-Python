from discord.ext import commands
from Main import Client
from Game import Game

class Type(commands.Cog):
    
    def __init__(self, bot):
        self._bot:Client = bot

    @commands.command(name="type", pass_context=True)
    async def type_data(self,ctx, *, message=None):
        await ctx.send("List of active games:")

    @commands.command(name="types", pass_context=True)
    async def list_types(self,ctx, *, message=None):
        await ctx.send(f"types: {Game.get_types_as_str()}")
        

def setup(bot):
    bot.add_cog(Type(bot))