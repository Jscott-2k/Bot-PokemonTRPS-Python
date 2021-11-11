from discord.ext import commands
from discord.message import Message
from Main import Client
from Game import Game

class Play(commands.Cog):
    
    def __init__(self, bot):
        self._bot:Client = bot

    @commands.command(name="play", pass_context=True)
    async def play_normal(self,ctx, *, message=None):
        await ctx.send("List of active games:")

    @commands.command(name="playcpu", pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def play_cpu(self,ctx, *, message=None):
        m:Message = ctx.message
        game:Game = self._bot.create_game(user_a = self._bot.user,user_b = m.author, channel=m.channel, cpu_game=True)
        if(game != None):
            self._bot.loop.create_task(game.start(ctx, self._bot))
        else:
            print(f"Failed to start game user_a = {self._bot.user} user_b = {m.author} channel = {m.channel}")
def setup(bot): 
    bot.add_cog(Play(bot))