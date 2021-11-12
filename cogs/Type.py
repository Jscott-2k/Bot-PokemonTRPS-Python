from discord.ext import commands
from Main import Client
from Game import Game

class Type(commands.Cog):
    
    def __init__(self, bot):
        self._bot:Client = bot

    @commands.command(name="type", pass_context=True)
    async def type_data(self,ctx, *arg, message=None):
        print(f"Getting type data for {arg[0]}")
        typeData = Game.get_type_data(arg[0])
        #reaction = Game.get_reaction(arg[0])
        #strengths = Game.get_strengths(arg[0])

        if not typeData is None:
            await ctx.send(f"type data {typeData}")

    @commands.command(name="types", pass_context=True)
    async def list_types(self,ctx, *, message=None):
        await ctx.send(f"types: {Game.get_types_as_str()}")
        

def setup(bot):
    bot.add_cog(Type(bot))