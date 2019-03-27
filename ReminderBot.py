#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import asyncio
import datetime
import re
import discord
from discord import Game
from discord.ext.commands import Bot


# In[2]:


BOT_PREFIX = ("^")
TOKEN = "NDQzODMzODg3MzQxNDEyMzYz.DdTJfg.pWTymsXJVslXw5PJV7fVw-12TQg"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)
#reminders looks like: reminders = [[expTime,'reminder',<channel info>,<author info>],...]
reminders = []




    
#Takes input and parses it for message time, duration to reminder, and content, appends to list of reminders
@client.command(name='remind',
                description="Set a reminder",
                brief="Set a reminder",
                pass_context=True)
async def remind(context):
    durregex = re.compile(r'(\d+) (years|year|yrs|yr|y|months|month|mos|mons|mon|m|weeks|week|wks|wk|w|days|day|dys|dy|d|hours|hour|hrs|hr|h|minutes|minute|mins|min|m|seconds|second|secs|sec|s)')
    search = durregex.search(context.message.content.lower())
    d_t = search.group(1)
    d_t_label = search.group(2)

    ###Makes proper duration depending on str found in message
    if d_t_label == str('days') or d_t_label == str('day') or d_t_label == str('dys') or d_t_label == str('dy') or d_t_label == str('d'):
        dur = datetime.timedelta(days=int(d_t))
    elif d_t_label == str('weeks') or d_t_label == str('week') or d_t_label == str('wks') or d_t_label == str('wk') or d_t_label == str('w'):
        dur = datetime.timedelta(weeks=int(d_t))
    elif d_t_label == str('hours') or d_t_label == str('hour') or d_t_label == str('hrs') or d_t_label == str('hr') or d_t_label == str('h'):
        dur = datetime.timedelta(hours=int(d_t))
    elif d_t_label == str('minutes') or d_t_label == str('minute') or d_t_label == str('mins') or d_t_label == str('min') or d_t_label == str('m'):
        dur = datetime.timedelta(minutes=int(d_t))
    elif d_t_label == str('seconds') or d_t_label == str('second') or d_t_label == str('secs') or d_t_label == str('sec') or d_t_label == str('s'):
        dur = datetime.timedelta(seconds=int(d_t))
    elif d_t_label == str('years') or d_t_label == str('year') or d_t_label == str('yrs') or d_t_label == str('yr') or d_t_label == str('y'):
        dur = datetime.timedelta(days=(365*int(d_t)))
    else:
        dur = dur = datetime.timedelta(seconds=1)

    time = context.message.timestamp   #time of message in UTC
    expTime = time + dur  #Time to call reminder

    ##Months Fix    
    if d_t_label == str('months') or d_t_label == str('month') or d_t_label == str('mos') or d_t_label == str('mons') or d_t_label == str('mon')or d_t_label == str('m'):
        now = datetime.datetime.utcnow()
        cur_mo = now.month
        fut_mo = now.month + int(d_t)
        if fut_mo < 13:
            expTime = datetime.datetime(now.year, fut_mo, now.day, hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
        else:
            yrs = int(fut_mo/12)
            fut_mo = fut_mo%12
            year = now.year + yrs
            expTime = datetime.datetime(year, fut_mo, now.day, hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
    
    reminder = str(context.message.content) #takes in message
    reminder = reminder.replace(r'^remind', '') #strip message down to reminder
    reminder = reminder.replace(d_t, '')
    reminder = reminder.replace(d_t_label, '')
    
    kind = 1
    channel = context.message.channel
    author = context.message.author
    newEntry = [expTime,reminder,channel,author,kind]
    reminders.append(newEntry)
    await client.say("Okay, " + context.message.author.mention + ', your reminder has been set for ' + d_t + ' ' + d_t_label + ' in the future!')
    #await client.say(reminder)


##PM REMINDER FUNCTION
@client.command(name='pmind',
                description="Set pm reminder",
                brief="Set pm reminder",
                pass_context=True)
async def pmind(context):
    durregex = re.compile(r'(\d+) (years|year|yrs|yr|y|months|month|mos|mons|mon|m|weeks|week|wks|wk|w|days|day|dys|dy|d|hours|hour|hrs|hr|h|minutes|minute|mins|min|m|seconds|second|secs|sec|s)')
    search = durregex.search(context.message.content.lower())
    d_t = search.group(1)
    d_t_label = search.group(2)

    ###Makes proper duration depending on str found in message
    if d_t_label == str('days') or d_t_label == str('day') or d_t_label == str('dys') or d_t_label == str('dy') or d_t_label == str('d'):
        dur = datetime.timedelta(days=int(d_t))
    elif d_t_label == str('weeks') or d_t_label == str('week') or d_t_label == str('wks') or d_t_label == str('wk') or d_t_label == str('w'):
        dur = datetime.timedelta(weeks=int(d_t))
    elif d_t_label == str('hours') or d_t_label == str('hour') or d_t_label == str('hrs') or d_t_label == str('hr') or d_t_label == str('h'):
        dur = datetime.timedelta(hours=int(d_t))
    elif d_t_label == str('minutes') or d_t_label == str('minute') or d_t_label == str('mins') or d_t_label == str('min') or d_t_label == str('m'):
        dur = datetime.timedelta(minutes=int(d_t))
    elif d_t_label == str('seconds') or d_t_label == str('second') or d_t_label == str('secs') or d_t_label == str('sec') or d_t_label == str('s'):
        dur = datetime.timedelta(seconds=int(d_t))
    elif d_t_label == str('years') or d_t_label == str('year') or d_t_label == str('yrs') or d_t_label == str('yr') or d_t_label == str('y'):
        dur = datetime.timedelta(days=(365*int(d_t)))
    else:
        dur = dur = datetime.timedelta(seconds=1)

    time = context.message.timestamp   #time of message in UTC
    expTime = time + dur  #Time to call reminder

    ##Months Fix    
    if d_t_label == str('months') or d_t_label == str('month') or d_t_label == str('mos') or d_t_label == str('mons') or d_t_label == str('mon')or d_t_label == str('m'):
        now = datetime.datetime.utcnow()
        cur_mo = now.month
        fut_mo = now.month + int(d_t)
        if fut_mo < 13:
            expTime = datetime.datetime(now.year, fut_mo, now.day, hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
        else:
            yrs = int(fut_mo/12)
            fut_mo = fut_mo%12
            year = now.year + yrs
            expTime = datetime.datetime(year, fut_mo, now.day, hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
    
    reminder = str(context.message.content) #takes in message
    reminder = reminder.replace(r'^pmind', '') #strip message down to reminder
    reminder = reminder.replace(d_t, '')
    reminder = reminder.replace(d_t_label, '')
    
    kind = 0
    channel = context.message.channel
    author = context.message.author
    newEntry = [expTime,reminder,channel,author,kind]
    reminders.append(newEntry)
    await client.say("Okay, " + context.message.author.mention + ', your pminder has been set for ' + d_t + ' ' + d_t_label + ' in the future!')
    #await client.say(reminder)
    

#Rechecks reminder database and calls reminders as their expirations come up    
@client.event
async def on_ready():
    await client.change_presence(game=Game(type=3,name="your dates"))
    print("Logged in as " + client.user.name)
    while not client.is_closed:
        #print('Reminders:')
        i_s = []

        for i in range(len(reminders)):
            reminder = reminders[i]
            if reminder[0] < datetime.datetime.utcnow():
                i_s.append(i)
                print(str(reminder[1]))
                if reminder[4] == 1:  #public reminder
                    ##If first arg changed to reminder[3], sends reminder as pm, rather than to group
                    await client.send_message(reminder[2], str(reminder[3].mention) + ' Reminder!' + str(reminder[1]))        
                elif reminder[4] == 0:  #pminder
                    await client.send_message(reminder[3], str(reminder[3].mention) + ' Reminder!' + str(reminder[1]))
                    
        i_s.sort(reverse=True)

        for i in i_s:
            del reminders[i]

        await asyncio.sleep(5)
        


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(100)
        
client.loop.create_task(list_servers())
client.run(TOKEN)

