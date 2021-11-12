import math
import random
from discord import channel, reaction
from discord.channel import TextChannel
from discord.colour import Color
from discord.embeds import Embed
from discord.message import Message
from discord.user import User
from discord.ext.commands.context import Context
from discord.ext import tasks
import json

type_data_file = open('data.json',encoding="utf8")
type_data = json.load(type_data_file)
type_data_file.close()

reaction_type_map:dict = {}

for type in type_data:
    reaction_type_map.__setitem__(type_data[type]["reaction"], type)

print(f"Created type map: {list(reaction_type_map.items())}")
class Game():
    def __init__(self, user_a, user_b, channel, cpu_game=False):
        self._id:int = math.floor((random.random() * 8999999) + 1000000)
        self._cpu_game:bool = cpu_game
        self._user_a:User = user_a
        self._user_b:User = user_b
        self._user_b_type:str = "missing"
        self._user_a_type:str = "missing"
        self._channel:TextChannel = channel
        self._game_message:Message = None
        self._result = "undeclared"
        self._status = "initializing..."
        self._finished = False
        self._selection_message = "awaiting..."
        self._reaction_type_map = {}
        self._user_a_selected = False
        self._user_b_selected = False
        self._user_a_reaction = ""
        self._user_b_reaction = ""

    def get_info(self) -> str:
        return f"Game id:{self._id} status:{self._status} user 1:{self._user_a.display_name} user 2:{self._user_b.display_name} cpu:{self._cpu_game}\n"

    def is_finished(self) -> bool:
        return self._finished
    
    async def apply_embeded_message_changes(self):
        embed = Embed(title=self._id, color=0xFF0000)
        embed.add_field(name="Players",value=f"{self._user_a.mention}{self._user_b.mention}\n", inline=False)
        embed.add_field(name="Game Status", value=f"{self._status}\n", inline=False)
        embed.add_field(name="Result", value=self._result, inline=False)
        embed.add_field(name="Selections", value=self._selection_message, inline=False)
        print(f"Applying changes to game message {self._id} --> {self._selection_message}")
        await self._game_message.edit(embed=embed)
    
    async def start(self, ctx:Context, bot):
        embed = Embed(title=self._id, color=0xFF0000)
        embed.add_field(name="Players",value=f"{self._user_a.mention}{self._user_b.mention}\n", inline=False)
        embed.add_field(name="Game Status", value=f"{self._status}\n", inline=False)
        embed.add_field(name="Result", value=self._result, inline=False)
        embed.add_field(name="Selections", value=self._selection_message, inline=False)
        print(f"Started new game with {self._user_a} and {self._user_b}!")
        self._game_message = await ctx.send(embed=embed)
        await self.push_reactions()
        def check(reaction:reaction.Reaction, user):
            if reaction.message.id != self._game_message.id:
                print(f"Failed message ID check!")
                return False
            print(f"Checking against user: {user} in cpuGame={self._cpu_game}")
            if self._cpu_game:
                return user == self._user_b
            else:
                return user == self._user_a or user == self._user_b
        
        await self.set_status("Waiting for player(s)...")
        reaction_1, user_1 = await bot.wait_for("reaction_add", check=check, timeout=60.0)
        reaction_1 = reaction_1.emoji
        reaction_2 = None
        user_2 = None
        type_array = Game.get_types_as_array()
        
        
        if not self._cpu_game:
            
            reaction_2, user_2 = await bot.wait_for("reaction_add", check=check, timeout=60.0)
            reaction_2 = reaction_2.emoji

            if self._user_a.id == user_2.id:
                self._user_a_reaction = reaction_2
                self._user_b_reaction = reaction_1
            else:
                self._user_a_reaction = reaction_1
                self._user_b_reaction = reaction_2
        else:
            user_2 = self._user_a
            reaction_2 =  Game.get_reaction(type_array[math.floor(random.random()*len(type_array))])
            self._user_a_reaction = reaction_2
            self._user_b_reaction = reaction_1
        
        self._user_a_type = self.get_type_from_reaction(self._user_a_reaction)
        self._user_b_type = self.get_type_from_reaction(self._user_b_reaction)

        await self.set_status("Comparing...")

        await self.update_selections()

        await self.compare_response()
        await self.set_status("Done...")
    
    def get_type_from_reaction(self, reaction):
        return reaction_type_map[reaction]

    async def compare_response(self):
        strengths_a = Game.get_strengths(self._user_a_type)
        strengths_b = Game.get_strengths(self._user_b_type)

        if self._user_a_type in strengths_b and self._user_b_type in strengths_a:
            await self.set_result("TIE")
        elif self._user_a_type in strengths_b:
            await self.set_result(f"{self._user_b.mention} WINS! {self._user_b_type} beats {self._user_a_type}")
            return self._user_b
        elif self._user_b_type in strengths_a:
            await self.set_result(f"{self._user_a.mention} WINS! {self._user_a_type} beats {self._user_b_type}")
            return self._user_a
        elif self._user_a_type == self._user_b_type:
            await self.set_result("TIE")
        else:
            await self.set_result("TIE")

        return None

    async def set_result(self,result):
        self._result = result
        await self.apply_embeded_message_changes()
    
    async def set_status(self,status):
        self._status = status
        await self.apply_embeded_message_changes()
    
    async def update_selections(self):
        self._selection_message = f"{self._user_a.mention} --> {self._user_a_reaction} ||| {self._user_b.mention} --> ${self._user_b_reaction}"
        await self.apply_embeded_message_changes()
    
    async def push_reactions(self):
        types = Game.get_types_as_array()   
        for t in types:
            await self._game_message.add_reaction(Game.get_reaction(t))

    @staticmethod
    def get_types_as_str():
        return " ".join(list(type_data.keys()))
    
    @staticmethod
    def get_types_as_array():
        return list(type_data.keys())
    
    @staticmethod
    def get_type_data(type):
        if type in Game.get_types_as_array():
            return type_data[type]
        return None

    @staticmethod
    def get_strengths(type):
        return type_data[type]["strengths"]
    
    @staticmethod
    def get_reaction(type):
        return type_data[type]["reaction"]