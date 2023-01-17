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
        DB_NAME="Main_DB"
        #SQL File with Table Schema and Initialization Data
        SQL_File_Name = "Table_Schema.sql"
        ##############################################

        #Read Table Schema into a Variable and remove all New Line Chars
        TableSchema=""
        with open(SQL_File_Name, 'r') as SchemaFile:
         TableSchema=SchemaFile.read().replace('\n', '')

        #Connect or Create DB File
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        #Create Tables
        sqlite3.complete_statement(TableSchema)
        curs.executescript(TableSchema)

        #Close DB
        curs.close()
        conn.close()
        print("win")

    async def on_message(self,message):
        if message.author==client.user:
            return
        if message.author.bot:
            return

intents=discord.Intents.all()
client=MyClient(intents=intents)
FOToken=open('token',"r")
token=FOToken.readline()
client.run(token)