import os
from discord.abc import User
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.help import DefaultHelpCommand, HelpCommand
from discord.flags import Intents
from discord.message import Message
from discord.reaction import Reaction
from dotenv import load_dotenv
from pathlib import Path
from Game import Game

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class Client(commands.Bot):

    def __init__(self,command_prefix,help_command=None,description=None,**options):
        super().__init__(command_prefix=command_prefix,help_command=help_command,description=description,options=options)
        self._cogs = []
        self._active_games = []
        for p in Path('./cogs').glob('*.py'):
            self._cogs.append(os.path.splitext(p.name)[0])
        for cog in self._cogs:
            self.load_extension(f'cogs.{cog}')
        
    def get_active_games(self):
        return self._active_games

    def create_game(self, user_a, user_b, channel, cpu_game):
        print(f"Attemptng to create game user_a = {user_a} user_b = {user_b} channel = {channel}")
        if (user_a == None) or (user_b == None):
            return None
        game = Game(user_a=user_a, user_b=user_b, channel=channel, cpu_game=cpu_game)
        self._active_games.append(game)
        return game

    async def on_ready(self):
        print("Bot is ready!")
    async def on_reaction_add(self, reaction:Reaction, user:User):
        #channel:TextChannel = reaction.message.channel
        if user != self.user:
            await reaction.remove(user)
        #await channel.send(f"User {user.mention} reacted w/ {reaction.emoji}")

client = Client(command_prefix="!", intents=Intents.default())

if __name__ == '__main__':            
    client.run(DISCORD_BOT_TOKEN)