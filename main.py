import discord
import sqlite3
import os
from discord.ext import tasks, commands
from discord.utils import get
from random import random
from datetime import datetime




class MyClient(discord.Client):
    questionMode="open"
    
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

        DB_NAME="Main_DB"
        conn=sqlite3.connect(DB_NAME)
        curs=conn.cursor()

        localMessage=message.content.lower()
        if len(localMessage)>0:
            splitString=localMessage.split('|')

            if splitString[0]=='..quiz':
                if self.questionMode=='open':
                    self.questionMode='in-use'
                    await message.channel.send(self.questionMode)
                sqlStatment='''SELECT * FROM Questions ORDER BY RANDOM() LIMIT 1'''
                tableRow=curs.execute(sqlStatment)
                for row in tableRow:
                    await message.channel.send(row)
                curs.close()
                conn.close()
                return
            if splitString[0]=='..format':
                await message.channel.send("..add|question|reversable(1 or 0)|number of answers|answer1|answer2|answer3")
            if splitString[0]=='..add':
                #await message.channel.send("also not ready yet")
                splitString[2]=int(splitString[2])
                splitString[3]=int(splitString[3])
                if(len(splitString)>=4 and len(splitString)<8):
                    if isinstance(splitString[2],int) and isinstance(splitString[3],int):
                        statment='''insert into Questions (Question, Reversable, NumAnswers, Answer1, Answer2, Answer3) values (?,?,?,?,?,?);'''
                        data=(splitString[1], int(splitString[2]), int(splitString[3]), splitString[4], "NULL", "NULL")
                        curs.execute(statment,data)
                        conn.commit()
                        await message.channel.send("added question")
                        curs.close()
                        conn.close()
                        return
                        
                await message.channel.send("invalid number of parameters:"+str(len(splitString)))
                curs.close()
                conn.close()
                return
                
        

intents=discord.Intents.all()
client=MyClient(intents=intents)
FOToken=open('token',"r")
token=FOToken.readline()
client.run(token)