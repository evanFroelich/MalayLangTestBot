import discord
import sqlite3
import os
from discord.ext import tasks, commands
from discord.utils import get
from random import random
from datetime import datetime




class MyClient(discord.Client):
    questionMode='open'
    curQuestion=''
    curUser=''
    curChannel=''
    curFlipMode=0
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



            if self.questionMode=='in-use':
                if str(message.author.id) != self.curUser or str(message.channel.id) != self.curChannel:
                    curs.close()
                    conn.close()
                    return
                isCorrect='false'
                if self.curFlipMode==0:

                    if localMessage==self.curQuestion[3] or localMessage==self.curQuestion[4] or localMessage==self.curQuestion[5]:
                        isCorrect='true'
                else:
                    if localMessage==self.curQuestion[0]:
                        isCorrect='true'
                if isCorrect=='true':
                    await message.channel.send("correct")
                    sqlStatment='''SELECT * FROM Questions ORDER BY RANDOM() LIMIT 1'''
                    tableRow=curs.execute(sqlStatment)
                    for row in tableRow:
                        self.curQuestion=row
                        if row[1]==1:
                            r=random()
                            print(r)
                            if r<.5:
                                self.curFlipMode=1
                                await message.channel.send("translate: "+row[3])
                            else:
                                self.curFlipMode=0
                                await message.channel.send("translate: "+row[0])
                        else:
                            self.curFlipMode=0
                            await message.channel.send("translate: "+row[0])
                else:
                    await message.channel.send("incorrect. Correct answer is: "+ self.curQuestion[3] if self.curFlipMode==0 else "incorrect. Correct answer is: "+ self.curQuestion[0])
                    self.questionMode='open'
                curs.close()
                conn.close()
                return



            if splitString[0]=='..quiz':
                if self.questionMode=='open':
                    self.questionMode='in-use'
                    self.curChannel=str(message.channel.id)
                    self.curUser=str(message.author.id)
                    await message.channel.send(self.questionMode+" + "+self.curChannel+" + "+self.curUser)
                sqlStatment='''SELECT * FROM Questions ORDER BY RANDOM() LIMIT 1'''
                tableRow=curs.execute(sqlStatment)
                for row in tableRow:
                    self.curQuestion=row
                    if row[1]==1:
                        r=random()
                        if r<.5:
                            self.curFlipMode=1
                            await message.channel.send("translate: "+row[3])
                        else:
                            self.curFlipMode=0
                            await message.channel.send("translate: "+row[0])
                    else:
                        self.curFlipMode=0
                        await message.channel.send("translate: "+row[0])
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