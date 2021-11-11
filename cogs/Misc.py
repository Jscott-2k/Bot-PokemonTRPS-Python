from discord.ext import commands
from Main import Client
import functools
from discord.ext import tasks
from Game import Game
class Misc(commands.Cog):
    def __init__(self, bot):
        self._bot:Client = bot

    @commands.command(name="games", pass_context=True)
    async def list_games(self,ctx, *, message=None):
        games = self._bot.get_active_games()
   
        if(len(games) > 0 ):
            gamesInfo = map(lambda g:g.get_info(), games)
            gameString = functools.reduce(lambda ac,up: '\n'+f"{ac}{up}", gamesInfo)
            await ctx.send(f"List of active games:{gameString}")
        else:
            await ctx.send("No games active...")

def setup(bot):
    bot.add_cog(Misc(bot))
