#!/bin/python

#these are needed to interfase with discord
import discord
from discord.ext import commands

#the DGUi library is in the DGui subfolder of the project
import sys
sys.path.append('DGui/')
#this is where the code to render the gui comes from, we need it to set up the gui main loop
import DGui

#this is where we store the code for our cusom guis to render
import gui_classes
#this file stores code for the sql classes that we use to interact with our database
import dndiscord_sql

print(discord.version_info)

def get_token(env='dndiscord_token'):
	import os
	return os.environ[env]	

bot = commands.Bot(command_prefix='dndiscord ')
bot.remove_command('help')
clientId = int(get_token('clientId'))


cha_gui = gui_classes.charicter_gui(dndiscord_sql.character(1))

@bot.command()
async def listCharicters(ctx):
	#this command displays the given character
	list_gui = gui_classes.charicter_list_gui(dndiscord_sql.player(str(hash(ctx.message.author))))	
	await list_gui.addSelf(ctx)

@bot.command()
async def ping(ctx):
	await ctx.send('pong')

#just a simple little function to alert the console when we connect
async def on_ready():
	print('[*] connected to discord!')

@bot.command()
async def testChar(ctx):
	#create a character gui with the test character and add them to the display
	await gui_classes.charicter_gui(dndiscord_sql.character(1)).addSelf(ctx)

#this is needed for the DGui script to have its events loaded properly
@bot.event
async def on_reaction_add(reaction, user):
#	print(reaction.emoji)
	await DGui.checkGui(clientId,reaction,user)
bot.run(get_token())
