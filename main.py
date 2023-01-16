import discord
import sqlite3
import os
from discord.ext import tasks, commands
from discord.utils import get
from random import random
from datetime import datetime


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

intents=discord.Intents.all()
client=MyClient(intents=intents)
FOToken=open('token',"r")
token=FOToken.readline()
client.run(token)